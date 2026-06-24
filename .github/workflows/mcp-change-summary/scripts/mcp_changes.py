#!/usr/bin/env python3
"""Gather recent commits across the Adobe Analytics MCP repos for the public changelogs.

One subcommand:

  gather   Fetch each configured repo, collect the commits since a cutoff date, and print
           them as readable Markdown grouped by repo. The cutoff comes from either
           --since (an explicit date) or --since-changelog (read the most recent dated
           entry out of one or more existing changelog files). Nothing is persisted between
           runs -- the existing changelogs ARE the state, which is what lets this run in a
           stateless GitHub Action.

Auth: public repos clone over HTTPS with no credentials. Private repos need a token. Set
MCP_CHANGE_SUMMARY_TOKEN (or GH_TOKEN / GITHUB_TOKEN) and any github.com clone URL -- SSH or
HTTPS -- is rewritten to an authenticated HTTPS URL before cloning.

Clones live in a scratch dir (default ~/.mcp-change-summary/cache, override the parent with
MCP_CHANGE_SUMMARY_DIR). In CI the runner is ephemeral, so this is just a per-run workspace.
"""

import argparse
import os
import re
import json
import subprocess
import sys
from datetime import datetime, timezone
from urllib.parse import urlsplit, urlunsplit

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_CONFIG = os.path.join(HERE, "..", "config", "repos.json")

# Changelog date headers look like:  ### June 16, 2026
DATE_HEADER_RE = re.compile(r"^#{1,6}\s+([A-Z][a-z]+\s+\d{1,2},\s+\d{4})\s*$")


def data_dir():
    d = os.environ.get("MCP_CHANGE_SUMMARY_DIR") or os.path.expanduser("~/.mcp-change-summary")
    os.makedirs(d, exist_ok=True)
    return d


def cache_dir():
    d = os.path.join(data_dir(), "cache")
    os.makedirs(d, exist_ok=True)
    return d


def git(args, cwd=None, check=True):
    res = subprocess.run(["git"] + args, cwd=cwd, capture_output=True, text=True)
    if check and res.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed: {res.stderr.strip()}")
    return res.stdout


def token():
    for var in ("MCP_CHANGE_SUMMARY_TOKEN", "GH_TOKEN", "GITHUB_TOKEN"):
        val = os.environ.get(var)
        if val:
            return val.strip()
    return None


def authed_url(url):
    """Rewrite a github.com clone URL to authenticated HTTPS when a token is available.

    Handles both `git@github.com:org/repo.git` and `https://github.com/org/repo.git`. Without
    a token the URL is returned unchanged, which is fine for public repos like adobe/skills.
    """
    tok = token()
    if not tok:
        return url

    # git@github.com:org/repo.git  ->  org/repo.git
    m = re.match(r"^git@github\.com:(.+)$", url)
    if m:
        return f"https://x-access-token:{tok}@github.com/{m.group(1)}"

    parts = urlsplit(url)
    if parts.scheme in ("https", "http") and parts.hostname == "github.com":
        netloc = f"x-access-token:{tok}@github.com"
        return urlunsplit(("https", netloc, parts.path, parts.query, parts.fragment))

    return url


def ensure_repo(repo):
    """Return a working git dir for the repo, fetching the latest from origin.

    A `local_path` (an existing clone) is fetched in place. Otherwise the repo is mirrored
    into the scratch cache: cloned on first use, fetched thereafter.
    """
    branch = repo.get("branch", "main")
    if repo.get("local_path"):
        path = os.path.expanduser(repo["local_path"])
        if not os.path.isdir(os.path.join(path, ".git")):
            raise RuntimeError(f"not a git clone: {path}")
        git(["fetch", "--quiet", "origin", branch], cwd=path)
        return path
    if repo.get("clone_url"):
        path = os.path.join(cache_dir(), repo["name"])
        if not os.path.isdir(os.path.join(path, ".git")):
            git(["clone", "--quiet", "--filter=blob:none", authed_url(repo["clone_url"]), path])
        git(["fetch", "--quiet", "origin", branch], cwd=path)
        return path
    raise RuntimeError(f"repo {repo['name']} has neither local_path nor clone_url")


def commit_hashes(path, ref, since_iso, repo):
    """Hashes of non-merge commits since `since_iso`, honouring path/keyword filters.

    When filters are present a commit is included if it touches one of `path_filters`
    OR its message matches one of `keyword_filters` (case-insensitive) -- the union.
    """
    base = ["log", ref, f"--since={since_iso}", "--no-merges", "--pretty=%H"]
    path_filters = repo.get("path_filters")
    keyword_filters = repo.get("keyword_filters")

    if not path_filters and not keyword_filters:
        out = git(base, cwd=path)
        return list(dict.fromkeys(out.split()))

    hashes = []
    if path_filters:
        out = git(base + ["--"] + path_filters, cwd=path)
        hashes += out.split()
    if keyword_filters:
        grep = []
        for kw in keyword_filters:
            grep += ["--grep", kw]
        out = git(base + ["-i"] + grep, cwd=path)
        hashes += out.split()
    return list(dict.fromkeys(hashes))


def commit_detail(path, h):
    fmt = "%H%x1f%an%x1f%cI%x1f%s%x1f%b"
    out = git(["show", "-s", f"--pretty={fmt}", h], cwd=path)
    full, an, ci, subject, body = (out.split("\x1f") + ["", "", "", "", ""])[:5]
    files = git(["show", "--name-only", "--pretty=format:", h], cwd=path)
    file_list = [f for f in files.splitlines() if f.strip()]
    return {
        "hash": full.strip()[:9],
        "author": an.strip(),
        "date": ci.strip(),
        "subject": subject.strip(),
        "body": body.strip(),
        "files": file_list,
    }


def latest_changelog_date(path):
    """Most recent dated entry in a changelog file, as a date, or None if there are none."""
    dates = []
    with open(path) as f:
        for line in f:
            m = DATE_HEADER_RE.match(line.rstrip())
            if m:
                try:
                    dates.append(datetime.strptime(m.group(1), "%B %d, %Y").date())
                except ValueError:
                    pass
    return max(dates) if dates else None


def resolve_since(args):
    """Work out the cutoff date as an ISO string for `git log --since`.

    --since wins if given. Otherwise read every --since-changelog file and use the EARLIEST
    of their most-recent entries, so a single gather safely covers both changelogs even if
    one is slightly behind the other. Returns (since_iso, source_description).
    """
    if args.since:
        return args.since, f"--since {args.since}"

    if args.since_changelog:
        found = {}
        for p in args.since_changelog:
            d = latest_changelog_date(p)
            if d:
                found[p] = d
        if not found:
            raise RuntimeError(
                "no dated entries (e.g. '### June 16, 2026') found in: "
                + ", ".join(args.since_changelog)
            )
        cutoff = min(found.values())
        detail = ", ".join(
            f"{os.path.join(os.path.basename(os.path.dirname(p)), os.path.basename(p))}={d.isoformat()}"
            for p, d in found.items()
        )
        return cutoff.isoformat(), f"latest changelog entries ({detail}); using earliest"

    raise RuntimeError("provide --since YYYY-MM-DD or --since-changelog FILE [FILE ...]")


def gather(config, since_iso):
    now = datetime.now(timezone.utc)
    results = []
    for repo in config["repos"]:
        entry = {
            "name": repo["name"],
            "label": repo.get("label", repo["name"]),
            "description": repo.get("description", ""),
            "changelogs": repo.get("changelogs", []),
            "commits": [],
            "error": None,
        }
        try:
            path = ensure_repo(repo)
            ref = f"origin/{repo.get('branch', 'main')}"
            hashes = commit_hashes(path, ref, since_iso, repo)
            entry["commits"] = [commit_detail(path, h) for h in hashes]
        except Exception as e:  # one repo failing should not sink the rest
            entry["error"] = str(e)
        results.append(entry)

    return {
        "generated_at": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "since": since_iso,
        "repos": results,
    }


def print_markdown(payload, since_source):
    print("# Raw MCP repo changes")
    print(f"\nWindow: commits since `{payload['since']}` through `{payload['generated_at']}` "
          f"(UTC).\nCutoff source: {since_source}.\n")
    total = sum(len(r["commits"]) for r in payload["repos"])
    print(f"Total matching commits: **{total}**\n")
    for r in payload["repos"]:
        tags = f"  →  feeds: {', '.join(r['changelogs'])}" if r["changelogs"] else ""
        print(f"\n## {r['label']}  (`{r['name']}`){tags}")
        if r["description"]:
            print(f"_{r['description']}_")
        if r["error"]:
            print(f"\n⚠️ Could not read this repo: {r['error']}")
            continue
        if not r["commits"]:
            print("\nNo matching changes in this window.")
            continue
        print(f"\n{len(r['commits'])} commit(s):")
        for c in r["commits"]:
            print(f"\n- **{c['subject']}**  ({c['hash']}, {c['author']}, {c['date'][:10]})")
            if c["body"]:
                for line in c["body"].splitlines():
                    if line.strip():
                        print(f"    > {line.strip()}")
            if c["files"]:
                shown = c["files"][:8]
                more = "" if len(c["files"]) <= 8 else f" (+{len(c['files']) - 8} more)"
                print(f"    files: {', '.join(shown)}{more}")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("command", choices=["gather"])
    ap.add_argument("--config", default=DEFAULT_CONFIG)
    ap.add_argument("--since", help="cutoff date for git log, e.g. 2026-06-16")
    ap.add_argument("--since-changelog", nargs="+", metavar="FILE",
                    help="read the cutoff from the most recent entry in these changelog files")
    ap.add_argument("--json", action="store_true", help="print raw JSON instead of Markdown")
    args = ap.parse_args()

    since_iso, since_source = resolve_since(args)
    with open(args.config) as f:
        config = json.load(f)
    payload = gather(config, since_iso)
    if args.json:
        print(json.dumps(payload, indent=2))
    else:
        print_markdown(payload, since_source)
    return 0


if __name__ == "__main__":
    sys.exit(main())

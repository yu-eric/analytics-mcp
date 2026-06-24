---
name: mcp-change-summary
description: >-
  Update the public Adobe Analytics and Customer Journey Analytics MCP changelogs
  (src/pages/aa/changelog.md and src/pages/cja/changelog.md) with a new dated entry that
  covers recent work across the MCP repos (aa-mcp-server, cja-mcp-server,
  analytics-mcp-starter, app_mcp_evaluator, and the AA/CJA skills in adobe/skills). Use this
  whenever the user wants to update or refresh the AA or CJA changelog, add a new changelog
  entry, write up "what shipped" or "what changed" on the MCP servers, or run the periodic
  changelog update — and it runs unattended in the changelog GitHub Action. The window is
  detected automatically: from the most recent date already in each changelog through today.
---

# MCP Change Summary

Add a new dated entry to the two public MCP changelogs — `src/pages/aa/changelog.md` and
`src/pages/cja/changelog.md` — describing what shipped since each was last updated. The
output is a **customer-facing changelog**: short, outcome-focused bullets in the established
voice of those files, not an internal commit log or a leadership memo.

The existing entries are your style reference. Read both files first and match them exactly:
flat bullets under a `### Month D, YYYY` date header, each bullet a single past-tense
statement of something a customer can now do or rely on.

## How it works

There is no saved state — the changelogs themselves are the record. You find the most recent
date already in each file, gather every commit since then across the relevant repos, and
write the meaningful ones up as a new entry dated today. A helper script does all the git
work (cloning/fetching, applying the cutoff, filtering, collecting commits); you read its
output and write the prose.

Which repo feeds which changelog is declared in `config/repos.json` (the `changelogs` field)
and echoed in the script output:

| Repo | AA | CJA |
|------|----|----|
| aa-mcp-server | ✓ | |
| cja-mcp-server | | ✓ |
| analytics-mcp-starter (shared) | ✓ | ✓ |
| app_mcp_evaluator (quality/coverage) | | ✓ |
| adobe/skills (AA + CJA plugins) | ✓ | ✓ |

Shared-library work lands in both changelogs; skills work lands in whichever product the
skill belongs to.

## Steps

### 1. Find the window

Read both changelog files and note the most recent `### Month D, YYYY` header in each. That
date is where each file's new entry begins; today is where it ends.

### 2. Gather the raw changes

Run the helper, pointing it at both changelog files so it derives the cutoff itself (it uses
the earlier of the two most-recent dates, so nothing slips through if one file is behind):

```bash
python3 ~/.claude/skills/mcp-change-summary/scripts/mcp_changes.py gather \
  --since-changelog src/pages/aa/changelog.md src/pages/cja/changelog.md
```

It prints the matching commits grouped by repo, each repo tagged with the changelog(s) it
feeds. (You can also pass `--since 2026-06-16` to force a cutoff.)

- If a repo reports an error (SSH/network/auth), note it to the user and keep going — a
  partial update is fine; a wrong one is not. Don't invent entries for a repo you couldn't read.
- If there are zero relevant changes across all repos, say so and leave the files untouched.
  Don't write an empty `### <today>` header. (In the Action, no changes means no PR.)

### 3. Write the changelog entries

For each changelog, add one new section dated **today** above the previous most-recent entry,
covering only changes that postdate that file's own latest entry. If a section for today
already exists, merge into it instead of adding a duplicate.

Keep the file's existing format precisely:

```markdown
### June 23, 2026
- One outcome per bullet, past tense.
- Another outcome.
```

No "Highlights", no "By area", no "Notes", no forward-looking section — just the dated header
and the bullets, exactly like the entries already in the file.

#### Turning commits into changelog bullets

The hard part is translation. A changelog reader wants to know what's now true for them, not
what an engineer did.

- **State the outcome, not the change.** "Add retry with backoff to dimension lookup" →
  "Improved reliability of data lookups under load." "Fix null deref in segment parser" →
  "Resolved an issue that could cause segment reports to fail."
- **Lead with the verb, past tense**, matching the file: *Added, Enabled, Launched, Released,
  Expanded, Improved, Resolved, Completed.*
- **Group by theme, not by commit.** Several commits toward one capability become one bullet.
  Aim for a tight set of bullets per entry, in line with the existing entries' length.
- **Keep it customer-facing.** No commit hashes, file paths, author names, internal codenames,
  or ticket numbers. If a reasonable customer wouldn't care, leave it out.
- **Quantify when the commits support it** — "11 analytics skills", "coverage expanded to N
  tools" reads better than "various improvements." Never invent numbers.
- **Drop pure noise** — version bumps, lint, formatting, dependency updates, CI tweaks,
  internal refactors — unless it rolls up into something a customer feels (e.g. testing work
  framed as "Expanded automated test coverage and evaluation datasets").
- **Don't restate** anything already captured in an earlier entry.

When in doubt about whether something is meaningful enough to publish, leave it out — the
changelog is curated, not exhaustive.

### 4. Hand off

The skill's job ends once the two files are edited. Committing and opening the PR is the
harness's responsibility (the GitHub Action does this; interactively, tell the user what you
changed). Briefly summarize, per changelog, what you added and the window it covers.

## Running in CI

The changelog GitHub Action (`.github/workflows/update-changelog.yml`) runs this skill on a
manual trigger and opens a single PR with both changelog edits. Two things the script needs
in that environment:

- **A token for the private repos.** The four `AdobeAnalytics/*` repos are private; cloning
  them needs a token with read access, supplied via `MCP_CHANGE_SUMMARY_TOKEN` (or
  `GH_TOKEN` / `GITHUB_TOKEN`). The script rewrites the SSH/HTTPS clone URLs to authenticated
  HTTPS automatically when a token is present. `adobe/skills` is public and needs none.
- **The skill on disk.** The Action copies this directory to `~/.claude/skills/` so the
  script path above resolves.

## Adding or changing repos

Edit `config/repos.json`. Each repo needs either a `local_path` (an existing clone, fetched
in place) or a `clone_url` (mirrored into the scratch cache). Set `changelogs` to the list of
products it feeds (`"aa"`, `"cja"`, or both). Add `path_filters` and/or `keyword_filters` to
narrow a large/shared repo (like `adobe/skills`) to only the relevant changes.

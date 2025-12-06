---
applyTo: "**"
---

# GitHub Analysis Tools

`spoon_toolkits.github.github_analysis_tool` bundles three ready-made `BaseTool` classes that call the GitHub GraphQL API via `GitHubProvider`. Each tool simply returns the raw list of entities (`issues`, `pull requests`, `commits`) interpolated into a single string.

## Environment

```bash
export GITHUB_TOKEN=ghp_your_personal_access_token   # repo scope recommended
```

- Each tool pulls `GITHUB_TOKEN` unless you pass `token="..."` explicitly. Missing credentials surface as `ToolResult(error="GitHub token is required...")`.
- GitHub's GraphQL endpoint enforces a rate limit of 5,000 points/hour per token. These tools request up to 100 nodes per call.

## Tool Catalog

| Tool | Parameters | Raw data returned | Use cases |
|------|------------|-------------------|-----------|
| `GetGitHubIssuesTool` | `owner`, `repo`, `start_date`, `end_date`, optional `token` | List of up to 100 issues with `title`, `state`, labels, comment totals, author, timestamps | Bug triage dashboards, changelog assembly |
| `GetGitHubPullRequestsTool` | Same window parameters | List of up to 100 pull requests with merge info, review counts, commit totals, labels | Contributor scorecards, weekly PR digests |
| `GetGitHubCommitsTool` | Same window parameters | Default branch history (first 100 commits) including message, author name/email, additions/deletions | Release notes, productivity metrics |

All parameters accept ISO `YYYY-MM-DD` strings. The window is inclusive and aligned to UTC.

## Usage Patterns

### Issues snapshot

```python
from spoon_toolkits.github.github_analysis_tool import GetGitHubIssuesTool

issues_tool = GetGitHubIssuesTool()
issues_result = await issues_tool.execute(
    owner="XSpoonAi",
    repo="spoon-core",
    start_date="2024-01-01",
    end_date="2024-02-01",
)

if issues_result.error:
    raise RuntimeError(issues_result.error)

raw_issues = issues_result.output
print(raw_issues)

from ast import literal_eval
issues_payload = literal_eval(raw_issues.replace("GitHub issues: ", "", 1))
for issue in issues_payload:
    print(issue["title"], issue["state"])
```

### Weekly contributor digest

```python
from datetime import date, timedelta
from spoon_toolkits.github.github_analysis_tool import (
    GetGitHubIssuesTool,
    GetGitHubPullRequestsTool,
    GetGitHubCommitsTool,
)

today = date.today()
week_ago = today - timedelta(days=7)
window = dict(
    owner="XSpoonAi",
    repo="spoon-core",
    start_date=week_ago.isoformat(),
    end_date=today.isoformat(),
)

issues = await GetGitHubIssuesTool().execute(**window)
prs = await GetGitHubPullRequestsTool().execute(**window)
commits = await GetGitHubCommitsTool().execute(**window)
```

## Error Handling Tips

- Inspect `ToolResult.error` before consuming `output`.
- If GitHub throttles you, the GraphQL API returns `errors: [{"type": "RATE_LIMITED", ...}]`.
- Dates outside the repository lifetime simply return an empty list.

## Next Steps

- [GitHub Provider](./toolkit-github-provider.instructions.md) - Low-level GraphQL client
- [Social Media Tools](./toolkit-social-media.instructions.md) - Communication channels

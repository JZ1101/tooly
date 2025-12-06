---
applyTo: "**"
---

# AIOZ Storage Tools

`spoon_toolkits.storage.aioz` wraps AIOZ W3S (S3-compatible object storage) in ready-made `BaseTool` classes so Spoon agents can upload, list, download, and delete files with minimal setup.

## Environment & Credentials

```bash
export AIOZ_REGION=us-east-1
export AIOZ_ACCESS_KEY=your_access_key
export AIOZ_SECRET_KEY=your_secret_key
export AIOZ_BUCKET_NAME=your_bucket_name
```

- Missing credentials surface as `ValueError` on tool initialization.
- Each tool constructs its own `boto3.client("s3", ...)` using these variables.
- AIOZ supports both direct bucket creation and multi-region endpoints; set `AIOZ_REGION` to match your gateway.

## Tool Catalog

| Tool | Parameters | What it does | Return format |
|------|------------|--------------|---------------|
| `UploadFileToAIOZTool` | `file_path` (str) | Upload local file to AIOZ bucket | Status dict `{"status": "success"/"error", ...}` |
| `ListFilesFromAIOZTool` | None | List all objects in bucket | Status dict with `files: [...]` array |
| `DownloadFileFromAIOZTool` | `file_name` (str), `local_path` (str) | Download from bucket to local filesystem | Status dict |
| `DeleteFileFromAIOZTool` | `file_name` (str) | Remove object from bucket | Status dict |

All status dicts include a `message` field with a human-readable description.

## Usage Patterns

### Upload local file

```python
from spoon_toolkits.storage.aioz.aioz_tools import UploadFileToAIOZTool

upload_tool = UploadFileToAIOZTool()
result = await upload_tool.execute(file_path="./data/report.pdf")
if result["status"] != "success":
    raise RuntimeError(result["message"])
```

### List bucket contents

```python
from spoon_toolkits.storage.aioz.aioz_tools import ListFilesFromAIOZTool

list_tool = ListFilesFromAIOZTool()
listing = await list_tool.execute()
print("Files:", listing.get("files", []))
```

### Download from bucket

```python
from spoon_toolkits.storage.aioz.aioz_tools import DownloadFileFromAIOZTool

download_tool = DownloadFileFromAIOZTool()
result = await download_tool.execute(
    file_name="report.pdf",
    local_path="./downloads/report.pdf",
)
```

### Delete a file

```python
from spoon_toolkits.storage.aioz.aioz_tools import DeleteFileFromAIOZTool

delete_tool = DeleteFileFromAIOZTool()
result = await delete_tool.execute(file_name="old_report.pdf")
```

## Error Handling

Each tool captures `ClientError` and returns `{"status": "error", "message": str(e)}`. Agents should inspect `result["status"]` before trusting the payload.

## Next Steps

- [4EVERLAND Storage](./toolkit-storage-foureverland.instructions.md) - Multi-chain decentralized storage
- [OORT Storage](./toolkit-storage-oort.instructions.md) - OORT network S3 tools

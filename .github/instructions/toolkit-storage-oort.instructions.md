---
applyTo: "**"
---

# OORT Storage Tools

`spoon_toolkits.storage.oort` offers `boto3`-based S3 tools that target the OORT network (S3-compatible decentralized storage). Use these when you need high-durability object storage with an S3 interface.

## Environment & Credentials

```bash
export OORT_REGION=us-east-1
export OORT_ACCESS_KEY=your_access_key
export OORT_SECRET_KEY=your_secret_key
export OORT_BUCKET_NAME=your_bucket_name
```

- Each tool constructs its own `boto3.client("s3", ...)` using `endpoint_url=f"https://s3.{OORT_REGION}.oortech.com"`.
- Missing credentials raise `ValueError` on tool initialization.

## Tool Catalog

| Tool | Parameters | What it does | Return format |
|------|------------|--------------|---------------|
| `UploadFileToOORTTool` | `file_path` (str) | Upload local file to OORT S3 bucket | Status dict `{"status": "success"/"error", ...}` |
| `ListFilesFromOORTTool` | None | List all objects in the bucket | Status dict with `files: [...]` array |
| `DownloadFileFromOORTTool` | `file_name` (str), `local_path` (str) | Download object from bucket to local filesystem | Status dict |
| `DeleteFileFromOORTTool` | `file_name` (str) | Remove object from bucket | Status dict |

All status dicts include a `message` field with a human-readable description.

## Usage Patterns

### Upload file to OORT

```python
from spoon_toolkits.storage.oort.oort_tools import UploadFileToOORTTool

upload_tool = UploadFileToOORTTool()
result = await upload_tool.execute(file_path="./data/archive.zip")
if result["status"] != "success":
    raise RuntimeError(result["message"])
```

### List bucket contents

```python
from spoon_toolkits.storage.oort.oort_tools import ListFilesFromOORTTool

list_tool = ListFilesFromOORTTool()
listing = await list_tool.execute()
print("Files:", listing.get("files", []))
```

### Download from OORT

```python
from spoon_toolkits.storage.oort.oort_tools import DownloadFileFromOORTTool

download_tool = DownloadFileFromOORTTool()
result = await download_tool.execute(
    file_name="archive.zip",
    local_path="./downloads/archive.zip",
)
```

### Delete file

```python
from spoon_toolkits.storage.oort.oort_tools import DeleteFileFromOORTTool

delete_tool = DeleteFileFromOORTTool()
result = await delete_tool.execute(file_name="old_archive.zip")
```

## Error Handling

Each tool captures `ClientError` exceptions from the boto3 S3 client and returns `{"status": "error", "message": str(e)}`. Agents should always inspect `result["status"]` before trusting the payload.

## Operational Notes

- OORT endpoints are region-specific: `https://s3.{region}.oortech.com`.
- Buckets must be pre-created; tools do not auto-create buckets if missing.
- The `UploadFileToOORTTool` uploads the file using its basename as the object key. For nested paths, wrap or extend the tool.

## Next Steps

- [Memory Tools](./toolkit-memory-mem0.instructions.md) - Long-term memory integration
- [Toolkit Index](./toolkit-index.instructions.md) - Complete toolkit overview

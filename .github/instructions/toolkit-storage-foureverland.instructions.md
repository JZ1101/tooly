---
applyTo: "**"
---

# 4EVERLAND Storage Tools

`spoon_toolkits.storage.foureverland` provides async `BaseTool` classes that wrap 4EVERLAND's IPFS and S3 endpoints. Use these tools when you need pinned IPFS uploads, bucket operations, or direct S3 reads/writes in a decentralized storage context.

## Environment & Credentials

```bash
# IPFS pinning
export FOUREVERLAND_API_KEY=your_api_key

# S3-compatible bucket access
export FOUREVERLAND_S3_ACCESS_KEY=your_access_key
export FOUREVERLAND_S3_SECRET_KEY=your_secret_key
export FOUREVERLAND_S3_REGION=us-west-1
export FOUREVERLAND_S3_BUCKET=your_bucket_name
```

- IPFS tools (`CreateOrUploadIpfsFolderTo4EverlandTool`, `ListIPFSPinsFrom4EverlandTool`, `DeleteIPFSPinFrom4EverlandTool`) require only `FOUREVERLAND_API_KEY`.
- S3 tools (`Upload4EverlandS3Tool`, `Get4EverlandS3Tool`) need all four S3 credentials and target `https://endpoint.4everland.co`.
- Missing or empty variables surface as tool initialization errors.

## Tool Catalog

| Tool | What it does | Return format |
|------|--------------|---------------|
| `CreateOrUploadIpfsFolderTo4EverlandTool` | Pin a folder to IPFS; returns CID and web link | Status string (✅ or ❌) |
| `ListIPFSPinsFrom4EverlandTool` | Query current IPFS pin status | Status string (✅ with pin list or ❌) |
| `DeleteIPFSPinFrom4EverlandTool` | Remove a pin by its UUID | Status string |
| `Upload4EverlandS3Tool` | Upload local file to S3 bucket | Status string with S3 URL on success |
| `Get4EverlandS3Tool` | Retrieve S3 object as bytes | Status string or raw object body |

All status strings include success/error codes (✅, ❌) for easy agent parsing.

## IPFS Pinning Workflow

### Upload folder to IPFS

```python
from spoon_toolkits.storage.foureverland.foureverland_tools import CreateOrUploadIpfsFolderTo4EverlandTool

ipfs_tool = CreateOrUploadIpfsFolderTo4EverlandTool()
result = await ipfs_tool.execute(folder_path="./my-nft-collection")
if not result.startswith("✅"):
    raise RuntimeError(result)
# Extract CID from result string
cid = result.split("CID: ")[1].split(",")[0]
```

### List existing pins

```python
from spoon_toolkits.storage.foureverland.foureverland_tools import ListIPFSPinsFrom4EverlandTool

list_tool = ListIPFSPinsFrom4EverlandTool()
pins = await list_tool.execute()
print(pins)
```

### Unpin a file

```python
from spoon_toolkits.storage.foureverland.foureverland_tools import DeleteIPFSPinFrom4EverlandTool

delete_tool = DeleteIPFSPinFrom4EverlandTool()
result = await delete_tool.execute(pin_id="abc-123-xyz")
```

## S3 Operations

### Upload to S3

```python
from spoon_toolkits.storage.foureverland.foureverland_tools import Upload4EverlandS3Tool

s3_upload_tool = Upload4EverlandS3Tool()
result = await s3_upload_tool.execute(
    file_path="./report.pdf",
    object_key="reports/report.pdf",
)
if result.startswith("❌"):
    raise RuntimeError(result)
# result contains the S3 URL
```

### Download from S3

```python
from spoon_toolkits.storage.foureverland.foureverland_tools import Get4EverlandS3Tool

s3_get_tool = Get4EverlandS3Tool()
result = await s3_get_tool.execute(object_key="reports/report.pdf")
if result.startswith("❌"):
    raise RuntimeError(result)
# result contains the object body as string or bytes
```

## Error Handling

- IPFS tools catch HTTP/network exceptions and return `❌` messages.
- S3 tools catch `ClientError` and return `❌` prefixed strings.
- Agents should use `result.startswith("✅")` checks before proceeding with returned data.

## Operational Notes

- 4EVERLAND's IPFS gateway publishes pins at `https://gateway.4everland.co/ipfs/{cid}`.
- S3 objects resolve to `https://your_bucket.4everland.co/{object_key}`.
- The default request timeout for IPFS endpoints is 60 seconds. Large folders may exceed this; consider chunked uploads or timeouts extension.

## Next Steps

- [OORT Storage](./toolkit-storage-oort.instructions.md) - OORT network S3 tools
- [Memory Tools](./toolkit-memory-mem0.instructions.md) - Long-term memory integration

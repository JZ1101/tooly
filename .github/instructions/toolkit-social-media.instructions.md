---
applyTo: "**"
---

# Social Media Tools

`spoon_toolkits.social_media` unifies Discord, Telegram, Twitter/X, and email under a single set of `BaseTool` classes so your Spoon agents can send messages, post updates, and check inbox content.

## Environment & Credentials

```bash
# Discord webhook integration
export DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/123456/abcdef

# Telegram bot
export TELEGRAM_BOT_TOKEN=123456:ABCDEFghijklmno
export TELEGRAM_CHANNEL_USERNAME=@your_channel_id

# Twitter/X bot (API v1.1 + v2 keys)
export TWITTER_API_KEY=abc...
export TWITTER_API_SECRET=def...
export TWITTER_ACCESS_TOKEN=ghi...
export TWITTER_ACCESS_TOKEN_SECRET=jkl...
export TWITTER_BEARER_TOKEN=mno...  # optional for v2 endpoints

# Email (Gmail SMTP)
export EMAIL_SENDER=your_email@gmail.com
export EMAIL_PASSWORD=your_app_password  # use App Password, not account password
```

- Each service is optional. Agents will safely skip unavailable tools if credentials are missing.
- Discord uses webhook-based posting (no OAuth).
- Telegram expects a pre-configured bot token and channel username.
- Twitter integration uses Tweepy; supply all five credentials for full post + engagement.
- Email leverages Gmail SMTP; secure the password with an App Password to avoid 2FA conflicts.

## Package Layout

| Module | Purpose |
|--------|---------|
| `discord_tools.py` | `SendDiscordMessageTool` - POST text to a Discord channel via webhook |
| `telegram_tools.py` | `SendTelegramMessageTool`, `CheckTelegramMessagesTool` - post and poll messages |
| `twitter_tools.py` | `PostTweetTool`, `CheckTwitterEngagementTool` - create tweets and fetch engagement stats (replies, retweets, favorites) |
| `email_tools.py` | `SendEmailTool`, `CheckEmailTool` - send and check for new emails via Gmail SMTP/IMAP |

## Tooling Highlights

### Discord
- `SendDiscordMessageTool` - posts a string to the configured webhook. Returns status dict `{"status": "success"/"failed", "message": "..."}`.

### Telegram
- `SendTelegramMessageTool` - send text to a channel. Returns status string (no exception on error).
- `CheckTelegramMessagesTool` - fetch last 10 updates from the bot. Returns status string summarizing messages/senders.

### Twitter/X
- `PostTweetTool` - create a tweet with optional `in_reply_to_status_id`. Returns `{"status": "success"/"failed", "tweet_id"/"message": ...}`.
- `CheckTwitterEngagementTool` - query mentions, retweets, favorites for a given tweet ID. Returns formatted string with numeric totals.

### Email
- `SendEmailTool` - compose and send an email. Returns `{"status": "success"/"error", ...}`.
- `CheckEmailTool` - scan inbox for subjects matching an optional filter. Returns plain-text summary.

## Usage Examples

### Post to Discord

```python
from spoon_toolkits.social_media.discord_tools import SendDiscordMessageTool

discord_tool = SendDiscordMessageTool()
result = await discord_tool.execute(message="Daily report: 🚀")
if result["status"] != "success":
    raise RuntimeError(result["message"])
```

### Telegram bot flow

```python
from spoon_toolkits.social_media.telegram_tools import (
    SendTelegramMessageTool,
    CheckTelegramMessagesTool,
)

send_tool = SendTelegramMessageTool()
await send_tool.execute(message="System online")

check_tool = CheckTelegramMessagesTool()
updates = await check_tool.execute()
print(updates)
```

### Twitter engagement tracking

```python
from spoon_toolkits.social_media.twitter_tools import PostTweetTool, CheckTwitterEngagementTool

post_tool = PostTweetTool()
post_result = await post_tool.execute(message="New release v2.0!")
if post_result["status"] == "success":
    tweet_id = post_result["tweet_id"]

    engagement_tool = CheckTwitterEngagementTool()
    stats = await engagement_tool.execute(tweet_id=tweet_id)
    print(stats)
```

### Email workflow

```python
from spoon_toolkits.social_media.email_tools import SendEmailTool, CheckEmailTool

send_tool = SendEmailTool()
send_result = await send_tool.execute(
    recipient="user@example.com",
    subject="Notification",
    body="Task completed successfully.",
)

check_tool = CheckEmailTool()
inbox = await check_tool.execute(subject_filter="Notification")
```

## Operational Notes

- Use App Passwords for Gmail; standard account passwords won't work with SMTP/IMAP.
- Discord webhooks have rate limits (~30 messages/minute); stagger bulk posts.
- Telegram's `getUpdates` endpoint reads up to 100 messages by default; the tool slices to the last 10.
- Twitter's v1.1 API is rate-limited at 300 requests per 15-minute window per endpoint; avoid tight polling loops.
- Each tool returns status indicators instead of raising; parse `result["status"]` or string prefixes to handle partial failures.

## Next Steps

- [Storage Tools](./toolkit-storage-aioz.instructions.md) - AIOZ decentralized storage
- [Memory Tools](./toolkit-memory-mem0.instructions.md) - Long-term memory integration

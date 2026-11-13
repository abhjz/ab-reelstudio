---
name: schedule-posts
description: Schedules approved videos to the user's connected accounts through Zernio (upload media, validate, create scheduled posts at free slots). Use only after the user approved the specific videos.
---

# Schedule posts via Zernio

Precondition: `decisions.json` lists the videos as approved. Anything else is never posted.

1. **Find tools.** Zernio exposes many tools lazily: call `search_tools` for "create scheduled post" and "upload media" and use the exact names/arguments returned. Do not guess.
2. **Slots.** For each account take its `slots` from the profile in the profile timezone. Read already scheduled posts (`posts_list`, status scheduled) and skip taken times; roll to the next day when a day is full. If no slots are saved, propose times (optionally `analytics_get_best_time_to_post`) and ask.
3. **Upload.** Upload each mp4 with the media tools (upload link flow) and wait until the upload check reports done.
4. **Validate.** Run `validate_media` and `validate_post` (and `validate_post_length`) for the target platform. Fix caption length or format issues, never silently trim meaning.
5. **Confirm once.** Show a table: video → account → date/time → caption start. Wait for a clear yes (the earlier approval was of the video; this confirms the time and account).
6. **Create.** `posts_create` with a scheduled time and the correct `account_id`. Never omit the schedule time (that publishes immediately). Platform extras (for example TikTok privacy level) come from the tool schema; use the most restrictive sensible default unless the profile says otherwise.
7. **Report.** Post id, account, local time per video. On failure use `posts_list_failed` / `posts_retry` once, then report.

Never send tokens, account ids or personal data anywhere except Zernio calls.

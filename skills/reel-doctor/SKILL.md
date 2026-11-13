---
name: reel-doctor
description: Full setup check for Ab ReelStudio - verifies and helps install everything the pipeline can use (Zernio, Chrome + Gemini Pro tools, Higgsfield, Tarteel for Quran reels, local tools, video styles, podcast engine). Run during setup and any time something fails.
---

# Reel doctor

Produce ONE status table (item, status, how to fix) and then offer to fix what is missing, one item at a time, with the user's consent. Never install silently. The user does all sign-ins.

## 1. Local tools
Run `bash ${CLAUDE_PLUGIN_ROOT}/scripts/doctor.sh`. Missing items map to:
- `ffmpeg`, `node`, `python3`, `git`: tell the user how to install for their OS (they run it).
- `pillow/numpy`: `bash ${CLAUDE_PLUGIN_ROOT}/scripts/install-styles.sh render-tools`
- `yt-dlp`, whisper: `... install-styles.sh source-tools`
- video skills: `... install-styles.sh hyperframes|remotion|lemo-opuscar|onetake|clawd`
- podcast editing engine (majed-video): `... install-styles.sh podcast-engine`

## 2. Connections (check the tools available in this session)
| Item | How to detect | If missing |
|---|---|---|
| **Zernio** (required for scheduling) | tools like `accounts_list`, `posts_create` | Create an account at zernio.com, connect social accounts there, then `/mcp` -> sign in to **zernio** |
| **Claude in Chrome** (needed for Gemini tools) | `mcp__claude-in-chrome__*` tools | Install the Claude in Chrome extension and connect it |
| **Gemini Pro** in Chrome | open `aistudio.google.com` and `flow.google.com`; signed in? | The user signs in; without a Gemini Pro plan the AI voice/clips are skipped |
| **Higgsfield** (optional) | tools like `generate_video`, `generate_image` | Add the Higgsfield connector and sign in via `/mcp` |
| **Tarteel** (Quran reels) | tools like `ayah_search`, `play_ayahs`, `search_ayahs_text`, `list_reciters` | Add the Tarteel connector from the connectors directory (search "Tarteel"), sign in via `/mcp` |

Only check what the profile says the user wants (`generators`, `quran`), but always report Zernio.

## 3. Profile
Check `.ab-reelstudio/profile.json`: accounts present, timezone, language, voice method, rules, enabled styles. Offer `/reel-setup` for gaps.

## 4. Report
Print the table. End with the single next fix to do, then repeat until everything the user wants is green. Re-run the table after each fix.

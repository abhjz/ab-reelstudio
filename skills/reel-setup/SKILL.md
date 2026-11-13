---
name: reel-setup
description: One-time (re-runnable) onboarding for ab-reelstudio - connects Zernio, lets the user pick accounts, language, niche, voice method, rules and posting slots, then saves a local profile. Use when no profile exists or the user wants to change settings.
---

# Reel setup

The profile lives in the USER'S project at `.ab-reelstudio/profile.json`. It is never part of the plugin repo. Add `.ab-reelstudio/` to the project's `.gitignore`.

## Steps

### 1. Connect Zernio
The plugin ships a Zernio MCP server (`https://mcp.zernio.com/mcp`, OAuth). Check that Zernio tools exist (for example `accounts_list`, `posts_create`, possibly prefixed `mcp__zernio__`).
- Missing or unauthorized → tell the user to sign in to the `zernio` server through `/mcp` (the user does the sign-in; never ask for tokens or codes in chat) and wait.
- Several Zernio MCP servers present (multiple Zernio accounts) → ask which one to use.

### 2. Accounts
Call `accounts_list`. Show platform + username only. Ask which accounts to post to and give each a short label (for example "main", "second").
For each account ask what it is for, in the user's words (niche, language, style). Save as `accounts[]`: `{label, platform, accountId, purpose, languages, slots}`. Account ids stay local.

### 3. Defaults (AskUserQuestion, skip what is obvious)
- Language and dialect for narration/captions.
- Tone (educational, funny, calm, news...).
- Target length (default 30-45s).
- Voice method: record own voice / use an installed TTS / no voice (captions + music).
- Music: allowed or never. SFX: allowed or never.
- Colors: brand colors for captions, hook cards and graphics (base / support / accent hex)? Or pick from the `palette-603010` book (offer 2-3 that fit the niche, hex with roles), or choose per video. Save as `palette` and `paletteMode` (`brand` | `book` | `per-video`).
- Branding: watermark text or handle? Mid-video "follow" ask? End CTA wording?
- Timezone and daily posting slots per account (for example 13:00, 18:00).
- Checkpoint: approve script hooks / clip picks before rendering (default yes), or only the final videos?
- 3-second teaser of the strongest moment on clips (default no)?
- When the input is a podcast/video link: confirm they will only use content they own or have permission to clip.
Free-text rules go to `rules[]` verbatim (for example "no sound effects"). Rules override every default.

### 4. Styles
Run the `install-styles` skill: it checks which styles are installed and offers to install the missing ones from their official sources, with licence notes. Never install anything without a yes. Save `enabledStyles[]` and `styleMode`: `fixed:<name>` | `rotate` | `ask-each-time`.

### 4b. Quran reels (optional)
Ask: "Do you want Quran recitation reels?" If yes, set `quran: true` and check the Tarteel connector (see `reel-doctor`). Ask which account should receive them and the posting slots.

### 5. AI generators (ask, optional)
AskUserQuestion: "Which AI generation tools do you have?" (multi-select)
- **Gemini Pro** → enables Google Flow (Veo clips), Nano Banana (images) and AI Studio (speech) through the user's own Chrome. Ask which of the three to use. The user signs in themselves.
- **Higgsfield** → check for its connector tools; if missing, tell the user to add and sign in through `/mcp`.
- **None** → code-drawn styles only.
Save under `generators` (details in the `ai-generators` skill).

### 5b. Full check
Run the `reel-doctor` skill now and fix every red item the user wants (Zernio, Chrome + Gemini sign-in, Higgsfield, Tarteel, local tools, styles, podcast engine). Setup is not finished until the table is green for what the user chose.

### 6. Save
Write the JSON:

```json
{
  "version": 1,
  "timezone": "Region/City",
  "language": "...", "tone": "...", "defaultLengthSec": 40,
  "voice": {"method": "own|tts|none", "notes": ""},
  "rules": ["..."],
  "palette": {"base": "#062C30", "support": "#E5D4B8", "accent": "#FF4E00"}, "paletteMode": "book",
  "accounts": [{"label":"main","platform":"tiktok","accountId":"...","purpose":"...","slots":["13:00","18:00"]}],
  "generators": {"gemini": {"enabled": false, "flow": false, "nanoBanana": false, "aiStudioTts": false}, "higgsfield": {"enabled": false}},
  "enabledStyles": ["..."], "styleMode": "rotate",
  "checkpoint": true, "teaser": false, "quran": false
}
```

Confirm with a short summary and tell the user they can now run `/reel <topic>`.

---
name: ai-generators
description: Optional AI generation for reels - Google Flow (Veo clips), Nano Banana images, AI Studio speech via the user's Gemini Pro in Chrome, or Higgsfield via its connector. Use when the profile enables a generator or the user asks for AI footage, images or voice.
---

# AI generators (optional)

Profile field: `generators`: `{ "gemini": {"enabled": true, "flow": true, "nanoBanana": true, "aiStudioTts": true}, "higgsfield": {"enabled": false} }`. Setup fills it by asking the user (see `reel-setup`).

## Google (Gemini Pro subscription)
Used through the user's own **Chrome** (claude-in-chrome tools), signed in by the user. Never look for or use API keys on disk, never click Upgrade/Opt-in/purchase prompts, and stop on quota or sign-in errors (skip the clip, tell the user).
- **Google Flow** (flow.google): generate short Veo clips (hook or B-roll, about 8 s). One clip per video unless the user wants more. Download the mp4 into `<run>/assets/`.
- **Nano Banana** (Gemini image generation): make objects/backgrounds. Prompt for a plain white background when you need cutouts, then remove the background locally.
- **AI Studio** (aistudio.google.com, generate speech): narration in the profile language/dialect. Style prompt states dialect, pace and tone. Download the WAV, then get word timings by transcribing it.
Ask for download permission once per session; keep file names predictable.

## Higgsfield
Used through its connector tools (look for tools named like `generate_video`, `generate_image`, `generate_audio`). If absent, tell the user to add the Higgsfield connector and sign in through `/mcp`. Check balance/credits before big jobs and show the quote when the tool provides one.

## Rules
- Generated clips supplement the chosen style (hook clip, B-roll, voice); the style skill still assembles and renders the final video.
- Profile `rules[]` still win (for example "no music").
- Never generate real people's likeness without the user's explicit instruction and rights; no deceptive content.
- Keep a note of each generated asset (tool, prompt) in `<run>/assets/manifest.json` so the user can see what was AI-made.

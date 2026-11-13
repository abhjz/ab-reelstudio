<p align="center"><img src="assets/hero.svg" alt="Ab ReelStudio" width="100%"></p>

# 🎬 Ab ReelStudio — a plugin for Claude Code

**Type a topic. Get finished reels scheduled to your accounts.**

Sonnet writes the script, Opus builds the video with the video skills you have installed, you approve, then it is scheduled to TikTok, Instagram, YouTube and more through Zernio. **Nothing is posted without your approval.**

> 🎨 **New in 0.5.0: [color palettes](#-colors-603010-palettes-new-in-050).** Nine tested 60/30/10 palettes + a contrast checker, so your captions, hook cards and graphics always look good and stay readable.

🇸🇦 [النسخة العربية](README.md) · Free · MIT · Any topic: coffee, science, Quran, FPV, anything

---

<p align="center"><img src="assets/pipeline.svg" alt="From topic to scheduled post" width="100%"></p>

## 👀 Examples generated with the plugin

All made with the same steps: topic → script → video → approval → scheduling. (Short silent previews; the real videos are 30–45 s with voice.)

| ☕ Moka pot | ☕ AeroPress | 🌙 Mushaf | 🌙 Crescent |
|:--:|:--:|:--:|:--:|
| <img src="assets/example-coffee-moka.gif" width="170"> | <img src="assets/example-coffee-aeropress.gif" width="170"> | <img src="assets/example-quran-mushaf.gif" width="170"> | <img src="assets/example-quran-moon.gif" width="170"> |
| dark style, code-drawn | dark style, live counters | recitation, verse by verse | recitation + translation |

<p align="center"><img src="assets/examples-strip.jpg" alt="Five videos made with the plugin" width="100%"></p>

> 💡 The examples are coffee and Quran only because those are what was tried first. **The topic is yours**: science, tech, sport, cooking, anything.

## ⚠️ Before you start: you need a Zernio account

Scheduling goes through **[Zernio](https://zernio.com)**, a service that connects your accounts (TikTok, Instagram, YouTube…) and posts at the times you choose.

1. Create an account at [zernio.com](https://zernio.com).
2. Connect your social accounts in the Zernio dashboard.
3. Then `/reel-setup` links Claude Code to your account (sign-in through `/mcp`, **no keys**).

Without a Zernio account the plugin can still make videos, but it **cannot schedule them**.

---

## 🚀 Start here: 3 steps

| | Step | Command |
|---|---|---|
| 1️⃣ | Install the plugin (once) | terminal, below |
| 2️⃣ | Setup: connect Zernio, accounts, styles | `/reel-setup` |
| 3️⃣ | Make your first reel | `/reel specialty coffee` |

## 1️⃣ Install: once, about a minute

**You need Claude Code installed.** Open your terminal (**Terminal** on Mac, **PowerShell** on Windows) and run:

```
claude --version
```

Got a version number? Continue. Got `command not found: claude`? Install Claude Code first from [docs.claude.com/claude-code](https://docs.claude.com/en/docs/claude-code), then come back.

Paste the commands **one at a time** (command → Enter → wait):

```
claude plugin marketplace add abhjz/ab-reelstudio
```

```
claude plugin marketplace list
```

```
claude plugin install ab-reelstudio@ab-reelstudio
```

- ✅ **Check after the first command:** the second one (`marketplace list`) **must show `ab-reelstudio`**. If not, run the first command again (the connection may have dropped).
- 🔁 **Restart `claude`** after installing, or the commands will not appear in the session.
- 🏷️ **Two names, don't mix them up:** the add command takes the **repository** (`abhjz/ab-reelstudio`); the install command takes **plugin@marketplace** (`ab-reelstudio@ab-reelstudio`).

> 💡 **Best results:** run `claude` on **Opus 5.5**. The plugin pins Sonnet for scripts and Opus for videos by itself.

### 🔄 Turn on auto-update: don't skip this

So every new style and skill I add reaches you on its own:

In a normal terminal run `claude`, then:

```
/plugin  →  Marketplaces  →  ab-reelstudio  →  Enable auto-update
```

> ℹ️ `/plugin` is interactive and works in a **regular terminal only**, not inside the desktop app's Code tab.
> ⚠️ **Without this step you get no updates.** Auto-update is off by default for third-party marketplaces.
> 🔁 Want the latest now? `claude plugin update ab-reelstudio@ab-reelstudio`, then restart `claude`.

### 🌐 Or from claude.ai (no terminal)

Install once and it shows up on web, desktop and mobile, and keeps itself updated:

1. Open **claude.ai** → click your name → **Settings** → **Customize** → **Plugins** → **Add** → **Add marketplace**
2. Paste `abhjz/ab-reelstudio`, add it, then add **Ab ReelStudio**.
3. **Add** → **Manage marketplaces** → **⋮** → turn on **Sync automatically**.

> ☝️ Pick one way only (terminal **or** claude.ai) so you don't get duplicates.

## 2️⃣ Setup: `/reel-setup` (first time only)

Inside `claude`:

```
/reel-setup
```

It asks one question at a time:

1. **Connect Zernio.** The plugin ships the Zernio server. Type `/mcp`, pick **zernio**, sign in. **Never paste keys into the chat.**
2. **Accounts.** It lists the accounts connected to Zernio (TikTok, Instagram, YouTube…). You choose where videos go and describe each account's content.
3. **Your taste.** Language and dialect, tone, length, voice (your own / AI / none), music or not, sound effects or not, watermark, posting times, and **colors** (your brand colors, or a tested palette).
4. **AI tools.** Do you have **Gemini Pro** (Google Flow, Nano Banana, AI Studio through your own Chrome) or **Higgsfield**? Or neither?
5. **Styles.** It checks what is installed, lists what is missing, and installs it with your OK (details below).

Everything you say stays **on your machine** (`.ab-reelstudio/profile.json`).

## 3️⃣ Make your first reel

```
/reel specialty coffee
```

| Step | Who | What happens |
|---|---|---|
| 📝 Script (optional) | **Sonnet** | writes it from a topic, checks yours, or picks the best moments from a podcast |
| 🎞️ Video | **Opus** | builds the video with the chosen style's skill and checks it (frozen frames, audio, cut-off text) |
| 👀 Review | you | a page with every video, script, caption and time slot; pick **Approve / Change / Reject** |
| 📅 Schedule | Zernio | only after you approve: uploads, validates, schedules at your times |

## 🧭 5 ways to start: the script is optional

| You have | Type | What happens |
|---|---|---|
| **Just a topic** | `/reel specialty coffee` | Sonnet writes the script → Opus builds the video |
| **Your own script** | `/reel --script "your text"` | It only checks it (length, hook, caption) and **never changes a word** without your OK |
| **A podcast or video link** | `/reel https://…` or `/reel --from video.mp4` | **No script**: rights check → download → transcript → Sonnet picks the best moments → Opus cuts them, adds captions and a hook |
| **A folder of clips** | `/reel --from ./my-clips` | **No script**: cuts to the beat, vertical |
| **Quran recitation** | `/reel --quran 93:1-11 --reciter <name>` | Text and audio from the **Tarteel** connector, verse by verse, **no music or effects** |

**Options for any path:** `--teaser` (3 seconds of the strongest moment up front) · `--ai` (AI clips) · `--voice own|tts|none` · `--no-checkpoint` (no approval before rendering) · `--count 3`.

> ⚠️ **Links:** the plugin always asks "do you own this content or have permission?". If not, it stops. It never bypasses protections or paywalls.

## 🎁 Ready-made templates inside the plugin

| Template | What it is |
|---|---|
| `templates/explainer` | step-by-step explainers (for example brewing): **dark** with a code-drawn SVG and live counters, or **light** with real photo cutouts you make with Nano Banana plus a Flow clip |
| `templates/quran` | three calm Quran looks: night sky, mushaf page, crescent that reacts to the audio; `build_quran.py` assembles audio and verses from Tarteel |

> Templates are code only (no photos or clips) and contain no account names: the watermark is optional and empty by default.

## 🩺 Full setup check: `/reel-doctor`

`/reel-setup` runs it for you and you can run it any time. One table of everything the plugin can use, with fixes offered (only with your OK):

| Item | What it checks |
|---|---|
| **Zernio** | connection and accounts (required for scheduling) |
| **Claude in Chrome** + **Gemini Pro** | Google Flow (Veo), Nano Banana, AI Studio voice |
| **Higgsfield** | optional |
| **Tarteel** | for Quran reels |
| Local tools | ffmpeg · Node · Python · pillow · yt-dlp · Whisper |
| Styles | HyperFrames · Remotion · Lemo-Opuscar · onetake · Clawd |
| Podcast engine | `majed-video` (MIT) for cutting podcasts with Arabic captions and hooks |

## 🗣️ What you can type

| You want | Type |
|---|---|
| A reel on a topic | `/reel causes of insomnia` |
| Several reels | `/reel sleep myths --count 3` |
| A specific style | `/reel gravity --style motion-graphics` |
| For one account | `/reel coffee --account main` |
| Surprise me | `/reel surprise me` |
| From a podcast | `/reel https://…` |
| Your own script | `/reel --script "…"` |
| Change settings | `/reel-setup` |
| Install styles | `/reel-install-styles` |
| Check everything | `/reel-doctor` |
| Quran | `/reel --quran 94 --reciter <name>` |

## 🧩 What's inside the plugin

**The plugin itself** (made by us, MIT):

| Type | Name | What it does |
|---|---|---|
| 🤖 Agent | `script-writer` (Sonnet 5.5) | writes the script: hook, beats, narration, caption, hashtags |
| 🤖 Agent | `video-producer` (Opus 5.5) | builds the video with the style's skill and checks it |
| 🛠️ Skill | `reel-setup` | setup: Zernio, accounts, taste, rules |
| 🛠️ Skill | `reel-pipeline` | detects the input type and runs the steps in order |
| 🛠️ Skill | `quran-reels` | verse-by-verse recitation from Tarteel, no music |
| 🛠️ Skill | `reel-doctor` | checks every setting and fixes it with your OK |
| 🛠️ Skill | `source-reels` | reels from a podcast, video or folder of clips, no script |
| 🛠️ Skill | `video-styles` | the style catalog and when to pick each |
| 🛠️ Skill | `install-styles` | checks and installs video skills from their sources |
| 🛠️ Skill | `ai-generators` | Google Flow / Nano Banana / AI Studio / Higgsfield |
| 🛠️ Skill | `palette-603010` | 9 tested 60/30/10 color palettes + contrast checker for captions and graphics |
| 🛠️ Skill | `review-gallery` | review page: approve / change / reject |
| 🛠️ Skill | `schedule-posts` | uploads, validates, schedules on Zernio |
| ⌨️ Commands | `/reel` · `/reel-setup` · `/reel-install-styles` · `/reel-doctor` | |
| 🔌 Connection | Zernio MCP server | `https://mcp.zernio.com/mcp` |

## 🎨 Colors: 60/30/10 palettes (new in 0.5.0)

**The problem:** good reels look professional because their colors work together. Random colors look amateur, and light text on a light background is unreadable.

**The fix:** the plugin bundles the **`palette-603010`** skill: nine tested palettes that follow the 60/30/10 rule.

| Share | Role | What it colors in a reel |
|---|---|---|
| **60%** | Base | backgrounds, plates behind captions, large surfaces: sets the mood |
| **30%** | Support | main text, panels, the subject |
| **10%** | Accent | **ONE** focal thing: a hook word, the call-to-action, a progress bar |

<p align="center"><img src="assets/palettes.png" alt="The nine 60/30/10 palettes" width="100%"></p>

| Palette | Mood | 60% base | 30% support | 10% accent |
|---|---|---|---|---|
| **Sky Fresh** | light, clean, skincare | `#52C5FF` | `#FFFFFF` | `#FF1088` |
| **Petrol Gaming** | dark, premium, gaming | `#062C30` | `#E5D4B8` | `#FF4E00` |
| **Monochrome Brown** | warm, classic, fashion | `#3D231A` | `#F3EBDD` | `#00F0FF` |
| **Teal Brand** | dark, corporate-bold | `#0B434C` | `#FFFFFF` | `#FF5533` |
| **Midnight Neon** | dark, tech, games | `#0A0A0A` | `#FFFFFF` | `#55FF00` |
| **Navy Idea** | dark, serious, marketing | `#031326` | `#FFFFFF` | `#D100D1` |
| **Mauve Loud** | warm, bold, playful | `#913768` | `#C29A74` | `#FDD001` |
| **Olive Standout** | warm, natural, earthy | `#778A3F` | `#6E4B2C` | `#F16619` |
| **Brick Hook** | warm, confident | `#C15B46` | `#ABA6A3` | `#45DBE1` |

### How to use it
1. **Once, in `/reel-setup`:** give your brand colors (hex) or pick a palette. It offers 2–3 that fit your niche. This is saved in your profile as `palette`.
2. **Per reel, in plain words:** "Which colors for a coffee reel?", "Use Petrol Gaming for this one", "Same palette as last time, change only the accent". The skill also activates by itself whenever you ask about colors.
3. **Automatic:** the `video-producer` applies the palette while it builds the video, and the review page shows each video's color swatches.

### What it does for you
- **Graphics only, never your footage.** Captions, hook cards, lower thirds, progress bars and animated graphics follow the palette. Your own clips are never recolored.
- **Captions are contrast-checked.** Text over video must reach 4.5:1, otherwise the producer adds a plate or outline behind it.
- **Series trick:** keep base and support fixed, change only the accent per episode, and the whole channel looks consistent.
- **Your brand wins.** If you set colors, they are used; the book is only for choosing, fixing contrast and picking an accent.

### Pairing rules in 30 seconds
- The accent is the **opposite hue** of the base (blue↔pink, teal↔orange, brown↔cyan, navy↔purple).
- **Bright bases** (sky blue, yellow, neon green) can't carry white text: use near-black or the darkest palette color.
- **Neon accents** only on dark bases; on white or beige they wash out.
- Don't spread the accent: if it appears everywhere, nothing is the focal point.
- Contrast numbers: **4.5 or more** = body text OK · **3 to 4.5** = big bold headlines only · **under 3** = shapes and glows only, never text. Check any pair yourself: `python3 skills/palette-603010/scripts/contrast.py "#FFFFFF" "#062C30"`.

## 🎨 Styles and third-party skills

**A style is how the video gets drawn.** The plugin doesn't draw by itself; it drives skills made by other people that you install. **These skills are not ours.** Each has its own author and licence. The plugin **installs them from their official source** after showing you the licence (`/reel-install-styles`) and never copies their code.

| Style | Skill / source | Good for | Licence |
|---|---|---|---|
| ✨ **Motion graphics** (default) | [HyperFrames](https://github.com/heygen-com/hyperframes) by HeyGen | explainers, steps, numbers, captions, any topic | Apache-2.0 ✅ |
| ⚛️ **React-coded** | [Remotion skills](https://github.com/remotion-dev/skills) | data-driven videos and series | companies may need a paid licence ⚠️ |
| 🎞️ **Cinematic film** | [Lemo-Opuscar](https://github.com/lemomo-ai/lemo-opuscar) by LemoLab | stories, documentary, art styles (oil, watercolor, ukiyo-e); slow and token-heavy | demo films CC BY 4.0 |
| 🎥 **One take** | [onetake](https://github.com/feitangyuan/onetake) | teasers and launches from screenshots | **PolyForm Noncommercial: not for monetized accounts** ⛔ |
| 🖌️ **Brush animation** | [Clawd / ClaudeAnimationBase](https://github.com/JohnHeibel/ClaudeAnimationBase) | stories with a cartoon character | MIT |
| 🎙️ **Podcast engine** | [majed-video](https://github.com/majedphotos/video-ad-editor) by majedphotos | cutting podcasts and interviews with Arabic captions and hook cards | MIT |
| 🎬 **Cut from your footage** | any editing skill you have, or ffmpeg | podcasts, interviews, clips you own | — |
| 🛟 **Fallback** | ffmpeg | when nothing is installed | — |

**How does it choose?** Numbers/steps/explainers → motion graphics · story and mood → cinematic · your footage → cut. Force one with `/reel topic --style motion-graphics`. Choose "rotate" in setup and it changes style on every video.

### 🤖 AI generation tools (optional)

Setup asks: do you have **Gemini Pro**? **Higgsfield**?

| Tool | What it does | How |
|---|---|---|
| **Google Flow** (Veo) | short 8 s clips for hooks or B-roll | through your own Chrome, you sign in |
| **Nano Banana** | images and objects | same |
| **AI Studio** | narration in your dialect | same |
| **Higgsfield** | video, images, audio | through the Higgsfield connector (`/mcp`) |

No API keys are used, it never clicks Upgrade, and it stops when your quota runs out.

## 🧰 If something goes wrong

- **No `/reel` commands?** Restart `claude` and check that `claude plugin list` shows `ab-reelstudio`.
- **`Failed to add marketplace`?** Don't continue. Run `claude plugin marketplace list`; if `ab-reelstudio` is missing, run the add command again.
- **Zernio not working?** Type `/mcp` and make sure **zernio** is connected. If you see "Couldn't reach", remove it and add it again.
- **Want the latest version now?** `claude plugin update ab-reelstudio@ab-reelstudio`
- **Want to remove it?** `claude plugin uninstall ab-reelstudio@ab-reelstudio`
- ☝️ **Install it one way only** so you don't get duplicates.

## 🔒 Requirements and privacy

**Requirements:** Claude Code · **a Zernio account (required for scheduling)** · Node 22+ · ffmpeg · at least one style skill (`/reel-install-styles` installs them).

**Privacy:** your settings, account ids and videos stay in your project folder (`.ab-reelstudio/` and `ab-reelstudio-runs/`, both git-ignored). Nothing personal is in this repo. Nothing is posted or scheduled without your approval of **that video**.

## 📜 License

MIT: use, modify and share freely. Style skills have their own licences.

---
name: video-styles
description: Catalog of the video styles ab-reelstudio can drive, how to detect which video skills are installed, which style fits which topic, licence cautions and fallbacks. Used by setup, script-writer routing and video-producer.
---

# Video style catalog

ab-reelstudio bundles NO third-party video skills. It drives whichever of these the user has installed. Detect by checking the available skills list (and the Skill tool) for the skill names below. Show missing ones with the install hint; install only with the user's consent.

| Style id | Skill to invoke | Best for | Licence / caution | Install hint |
|---|---|---|---|---|
| `motion-graphics` | `hyperframes` (+ `hyperframes-registry`, `media-use`) | Explainers, step-by-step, numbers, charts, captions, any topic. **Default and fallback.** | Apache-2.0 | `claude plugin marketplace add heygen-com/hyperframes` then `claude plugin install hyperframes@hyperframes` |
| `remotion` | `remotion-best-practices` | React-coded videos, data-driven series | Remotion licence applies to companies; check `remotion-license` | see Remotion docs |
| `cinematic-film` | `lemo-opuscar` | Story, documentary feel, art styles (oil, watercolor, ukiyo-e...). Slow, token-heavy. | Library demos CC BY 4.0; credit if reusing | `claude plugin marketplace add lemomo-ai/lemo-opuscar` then `claude plugin install lemo-opuscar@lemolab` |
| `one-take` | `onetake` | Launch/teaser clips from screenshots | **PolyForm Noncommercial. Do NOT use for monetized or business accounts.** Ask the user to confirm non-commercial use every time. | `git clone https://github.com/feitangyuan/onetake.git ~/.claude/skills/onetake` |
| `style-episode` | `style-sampling` | A known episode format (collage, finance, science, 3D brand, true crime) on any topic | follows HyperFrames | via HyperFrames |
| `reverse-copy` | `reverse-any-video` | Rebuild a reference video the user owns/has rights to | Only with rights to the source | via HyperFrames |
| `footage-cut` | the `source-reels` skill, plus any installed editing skill (for example `podcast-video`, `montage-video`, `video-ad-editor`) or plain ffmpeg | The user supplies footage (podcast, interview, clips) and wants reels cut from it | Only footage the user has rights to | n/a |
| `ai-footage` | `ai-generators` skill | Real-looking footage/images/voice: Google Flow (Veo), Nano Banana, AI Studio TTS, or Higgsfield. Combine with any style above as B-roll or hook clips. | Needs the user's own paid account; respect quotas | see `ai-generators` |
| `ffmpeg-basic` | none | Absolute fallback: images/clips + captions + audio | none | ffmpeg |

## Choosing a style (when mode is ask/rotate/auto)
- Numbers, steps, tutorials, product → `motion-graphics`
- Story / emotional / art direction → `cinematic-film`
- Abstract concept or history → `style-episode` or AI footage (see `ai-generators`)
- User footage given → `footage-cut`
- Series of N videos → rotate through enabled styles, never the same style twice in a row.

## Rules for the producer
1. Invoke the chosen skill with the Skill tool and follow its own contract.
2. If it is missing: fall back to `motion-graphics`, then `ffmpeg-basic`. Tell the user which fallback was used.
3. Profile `rules[]` always override a style's defaults (music, SFX, branding, voice).
4. Respect licence cautions above before rendering.

## Adding a style
Add a row here (id, skill name, best for, licence, install hint). No other code change is needed.

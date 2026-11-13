#!/usr/bin/env bash
# Local tool check for Ab ReelStudio. Prints [ok]/[miss] lines; never installs anything.
have() { command -v "$1" >/dev/null 2>&1; }
row() { printf "  %-6s %-22s %s\n" "$1" "$2" "$3"; }
chk() { if "$@" >/dev/null 2>&1; then return 0; else return 1; fi; }

echo "Local tools"
have node    && row "[ok]" "node" "$(node -v)" || row "[miss]" "node" "install Node 22+ (nodejs.org)"
have ffmpeg  && row "[ok]" "ffmpeg" "" || row "[miss]" "ffmpeg" "brew install ffmpeg (or ffmpeg.org)"
have ffprobe && row "[ok]" "ffprobe" "" || row "[miss]" "ffprobe" "comes with ffmpeg"
have python3 && row "[ok]" "python3" "$(python3 -V 2>&1)" || row "[miss]" "python3" "install Python 3.11+"
have git     && row "[ok]" "git" "" || row "[miss]" "git" "install git"
have claude  && row "[ok]" "claude CLI" "" || row "[miss]" "claude CLI" "install Claude Code"
python3 -c "import PIL, numpy" 2>/dev/null && row "[ok]" "pillow + numpy" "(background cutouts, frame checks)" || row "[miss]" "pillow + numpy" "install-styles.sh render-tools"
have yt-dlp  && row "[ok]" "yt-dlp" "(podcast links)" || (python3 -m yt_dlp --version >/dev/null 2>&1 && row "[ok]" "yt-dlp" "(python module)" || row "[miss]" "yt-dlp" "install-styles.sh source-tools")
if python3 -c "import mlx_whisper" 2>/dev/null; then row "[ok]" "mlx-whisper" "(transcripts)"
elif python3 -c "import faster_whisper" 2>/dev/null; then row "[ok]" "faster-whisper" "(transcripts)"
else row "[miss]" "whisper" "install-styles.sh source-tools"; fi
if have npx && (cd "${TMPDIR:-/tmp}" && node -e "require.resolve('puppeteer-core')" >/dev/null 2>&1); then row "[ok]" "puppeteer-core" ""; else row "[info]" "puppeteer-core" "only for custom HTML/SVG renders: npm i puppeteer-core in the run folder"; fi

echo; echo "Installed video skills / plugins"
found() { { find "$HOME/.claude/plugins/cache" -maxdepth 3 2>/dev/null; ls "${CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}" 2>/dev/null; } | grep -qi "$1"; }
for s in hyperframes remotion-best-practices lemo-opuscar onetake majed-video; do
  found "$s" && row "[ok]" "$s" "" || row "[miss]" "$s" "install-styles.sh <target>"
done
{ [ -d "${CLAWD_DIR:-$HOME/ClaudeAnimationBase}" ] || [ -d "$HOME/Documents/Claude/ClaudeAnimationBase" ]; } && row "[ok]" "Clawd animation" "" || row "[miss]" "Clawd animation" "install-styles.sh clawd"

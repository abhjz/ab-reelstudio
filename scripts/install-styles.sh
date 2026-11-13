#!/usr/bin/env bash
# Installs third-party video skills from their official sources.
# Usage: install-styles.sh [all|hyperframes|remotion|lemo-opuscar|onetake|clawd|check]...
# Nothing is copied from this repo: each skill comes from its own upstream, with its own licence.
set -u
SKILLS_DIR="${CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}"
have() { command -v "$1" >/dev/null 2>&1; }
ok()   { echo "  [ok]   $*"; }
warn() { echo "  [warn] $*"; }

prereqs() {
  echo "Prerequisites"
  have node   && ok "node $(node -v)" || warn "Node 22+ missing"
  have ffmpeg && ok "ffmpeg" || warn "ffmpeg missing (brew install ffmpeg)"
  have git    && ok "git" || warn "git missing"
  have claude && ok "claude CLI" || warn "claude CLI missing"
}

i_hyperframes() { echo "HyperFrames (Apache-2.0)"; claude plugin marketplace add heygen-com/hyperframes && claude plugin install hyperframes@hyperframes; }
i_remotion()    { echo "Remotion skills (company licence applies, see remotion.dev/docs/license)"; npx --yes skills add remotion-dev/skills; }
i_lemo()        { echo "Lemo-Opuscar (demo films CC BY 4.0)"; claude plugin marketplace add lemomo-ai/lemo-opuscar && claude plugin install lemo-opuscar@lemolab; }
i_onetake()     {
  echo "onetake (PolyForm Noncommercial - NOT for monetized/business use)"
  [ -d "$SKILLS_DIR/onetake" ] && { ok "already installed"; return; }
  git clone https://github.com/feitangyuan/onetake.git "$SKILLS_DIR/onetake"
  warn "needs python3 + playwright: pip install playwright && playwright install chromium"
}
i_clawd()       {
  echo "Clawd Animation (MIT) - a project, not a skill"
  local d="${CLAWD_DIR:-$HOME/ClaudeAnimationBase}"
  [ -d "$d" ] && { ok "already at $d"; return; }
  git clone https://github.com/JohnHeibel/ClaudeAnimationBase.git "$d" && (cd "$d" && npm install)
  warn "read $d/ANIMATION_GUIDE.md first"
}

check() {
  prereqs; echo; echo "Installed?"
  for s in hyperframes remotion-best-practices lemo-opuscar onetake; do
    if { find "$HOME/.claude/plugins/cache" -maxdepth 3 2>/dev/null; ls "$SKILLS_DIR" 2>/dev/null; } | grep -qi "$s"; then ok "$s"; else warn "$s not found"; fi
  done
}

[ $# -eq 0 ] && set -- check
for t in "$@"; do
  case "$t" in
    check) check;;
    all) prereqs; i_hyperframes; i_remotion; i_lemo; i_onetake; i_clawd;;
    hyperframes) i_hyperframes;; remotion) i_remotion;; lemo-opuscar) i_lemo;;
    onetake) i_onetake;; clawd) i_clawd;;
    *) echo "unknown: $t"; exit 2;;
  esac
done
echo; echo "Restart Claude Code so new skills load."

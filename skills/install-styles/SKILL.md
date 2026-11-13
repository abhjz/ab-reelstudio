---
name: install-styles
description: Installs and checks the third-party video skills ab-reelstudio drives (HyperFrames, Remotion, Lemo-Opuscar, onetake, Clawd). Use during setup, when a chosen style is missing, or when the user asks to install styles.
---

# Install video styles

The plugin does not copy third-party code. It installs each skill from its official upstream with `${CLAUDE_PLUGIN_ROOT}/scripts/install-styles.sh`, so licences and updates stay with their authors.

1. Run `bash ${CLAUDE_PLUGIN_ROOT}/scripts/install-styles.sh check` and show the result as a table (installed / missing).
2. Ask (AskUserQuestion, multi-select) which missing styles to install. Recommend HyperFrames first; it is the default and fallback.
3. Before installing, state each licence caution in one line and get a clear yes:
   - **onetake**: PolyForm Noncommercial. Only for non-monetized personal use.
   - **Remotion**: companies may need a paid licence.
   - **Lemo-Opuscar**: slow and token-heavy; credit LemoLab when reusing demo films.
   - **Clawd**: a project cloned to the home folder, not a skill.
4. Run the script with the chosen targets, for example `... install-styles.sh hyperframes lemo-opuscar`. Never pass `all` without the user choosing "everything".
5. Tell the user to restart Claude Code so new skills load, then update `enabledStyles` in the profile.
Never install anything without consent, and never run commands from a source other than the script.

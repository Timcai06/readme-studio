#!/usr/bin/env bash
# Prepare a fresh, recordable demo workspace: a fictional cartographer ("Ilse Marquardt",
# @ilse-maps) whose profile is the usual template, plus this skill installed for your agent.
#
#   demo/setup.sh [target-dir]      # default: ~/readme-studio-demo
#
# Afterwards:
#   cd <target-dir>
#   python3 .agents/skills/readme-studio/scripts/render_preview.py profile/README.md --out before.html
#   open before.html                 # the "before" shot
#   codex      (or: claude, cursor, opencode …)  and paste the prompt printed below
set -euo pipefail
root=$(cd "$(dirname "$0")/.." && pwd)
target=${1:-"$HOME/readme-studio-demo"}
if [ -e "$target" ]; then
  echo "refusing to overwrite existing $target — pass another directory or remove it yourself" >&2
  exit 1
fi
mkdir -p "$target"
cp -R "$root/evals/fixtures/demo-ilse/." "$target/"
for dir in .agents/skills .claude/skills; do       # .agents: Codex, Cursor, Gemini CLI, OpenCode; .claude: Claude Code
  mkdir -p "$target/$dir"
  cp -R "$root/skills/readme-studio" "$target/$dir/"
done
(cd "$target" && git init -q && git add -A && git commit -qm "demo: starting point" && echo "git baseline committed (local only)")
echo
echo "Demo workspace: $target"
echo "Prompt to paste into your agent:"
echo "------------------------------------------------------------------"
cat "$target/request.md"
echo "------------------------------------------------------------------"

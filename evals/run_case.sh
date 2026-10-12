#!/usr/bin/env bash
# Run one eval case with a fresh, headless agent that only knows the skill.
#
#   evals/run_case.sh <agent> <case> [workspace-dir]
#   agent: claude | codex | gemini | opencode
#   case:  newcomer | seasoned | creative | improve | demo-ilse
#
# Creates an isolated workspace (default: evals/runs/<case>-<agent>-<UTC time>),
# copies the fixture and installs the skill at project level:
#   claude   -> .claude/skills/readme-studio
#   others   -> .agents/skills/readme-studio
# The prompt is request.md verbatim. It never names the skill: whether the agent
# picks the skill up from its description is part of the test.
# Transcript: <workspace>/.eval/transcript.*  Result: files in <workspace>.
set -euo pipefail

agent=${1:?agent}; case=${2:?case}
root=$(cd "$(dirname "$0")/.." && pwd)
fixture="$root/evals/fixtures/$case"
[ -d "$fixture" ] || { echo "no fixture $case" >&2; exit 2; }
ws=${3:-"$root/evals/runs/$case-$agent-$(date -u +%Y%m%dT%H%M%SZ)"}
mkdir -p "$ws/.eval"
cp -R "$fixture/." "$ws/"
if [ "$agent" = claude ]; then dest="$ws/.claude/skills"; else dest="$ws/.agents/skills"; fi
mkdir -p "$dest"
cp -R "$root/skills/readme-studio" "$dest/"
prompt=$(cat "$fixture/request.md")
cd "$ws"
git init -q . 2>/dev/null || true   # some agents treat the git root as the project root
start=$(date +%s)
set +e
case "$agent" in
  claude)
    # project settings only: no user hooks/plugins; tools limited to file work + python/shell basics
    claude -p "$prompt" --setting-sources project --permission-mode acceptEdits \
      --allowedTools "Read Write Edit Glob Grep Skill Bash(python3:*) Bash(mkdir:*) Bash(cp:*) Bash(ls:*) Bash(diff:*) Bash(cat:*) Bash(git diff:*) Bash(git status:*)" \
      --output-format stream-json --verbose < /dev/null > .eval/transcript.jsonl 2> .eval/stderr.txt ;;
  codex)
    # workspace-write sandbox: no network unless NET=1 -> exercises the offline fallbacks
    net="sandbox_workspace_write.network_access=false"; [ "${NET:-0}" = 1 ] && net="sandbox_workspace_write.network_access=true"
    codex exec --skip-git-repo-check --sandbox workspace-write -c "$net" --json "$prompt" \
      < /dev/null > .eval/transcript.jsonl 2> .eval/stderr.txt ;;
  gemini)
    gemini --skip-trust -p "$prompt" --approval-mode auto_edit --output-format stream-json \
      < /dev/null > .eval/transcript.jsonl 2> .eval/stderr.txt ;;
  opencode)
    opencode run --pure -m "${OPENCODE_MODEL:-opencode/big-pickle}" --format json "$prompt" < /dev/null > .eval/transcript.jsonl 2> .eval/stderr.txt ;;
  *) echo "unknown agent $agent" >&2; exit 2 ;;
esac
status=$?
echo "{\"agent\":\"$agent\",\"case\":\"$case\",\"seconds\":$(( $(date +%s) - start )),\"exit\":$status}" > .eval/meta.json
echo "$ws"

#!/usr/bin/env bash
# Does the agent load the skill for the right requests, and only those?
#   evals/trigger_test.sh codex|opencode [out.tsv]
# Each query runs in a fresh empty workspace with the skill installed in .agents/skills.
# The agent is told to only plan (read-only sandbox for codex), so nothing is built.
# "triggered" = the transcript shows SKILL.md of this skill being read / the skill tool called.
set -uo pipefail
agent=${1:?agent}
root=$(cd "$(dirname "$0")/.." && pwd)
out=${2:-/dev/stdout}
base=$(mktemp -d)
queries=(
  "yes|帮我把我的 GitHub 个人主页做得好看一点，我的用户名是 example-user（虚构，别去查）。先只说你的计划，不要动手。"
  "yes|My GitHub profile looks like every other template (badges, stats cards, snake). Can you redesign it? Just outline your plan first, don't build anything."
  "yes|I just made the repo with my username so I get a profile README. What should I put on it? Plan only."
  "yes|Audit my profile README in ./README.md and tell me what to fix. Plan only, no edits."
  "no|Fix the typo 'recieve' in the README of my Python library. Plan only."
  "no|Write the CHANGELOG entry for v2.0.0 from the merged PRs. Plan only."
  "no|Set up a Docusaurus documentation site for this repo. Plan only."
  "yes|Write a README for my CLI tool that explains installation and usage. Plan only."
  "yes|our library README is a wall of text, can you redesign it so people get it in 10 seconds? Plan only."
  "no|Build me a personal portfolio website with Next.js and Tailwind. Plan only."
  "no|Add a GitHub Actions workflow that runs pytest on every push. Plan only."
)
printf "expected\ttriggered\tquery\n" > "$out"
for item in "${queries[@]}"; do
  want=${item%%|*}; q=${item#*|}
  ws=$(mktemp -d "$base/q.XXXX")
  mkdir -p "$ws/.agents/skills" && cp -R "$root/skills/readme-studio" "$ws/.agents/skills/"
  printf "# My project\n\nA library that does things.\n" > "$ws/README.md"
  (cd "$ws" && git init -q .
   case "$agent" in
     codex) codex exec --skip-git-repo-check --sandbox read-only --json "$q" < /dev/null > t.jsonl 2>/dev/null ;;
     opencode) opencode run --pure -m "${OPENCODE_MODEL:-opencode/big-pickle}" --format json "$q" < /dev/null > t.jsonl 2>/dev/null ;;
   esac)
  if grep -q 'readme-studio/SKILL.md\|"name":"readme-studio"\|"name": "readme-studio"' "$ws/t.jsonl"; then got=yes; else got=no; fi
  printf "%s\t%s\t%s\n" "$want" "$got" "$q" >> "$out"
done
rm -rf "$base"

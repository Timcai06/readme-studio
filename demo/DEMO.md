# Demo：普通 GitHub 主页 → 个性化主页（录屏脚本）

示例人物：**Ilse Marquardt（@ilse-maps）**，虚构的地图开发者，所有账号、仓库和数据都是编的。画面里请明确标注「虚构示例人物」。演示全程在本地进行，不会访问、创建或推送任何 GitHub 账号。

## 0. 录屏前准备（不入镜）

```bash
cd ~/DEV/readme-studio
```

```bash
demo/setup.sh ~/gps-demo
```

- 会生成 `~/gps-demo`，里面有：
  - `snapshot.json`：模拟的 GitHub 公开数据导出
  - `profile/README.md`：「Hi 👋 + 徽章 + 统计卡」的旧主页
  - `request.md`：要粘贴给 Agent 的需求
  - Skill 安装在 `.agents/skills/` 和 `.claude/skills/`
- 目标目录已存在时，脚本会拒绝覆盖。重录时换一个目录名，比如 `~/gps-demo-2`。
- 先用一次 Agent，确认它已登录。这台机器上 Claude Code 的命令行登录已经过期，用它的话先执行 `claude /login`。Codex 已验证可用。

## 1. 开场：普通主页（约 20 秒）

```bash
cd ~/gps-demo
```

```bash
python3 .agents/skills/readme-studio/scripts/render_preview.py profile/README.md --out before.html && open before.html
```

画面：浅色、深色、手机三栏的「Before」。这是 GitHub 渲染接口输出的真实 HTML。

旁白要点：这是最常见的模板主页，信息量很低，换个名字就能给任何人用。

## 2. 安装 Skill（约 15 秒）

```bash
ls .agents/skills/readme-studio
```

画面：`SKILL.md`、`references/`、`scripts/`、`assets/`。

旁白要点：一个文件夹，符合开放 Agent Skills 标准。Codex、Cursor、OpenCode 从 `.agents/skills` 读取，Claude Code 从 `.claude/skills` 读取。

## 3. 让 Agent 工作（主体，2–6 分钟，可加速剪辑）

```bash
codex
```

或者用 `claude`。然后粘贴 `request.md` 的内容。提示词里**没有点 Skill 的名字**，靠描述自动触发，这一点值得在镜头里强调。

依次留意这些镜头：
1. Agent 宣布使用 readme-studio，读取 SKILL.md。
2. 读 `snapshot.json` 和旧 README，建立证据账本（evidence ledger）。
3. 提出三个视觉概念，选定一个并说明理由。我们这次的实际输出是「map margin」：等高线和河流。
4. 写生成脚本 `tools/build_assets.py`，产出浅色、深色两套 SVG。
5. 跑检查：`check_readme.py`（含 `--baseline` 对比旧版）、`svg_kit.py lint`。
6. 交付报告：做了什么、删了什么、哪些没验证。

## 4. 结果（约 30 秒）

```bash
python3 .agents/skills/readme-studio/scripts/render_preview.py profile/README.md --out after.html && open after.html
```

画面：`before.html` 和 `after.html` 左右对比，再切换浅色和深色两栏。

```bash
cat profile/.readme-studio/brief.md
```

画面：证据账本、三个候选概念、删减清单。旁白可以说「它解释了为什么这样设计」。

```bash
git status --short
```

画面：全部是本地改动（新增和修改的文件），没有提交，也没有推送。

## 5. 收尾要点（旁白）

- 它不是模板：同样的输入每次跑出的设计都不同；方法固定，结果不固定。
- 它不编造：不把语言统计当技能，fork 和教程项目不当作原创。
- 它受 GitHub 约束：规则来自对 GitHub 渲染器的实测，并用 GitHub 自己的 Markdown 接口复核。
- 发布由你决定：最后只给出发布步骤，Agent 不推送。

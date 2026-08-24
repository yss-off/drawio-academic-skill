# 基线来源与迁移记录

## 2026-08-16 初始基线

- 工程路径：`/home/yss/code/scientific_visualization_skill`
- 权威 skill 工作目录：`skill/scientific-visualization/`
- 基线来源：`/home/yss/.codex/skills/scientific-visualization/`
- 基线标识：`scientific-visualization` v1.1，`skill-author: K-Dense Inc.`
- 上游参考：https://github.com/K-Dense-AI/scientific-agent-skills/tree/main/skills/scientific-visualization
- 迁移方式：逐文件复制当前已安装副本；迁移时不修改 skill 内容。
- 安装副本状态：保持不变；本工程未同步回 Codex 运行目录。

## 初始阶段边界

只建立受版本控制的个人维护源并迁入调研、决策记录。P0 行为合同尚未冻结，因此不实现 profiler、选图、视觉 QA、CJK preflight 或 eval 新能力。

该边界记录的是初始迁移阶段。2026-08-16 用户随后授权按调研中的开源工作流先实现 P0 临时基线；当前授权与实现范围见 `management/02-p0-design-decisions.md` 的 D6。

## 基线验证

- `diff -qr`：工程内 skill 与已安装副本逐文件一致。
- helper smoke test：`scripts/*.py --help` 全部通过。
- `skill-creator/scripts/quick_validate.py`：未通过；当前 v1.1 frontmatter 含 `compatibility`，验证器允许列表不包含该字段。该问题属于迁入前基线，不在建工程阶段静默修改，待讨论 frontmatter/兼容性策略时处理。

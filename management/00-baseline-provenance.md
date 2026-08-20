# Draw.io Academic Overlay 基线来源

## 2026-08-16 初始基线

- 工程路径：`/home/yss/code/drawio_academic_skill`
- 权威 overlay 源：`skill/drawio-academic-skills/`
- 基线来源：`/home/yss/.codex/skills/drawio-academic-skills/`
- 基线标识：README 标注 repository release `2.6.0`，`evals/evals.json` 标注 `2.7.1`，CHANGELOG 含 2.7.0 与 Unreleased；版本信息存在漂移，不能据此声称唯一发布版本。
- sibling base：`/home/yss/.codex/skills/drawio/`，只读测试依赖；Node `v22.22.2`。
- 迁移方式：逐文件复制当前已安装副本，不复制 sibling base。

## 基线验证

- overlay 安装目录不是 Git 仓库，未发现本地维护源。
- 初始迁移检查曾记录 `diff -qr` 一致；随后发现已安装副本在复制点附近发生了并发更新。用户于 2026-08-16 明确同意以当前已安装副本为新基线重放第二阶段增强；处理结果见 `management/04-current-installed-baseline-rebase.md`。
- sibling base 的 `scripts/cli.js` 与 `assets/schemas/spec.schema.json` 存在。
- 当前 PATH 未发现 draw.io Desktop，可预期 PNG/PDF Desktop export 需要诚实回退到 SVG，除非后续发现其他可用安装路径。

## 授权边界

- 用户选择启动第二阶段，授权在本工程权威源内实现 overlay 临时增强。
- 未授权同步 `/home/yss/.codex/skills/drawio-academic-skills/`，未授权修改 sibling base、commit、push 或发布。

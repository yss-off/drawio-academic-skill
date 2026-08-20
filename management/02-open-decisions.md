# 第二阶段待单独确认事项

## O1 默认导出合同冲突（已解决）

原基线内部存在不一致：

- 当前 `SKILL.md` 表述为默认 editable `.drawio` + 300dpi publication `.png`，Desktop 不可用时使用 source-preserving browser-rasterized PNG；live-text SVG 仅作 preview/intermediate；
- README、`publication-overlay.md`、`academic-figure-playbook.md` 和多条 eval 仍表述为默认 `.drawio` + `.svg`，PNG 是可选 Desktop 增强。

2026-08-20，用户明确同意采用场景化合同，不再设置通用 PNG/SVG 默认值。`academic-figure-playbook.md § Academic Delivery Matrix` 现为唯一选择权威：所有类别交付 `.drawio`；`raster-publication` 要求 300ppi-effective PNG；`vector-submission` 要求 PDF 或 path-only SVG 并服从 venue 限制；`draft-preview` 使用明确标注的 live-text SVG。实现和验证见 `management/05-scenario-delivery-contract.md`。

## O2 复制点附近的已安装副本漂移（已解决）

最终复核发现 `/home/yss/.codex/skills/drawio-academic-skills/references/docs/academic-export-checklist.md` 的 mtime 为 `2026-08-16 17:48:23 +0800`，而工程复制点文件保留 `2026-08-16 13:30:11 +0800` 内容。当前已安装版新增了 browser-rasterized PNG、live-text SVG 限制、三类 artifact hash 及 DOCX/PDF embedding 检查；工程复制点仍是旧措辞。

用户已明确选择以当前已安装副本为新基线。工程源完成机械基线同步并重放第二阶段增强；`academic-export-checklist.md` 已与当前安装基线逐字一致，`SKILL.md` 与 `agents/openai.yaml` 的差异仅为本轮布局候选、参考索引和 manifest 集成。验证见 `management/04-current-installed-baseline-rebase.md`。

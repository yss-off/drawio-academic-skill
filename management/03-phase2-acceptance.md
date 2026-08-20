# 第二阶段临时增强验收

## 结论

2026-08-16，第二阶段四项临时增强在权威源 `skill/drawio-academic-skills/` 内完成：布局候选、离线参考索引、统一 figure manifest 与回归 eval。随后已按用户授权重放到当前安装版基线之上。未修改 sibling base runtime，未同步已安装 overlay。

## 自动验证

- `python skill/drawio-academic-skills/evals/smoke_test.py`：7/7 通过。
- 布局 fixture：12/12 通过；每例只生成 2–3 个候选，section order 与 `scientific_content_status: unchanged` 受检。
- known-bad manifest：10/10 均命中预期错误码。
- JSON 语法：`evals.json`、layout/manifest fixture、reference index 均通过 `python -m json.tool`。
- Python 语法：新 helper 与 smoke test 通过 `py_compile`；缓存写入 `/tmp`。
- skill 结构：skill-creator `quick_validate.py` 返回 `Skill is valid!`。
- `git diff --check`：通过。
- manifest CLI：`init` 与普通 `validate` 通过；重复输出在未给 `--force` 时按预期拒绝覆盖。

## Sibling base 兼容性

- 使用 `/home/yss/.codex/skills/drawio/scripts/cli.js` 对 overlay 的 8 个 example 和 2 个 template 执行 `--validate --strict-warnings`：10/10 退出码为 0，XML 全部通过。
- 三个既有复杂示例仅产生 base 标为 `[info]` 的长标签提示；未改变基线示例内容。
- 代表性 forward test：`system-architecture-paper.yaml` 成功生成 `.drawio`、standalone `.svg`、`.spec.yaml` 与 `.arch.json`。
- forward SVG SHA-256：`e23e772001fd558d200b08ac6cb358e2b236a2f66d6221feb8dc9ba238aedae6`。
- 以本机 Chrome 生成 `browser-rasterized` 检查图后目视复核：三层边界、节点文字、箭头和虚线关系清晰，无裁切、重叠或断连。该检查不冒充 draw.io Desktop export 或投稿合规证明。

## 安装边界证据

- 已安装 overlay 最终树哈希：`3c7e3a32d36d6c6a8b3d7d35ccf7282493e1567b0c1702f0f61e251cdc660567`。
- 已安装 overlay 最新文件 mtime：`2026-08-16 17:48:24 +0800`；早于权威源 helper 实现和 19:00 后的基线重放。安装树哈希在重放前后保持不变。
- 验收过程中只读调用 sibling base CLI；没有向 `/home/yss/.codex/skills/drawio/` 或 `/home/yss/.codex/skills/drawio-academic-skills/` 写入。

## 保留事项

复制点漂移已解决。O1 当时仍保留，后于 2026-08-20 经用户授权采用场景化交付合同解决，见 `management/05-scenario-delivery-contract.md`；正式启用仍需用户单独授权把权威源同步到已安装运行副本。

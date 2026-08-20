# 当前安装基线重放记录

## 授权与范围

2026-08-16 19:00 +0800，用户明确同意“以当前已安装版本作为新基线，重新叠加第二阶段四项增强”。本次只修改工程权威源 `skill/drawio-academic-skills/`；安装目录和 sibling base 保持只读。

重放前已把工程的 `AGENTS.md`、`.gitignore`、`management/` 与 `skill/` 完整备份到 `/tmp/drawio-academic-pre-rebase.H7rPKc/`。当前安装基线树哈希为：

`3c7e3a32d36d6c6a8b3d7d35ccf7282493e1567b0c1702f0f61e251cdc660567`

## 重放结果

- 已安装 overlay 的全部同名文件机械同步到工程源；第二阶段新增文件保留。
- 仅重放布局候选、离线参考索引、figure manifest、eval 及其入口/文档集成。
- `academic-export-checklist.md` 与当前安装基线无差异；未回退 browser-rasterized PNG、live-text SVG、artifact hash 或 DOCX/PDF embedding 规则。
- `SKILL.md` 与 `agents/openai.yaml` 的逐行差异只包含第二阶段入口、路由、候选、manifest 与完成报告集成。
- O1 在本次基线重放时仍按原样保留；后于 2026-08-20 经用户授权解决，见 `management/05-scenario-delivery-contract.md`。

## 重放后验证

- offline smoke tests：7/7 通过。
- layout fixtures：12/12 通过；known-bad manifests：10/10 命中预期错误码。
- Python `py_compile`、JSON 语法和 skill-creator `quick_validate.py` 全部通过；输出 `Skill is valid!`。
- sibling base 严格校验：8 个 example + 2 个 template，10/10 退出码 0；XML 全部通过。
- representative forward test：`.drawio`、standalone `.svg`、sidecars 和 browser-rasterized regression PNG 均生成；目视检查无裁切、重叠或断连。
- forward manifest 使用 `build --strict` 和 `validate --strict --verify-artifacts` 均为 0 errors / 0 warnings。
- forward manifest SHA-256：`ac82b9538c030d2b20def8048a1748f20a7db37a5f08959ff3d4408022832de1`。
- regression PNG SHA-256：`26bef4b6c74382c3b53c6ea7c3216b3b67f28ea067b2a526f54e03d5f4dbb033`；manifest 明确记录其为 browser-rasterized regression preview，不冒充 300dpi venue artifact。

## 剩余边界

工程尚未 commit、push、发布或安装。将权威源同步到 `/home/yss/.codex/skills/drawio-academic-skills/` 仍需单独明确授权。

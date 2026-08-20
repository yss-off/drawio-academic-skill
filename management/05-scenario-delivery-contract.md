# 场景化学术交付合同

## 决定

2026-08-20，用户同意解决 O1，不再把 PNG 或 SVG 写成所有学术任务的通用最终默认值。唯一选择权威为 `skill/drawio-academic-skills/references/docs/academic-figure-playbook.md § Academic Delivery Matrix`：

| 主交付类别 | 适用场景 | 必需主产物 |
| --- | --- | --- |
| `raster-publication` | Word、学位论文、A4、raster-first | `.drawio` + 300ppi-effective PNG |
| `vector-submission` | 期刊或 venue 要求矢量 | `.drawio` + PDF 或 path-only SVG；IEEE 只接受 PS/EPS/PDF |
| `draft-preview` | 草稿评审或出版目标未确定 | `.drawio` + 明确标注 preview/intermediate 的 live-text SVG |

`.spec.yaml`、`.arch.json` 和 figure manifest 保存在工作目录。用户额外要求的格式可以作为 companion，但一个 manifest 只记录一个主 `delivery_class`；不得把 preview 升格为出版证据。

## 实现

- `SKILL.md`、中英文 README、publication overlay、playbook、export checklist、agents 和 prompt eval 使用同一矩阵。
- manifest schema/skeleton 新增规范字段 `contract.delivery_class`；旧 planning manifest 在普通校验中得到迁移 warning，accepted/strict 必须补齐。
- strict manifest validation 要求每类匹配主产物：PNG、PDF/`text_mode: paths` SVG、或 preview SVG；所有类别仍要求 `.drawio`。
- `draft-preview` 是目标未知时的明确降级状态，不等于出版完成。
- `raster-publication` 的 browser fallback 必须走 source-preserving derivative gate；`vector-submission` 缺少合规 exporter 时标为 blocked。

## 验证

- offline smoke tests：10/10 通过，其中新增 delivery-class mismatch、matching-artifact 与旧 planning manifest 兼容回归。
- Python `py_compile`、JSON 语法和 skill-creator `quick_validate.py` 通过；输出 `Skill is valid!`。
- sibling base strict validation：8 个 example + 2 个 template，10/10 退出码 0；XML 全部通过。
- representative `draft-preview` forward test：`.drawio`、standalone SVG、sidecars、manifest 和目视检查通过。
- forward manifest `build --strict` 与 `validate --strict --verify-artifacts` 均为 0 errors / 0 warnings。
- forward manifest SHA-256：`1d8fd73869fb462adcdd67b789a5d031053614df3264e7c1a27a50d3241ed884`。

## Base 残余问题

sibling base CLI 仍输出：`academic-paper profile recommends SVG export for paper-ready vector output.` 该提示把 live-text SVG 泛化成 paper-ready vector，与新 overlay 合同不一致，但不影响转换和 XML 校验。问题属于只读 base runtime；本工程只记录，不在 overlay vendor-copy 修补。正式安装 overlay 前可独立决定是否授权修正 base 提示。

## 边界

本轮未修改 `/home/yss/.codex/skills/drawio-academic-skills/` 或 `/home/yss/.codex/skills/drawio/`，未 commit、push、发布或安装。修改前工程备份位于 `/tmp/drawio-academic-delivery-contract.nrXFaT/`。

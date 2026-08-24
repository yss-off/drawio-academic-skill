# P0 上游集成审计

> 审计日期：2026-08-16  
> 目的：固定“先采用开源基线、遇到问题再迭代”的来源与边界。本文只记录审计和取舍，不由 skill 运行时加载。

## 固定来源

| 项目 | 固定 commit | 许可证 | 本轮用途 |
|---|---|---|---|
| [`Haojae/scipilot-figure-skill`](https://github.com/Haojae/scipilot-figure-skill) | `43098ddb9e6a6d142218540c114f9ed38922fc42` | MIT，`Copyright (c) 2026 Haojae` | profiler、选图和渲染后视觉复核的工作流与接口参考 |
| [`TingxiYu/academic-figure-skill`](https://github.com/TingxiYu/academic-figure-skill) | `1df9940dd01ac939f072b12fe28d6353b79b90f9` | Apache-2.0 | figure contract、分层 QA 和 eval 结构参考 |
| [`lingzhi227/agent-research-skills`](https://github.com/lingzhi227/agent-research-skills) | `9e6c085d65e313e475e921fdfe795ac11eb7589e` | 仓库根目录未发现许可证 | 仅采用有限次“执行—看图—回改”概念；不复制代码、模板或文字 |

## 审计结论

- 不直接执行任何上游脚本；所有新增 helper 在本工程内独立实现并单独测试。
- SciPilot `profile_data.py` 会自动推荐统计图、计算 Pearson 相关并使用 `n<3`、`n<10`、缺失率 20%、跨度 100 倍等固定阈值。本工程只保留事实剖析和显式标注的可配置启发式，不让 profiler 选择检验或得出科学结论。
- SciPilot 支持 Excel/DataFrame 并依赖 Pandas/NumPy；P0 为降低依赖与解析歧义，只原生支持 UTF-8 CSV/TSV，多个文件分别处理。
- Academic Figure 的 figure contract 和 QA 分层结构可复用，但“Nature-family 默认”、固定 89/183 mm、固定字号/DPI、按数据阈值拒绝渲染等规则不能作为通用合规门槛。
- Academic Figure 的源码静态扫描 validator 依赖字符串匹配，容易把编码风格当作成图正确性。本工程将 numeric、textual、visual 证据分开，机器检查不能覆盖的项目明确标为人工/视觉复核。
- `agent-research-skills` 没有可核验许可证，因此不形成派生文件，只采用不受版权保护的抽象流程思想。

## 本轮允许落点

- `references/figure_contract.md`：本工程确认过的最小 contract 和阻塞条件。
- `scripts/profile_data.py`：只读 CSV/TSV profiler，JSON 为权威结果，Markdown 为确定性派生。
- `references/chart_selection.md`：推荐、证据、假设、备选和风险格式；不静默决定统计检验。
- `scripts/font_preflight.py`：本地字体和字符覆盖预检。
- `scripts/visual_qa.py` 与 `references/visual_review.md`：确定性布局检查加最终尺寸人工/视觉复核，最多两轮自动回改。
- `evals/`：trigger、chart-choice、known-bad 和 smoke 回归。

## 许可证处理

本轮不逐文件复制上游实现或大段文字，而是依据审计后的行为合同独立实现，因此 skill 包不混入上游源文件。若后续决定直接复制实质代码或资产，必须在复制前增加对应 LICENSE/NOTICE 与逐文件来源说明。

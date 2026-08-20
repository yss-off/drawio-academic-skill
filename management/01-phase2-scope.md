# 第二阶段临时增强范围

## 目标

在不复制 base runtime、不中断现有 YAML-first 工作流的前提下，为复杂论文示意图补齐“先比较布局—再冻结语义—最后用统一证据验收”的 overlay 闭环。

## 本轮实现

1. **Layout candidates**：复杂或歧义任务先生成 2–3 个结构明显不同的候选计划；每个候选记录适用论点、主阅读轴、分组、反馈路径、节点预算、风险和选择理由。候选是计划，不是三份最终图。
2. **Reference index**：新增小型离线索引 schema 和查询 helper；先索引 overlay 自有 MIT 示例/模板，不下载远程图库，不复制第三方图片。
3. **Figure manifest**：新增向后兼容的 overlay-local manifest builder/validator，把 contract、semantic inventory、layout、palette/font、artifacts、QA 与 provenance 汇总到一个 JSON；不修改 base schema。
4. **Evals**：新增 trigger、layout-choice、manifest validation 和 known-bad manifest cases；现有人工 prompt eval 保留。

## 明确非目标

- 不修改 base CLI、renderer、schema、theme、palette 或 shared visual-review contract。
- 不自动决定科学关系、因果方向、公式含义、统计结论或论文贡献。
- 不执行第三方代码或下载外部参考图。
- 不把候选布局、参考样例、自动验证或视觉模型判断当成投稿合规证明。

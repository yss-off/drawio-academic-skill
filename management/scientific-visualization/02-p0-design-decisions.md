# Scientific Visualization P0 设计决策记录

> 状态：P0 临时基线已授权在权威维护源中实现；尚未授权同步到已安装 skill  
> 目标：在保持现有数据诚实性、可访问性、可复现导出和期刊核验优势的前提下，为 `scientific-visualization` 增加“绘制前判断—绘制后验证—可回归评测”闭环。

## 已确认决定

### D1 第一轮范围

- 第一轮只设计和改造 `scientific-visualization` 数据绘图 skill。
- `drawio-academic-skills` 保持不变；待数据绘图 P0 闭环完成并验证后，再单独评估是否需要共享 manifest 或参考索引。
- 当前阶段只讨论、记录并冻结方案，不修改已安装 skill。

### D2 权威维护源

- 在 `/home/yss/code/scientific_visualization_skill/` 建立受 Git 管理的个人维护工程。
- `skill/scientific-visualization/` 是权威 skill 源；以当前已安装 v1.1 的逐文件副本为基线。
- 验证通过并获得用户明确授权后，才允许同步到 `/home/yss/.codex/skills/scientific-visualization/`。
- 是否向第三方上游拆分贡献，作为后续独立决定。

### D3.1 Figure contract 触发策略

- 用户已经明确科学问题或指定图型时，自动形成 contract，陈述必要假设后继续，不机械阻塞。
- 用户只提供数据并笼统要求“画一下”时，先问一个问题：这张图主要要回答什么科学问题？
- 用户要求审查已有图时，从图、数据和论文上下文反推 contract；只有发现语义冲突或关键缺口时再询问。
- contract 是绘图决策与审计记录，不是强制每次让用户填写的表单。

### D3.2 Figure contract 最小内容与阻塞条件

- 最小内容包括：科学问题、沟通目标、预期论点；数据来源、变量语义与单位、重复单位；数据变换、缺失值与排除项、不确定性定义；交付场景；多面板计划为可选项。
- contract 应优先从用户请求、数据、已有图和论文上下文中推断；可以陈述不影响结论的假设，不要求用户逐项填写表单。
- 只有下列缺口会阻塞绘图并要求确认：
  - 科学问题无法可靠推断；
  - 变量含义、单位或重复单位的歧义会改变科学解释；
  - 数据来源缺失或不可读；
  - 过滤、变换、排除或不确定性定义的歧义可能改变结论。
- 期刊、最终宽度或配色等信息缺失时不阻塞；使用明确标注为临时的通用配置，并保留后续核验项。
- 判断原则：影响科学解释的信息必须确认；只影响外观或投稿格式的信息可以暂定。

### D3.3 Profiler 职责与只读边界

- profiler 是绘图前的数据体检器，只负责读取、描述和提示风险，不替研究者清洗、处理或解释数据。
- profiler 可以报告列类型、单位信息、缺失值、取值范围、重复记录、分组样本量等可观察事实。
- profiler 可以把潜在异常值、偏态、样本不平衡等标记为“需要复核”的风险；此类标记不得表述为数据错误、科学结论或强制门槛。
- profiler 不得自动删行或删列、填补缺失值、改变类型、归一化、改写原文件或生成冒充原始数据的替代文件。
- profiler 不得自行认定异常值无效，不得推断独立重复单位，也不得选择或执行统计检验。
- 判断原则：只发现问题，不替研究者处理或解释问题。

### D3.4 Profiler P0 输入范围

- P0 原生支持二维表格形式的 CSV 和 TSV 文件。
- 可以一次接收多个文件，但分别剖析；不得自动拼接、关联或合并数据。
- 对分隔符、文本编码或表头存在会改变数据结构的歧义时，明确报告并停止该文件的剖析，不静默猜测。
- P0 不原生支持 Excel、Parquet、JSON、HDF5 或 NetCDF，也不静默转换这些格式；后续根据实际需求以独立适配器扩展。
- 设计原则：先把常见二维表格的确定性检查做稳，再扩展复杂科研数据格式。

### D3.5 Profiler 报告载体

- JSON 是带 schema 版本的权威结果，供选图、QA 和自动评测读取。
- Markdown 是由同一 JSON 确定性生成的人类可读摘要，不增加 JSON 中不存在的新判断。
- 两种报告必须来自同一剖析结果，避免内容漂移。

### D6 临时基线实施策略

- 2026-08-16 用户决定停止逐字段讨论，先以已调研开源案例的高价值结构形成可运行基线，再根据实际问题迭代。
- 采用 SciPilot 的“contract → profiler → 选图 → 渲染 → 视觉复核”主流程、Academic Figure 的 figure contract / 分层 QA / eval 结构，以及有限次 render-review loop。
- “照搬”指优先复用已验证的工作流结构和接口形态，不等于整包复制代码或接受全部规则；与本工程数据诚实性、只读、离线、拒绝隐式覆盖和期刊实时核验约束冲突的上游行为必须替换。
- P0 实现默认值不再逐项等待确认：选图输出采用“推荐、证据、假设、备选、风险”；QA 分 numeric、textual、visual 三层；自动回改最多两轮；manifest 只做向后兼容的可选扩展。
- 本轮授权只覆盖 `/home/yss/code/scientific_visualization_skill/skill/scientific-visualization/` 及其管理/评测记录；不得同步到 `/home/yss/.codex/skills/scientific-visualization/`，不得提交或推送。

### D7 Frontmatter 兼容性迁移

- 基线 `compatibility` frontmatter 字段不被当前 `skill-creator` validator 接受。
- P0 将原字段内容完整迁移到 `SKILL.md` 正文的 `Runtime` 段，不删除运行要求；其余基线 frontmatter 字段保持不变。
- 该迁移只发生在权威维护源，尚未同步已安装副本。

## 实施中决定

### D3 P0 行为合同

以下项目按 D6 的临时默认值实现，并由 eval 与实际使用问题驱动修订：profiler schema/启发式、选图输出、三层 QA、两轮回改和 manifest 兼容扩展。

### D4 文件与接口

按 progressive disclosure 实施：保持 `SKILL.md` 精简，把详细决策规则放入 `references/`，把确定性、重复性任务放入 `scripts/`，把触发、好/坏图和 smoke cases 放入 `evals/`。

### D5 验收方案

采用可执行临时验收基线，至少覆盖：触发准确性、profiler 不改数据、选图证据可追溯、已知视觉缺陷检出、CJK fallback、重复运行稳定性、manifest 兼容性和现有导出能力不回退。

## 明确非目标

- 第一轮不修改 `drawio-academic-skills`。
- 不自动清洗、删除或重写用户数据。
- 不由绘图 skill 静默选择或执行统计检验。
- 不把固定经验阈值、VLM 评分或样式名表述为科学正确性或投稿合规证明。
- 不默认执行未经固定版本、许可证核验和代码审计的第三方脚本。
- 不安装新的大型图库、外部多代理框架或必须联网的生成服务。

## 相关调研

- `management/01-open-source-scientific-visualization-skills-research.md`

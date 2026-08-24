# 开源科研绘图 Skills 调研与融合建议

> 调研日期：2026-08-16  
> 范围：面向 Agent/Codex/Claude Code 的科研数据图、论文复合图和科研示意图工作流；仅评估可借鉴能力，不安装、不复制第三方代码、不修改现有 skill。  
> 结论性质：这是基于各项目当前仓库、`SKILL.md`、README 和论文页面的一次快照。第三方活跃度、实现和许可证后续可能变化，真正引入前应固定 commit 并重新核验。

## 1. 结论先行

现有科研绘图能力不应整体替换。当前两条路线的基本分工是合理的：

- `scientific-visualization` 负责数据图，强项是数据诚实性、缺失值与不确定性、可访问性、期刊要求核验、可复现导出和文件级审计。
- `drawio-academic-skills` 负责架构图、工作流、路线图和论文示意图，强项是 YAML-first、可编辑矢量源、语义冻结、箭头关系审计、页面尺度检查和导出回归。

网上项目真正值得融入的不是另一套“Nature 配色”，而是以下六项闭环能力：

1. **figure contract / visualization plan**：先写清图要回答的问题、核心结论、证据、面板和审稿风险，再画。
2. **只读数据剖析与选图顾问**：自动报告列类型、样本量、缺失、分布、异常、分组与尺度风险；结合论证目标推荐图型，而不是服从用户点名的图型。
3. **渲染后视觉 QA**：先做确定性检查，再查看最终尺寸预览，形成有上限的“发现问题—修改—重渲”闭环。
4. **CJK 字体预检与实际 fallback 报告**：在绘图前发现方框、负号和中西文混排问题。
5. **多面板一致性合同**：统一变量颜色、尺度、字号、panel label、图例与物理尺寸，并记录到 manifest。
6. **可回归 eval 套件**：覆盖触发准确率、好/坏图例、脚本 smoke test、视觉/语义不回退与第三方参考来源完整性。

不建议引入的做法包括：用固定经验阈值替代领域判断、把 VLM 评分当科学正确性证明、默认执行网上脚本、把连续色值强制分箱、把某个样式包宣称为期刊合规，以及用纯栅格生成替代可编辑示意图主流程。

## 2. 现有能力基线

### 2.1 `scientific-visualization`

当前版本已经覆盖：

- 原始数据、变换、缺失值、误差定义与随机种子的保存；
- 诚实编码、双 Y 轴、对数轴、binning、平滑、归一化等风险；
- 色彩冗余、对比度、灰度筛查与替代文本；
- Matplotlib/Seaborn/Plotly 的实现注意事项；
- 原子导出、禁止隐式覆盖、manifest、字体与位图元数据审计；
- 按具体期刊、文章类型、figure 类型和投稿阶段核验实时规范。

当前明显缺口：

- 没有 `profile_data.py` 一类的只读数据剖析入口；
- 没有“科学问题/论证目标 → 图型与 panel”的结构化决策输出；
- “人工查看最终图”已有原则，但没有程序化 layout QA 和明确的视觉回改协议；
- 没有 CJK 字体探测/回退脚本；
- 多面板只有 API 提示，没有统一 panel label、跨 panel 颜色/尺度一致性检查；
- 没有独立 `evals/`、已知好/坏样例和触发准确率测试。

### 2.2 `drawio-academic-skills`

当前版本已经覆盖复杂图计划确认、`source --relation--> target` 语义合同、YAML-first、node budget、调色板 print gate、CJK fallback、最终导出物视觉检查、标签/箭头/线型语义回归以及可编辑源交付。它与数据绘图 skill 的边界应保留。

可增强但不应重写的部分：

- 增加“从多个参考图抽取风格但不复制内容”的离线参考索引；
- 给复杂论文示意图提供 2–3 个低成本布局草案，再冻结语义与布局；
- 把现有语义回归与视觉检查结果写成更统一的机器可读 manifest；
- 将现有 eval 与每次新增模板/图型的 gold/bad case 绑定。

## 3. 代表性开源项目

这里的“优秀”指某一工作流设计有明确可复用价值，不等于其全部规则都可靠，也不等于已经验证能直接用于本项目。

### 3.1 SciPilot Figure Skill

来源：[仓库](https://github.com/Haojae/scipilot-figure-skill)；[当前 `SKILL.md`](https://raw.githubusercontent.com/Haojae/scipilot-figure-skill/main/SKILL.md)；仓库标注 MIT。

值得借鉴：

- 先问“这张图要论证什么”，再运行数据剖析和选图；
- `profile_data.py` 报告列类型、n、缺失、偏态、异常值、相关与分组规模；
- `chart_selection.md` 把数据形态与论证目标共同用于选图；
- `visual_qa.py` + 最终 PNG 人工/视觉模型查看的双层 QA；
- `layout_tools.py` 统一 panel label 与布局；
- CJK 字体优先级、负号修复和中文衬线混排；
- 可选依赖缺失时显式降级。

需要改造：

- “n 小于某值就严禁某图”等硬规则应改为风险提示；是否适用取决于估计量、数据生成过程和领域惯例。
- “不得在 Word/LaTeX 再缩放”过于绝对，应改成计算最终有效字号与线宽，并在目标版面复核。
- 视觉模型只能检查可见问题，不能证明统计或科学含义正确。

融合判断：**最高优先级**。吸收工作流、数据 profiler、CJK preflight 和 bounded visual QA，不复制未经审计的期刊数字与强制阈值。

### 3.2 Academic Figure Skill

来源：[仓库](https://github.com/TingxiYu/academic-figure-skill)；[当前 `SKILL.md`](https://raw.githubusercontent.com/TingxiYu/academic-figure-skill/main/SKILL.md)；[许可证文件](https://github.com/TingxiYu/academic-figure-skill/blob/main/LICENSE)。

值得借鉴：

- 问题驱动而非模板驱动；在生成前提交 `Visualization Plan`；
- figure contract 将科学目标、每个 panel 回答的问题、数据依据与版式绑定；
- 生产资产目录、图型路由、Python/R runtime preflight；
- 四层 QA：反模式、代码合规、视觉逻辑/数据完整性、最终渲染；
- 统计与可复现报告包含 n 的定义、中心/区间、检验、校正、数据来源与 ML split/seed；
- 自带 trigger benchmark、reference integrity、QA coverage 和 E2E runner。

需要改造：

- “copy-first 并执行生产脚本”只适合可信、固定版本、已审计的本地资产；不能默认执行网上或未知来源代码。
- 把 R panel 先栅格化再拼入 Python 会损失可编辑性和矢量质量，必须作为兼容回退而非默认。
- 火山图显著点数、相关阈值、PCA 组间/组内方差比等固定“可画门槛”没有普适科学依据，不应进入通用 skill。
- 统计检验不应由绘图 skill 静默决定；应读取已确认分析或明确停在建议/展示层。

融合判断：**最高优先级**。引入 figure contract、分层 QA、统计/溯源报告字段和 eval 架构；拒绝固定数据门槛与不受信脚本执行。

### 3.3 AgentFigureGallery

来源：[仓库](https://github.com/Dsadd4/AgentFigureGallery)；[当前 skill 控制器](https://raw.githubusercontent.com/Dsadd4/AgentFigureGallery/main/skills/agent-figure-gallery/SKILL.md)；仓库标注 MIT。

值得借鉴：

- skill 本身只做轻量控制，不把大图像库塞入上下文；
- 先按任务/plot type 查询，再给用户看候选，记录 like/reject/select；
- stable candidate ID、plot type、来源、许可证与选择会话可追溯；
- 选择后只导出小型 reference bundle 给绘图 agent；
- lab/global preference 可形成长期一致的视觉语言。

需要改造：

- 不引入其大型远程图库作为核心依赖；先做 20–40 个经过许可核验的本地最小参考集。
- 参考图只能提供布局/风格先验，不能成为照抄数据、文字、商标或受保护构图的依据。
- 用户偏好不能覆盖数据诚实、可访问性和期刊规则。

融合判断：**中高优先级**。适合新增独立的 `reference-index` 辅助层，不应膨胀 `SKILL.md`。

### 3.4 agent-research-skills / figure-generation

来源：[仓库](https://github.com/lingzhi227/agent-research-skills)；[figure-generation `SKILL.md`](https://raw.githubusercontent.com/lingzhi227/agent-research-skills/main/skills/figure-generation/SKILL.md)；其方法明确借鉴 [MatPlotAgent](https://arxiv.org/abs/2402.11453)。

值得借鉴：

- “查询扩写 → 代码执行/报错修复 → 最终 PNG 视觉反馈”的短闭环；
- 重试次数有上限；
- 同时交付 PNG 预览、PDF 矢量文件和 LaTeX include 片段；
- 明确检查 labels、legend、色彩、尺度和最终字号。

需要改造：

- 视觉反馈必须拆成三类：数值映射、文字/单位、几何与可读性，避免一个总分掩盖严重错误。
- LaTeX caption 不能默认写 “Best viewed in color”；色彩不应是唯一编码。
- 代码能执行、产生 PNG 只是最低门槛，不代表数据语义和统计结论正确。

融合判断：**高优先级**。吸收 bounded render-review loop；结合 [PlotGen 的 numeric/lexical/visual 分层反馈思路](https://arxiv.org/abs/2502.00988)，但保持主线程最终判断。

### 3.5 Scientific Publication Plotter

来源：[仓库](https://github.com/dazhiyang/scientific-plotting-skill)；[当前 `SKILL.md`](https://raw.githubusercontent.com/dazhiyang/scientific-plotting-skill/main/SKILL.md)；MIT。

值得借鉴：

- R/ggplot2 与 Python/plotnine 路线；
- 脚本顶部集中参数块，便于复用和审计；
- 稳定类别顺序与颜色映射，避免重跑后颜色漂移；
- 密集散点和地图的文件体积意识；
- plot title 与论文 caption 的职责分离。

不建议直接引入：

- “连续色只能使用 viridis 且自动等频分箱”过于限制；连续量默认应保留连续映射，是否分箱取决于科学语义。
- “只允许一种字号”“只允许 Times”等规则不适用于所有期刊和中英文场景。
- EPS 不能作为通用首选，应跟随目标期刊的实时要求。

融合判断：**中优先级**。引入参数集中化、类别映射稳定性和可选 ggplot2 adapter；不引入单一风格教条。

### 3.6 K-Dense Scientific Schematics

来源：[当前 `SKILL.md`](https://raw.githubusercontent.com/K-Dense-AI/scientific-agent-skills/main/skills/scientific-schematics/SKILL.md)；MIT。

值得借鉴：

- 生成、审阅、定向改写、版本日志与停止原因；
- 明确记录外部 API、数据外发和未审阅状态；
- 把 prompt、每轮结果和 review log 作为溯源材料。

不建议融入主交付路线：

- 其主输出是由图像模型决定分辨率的 PNG，无矢量路径、DPI 控制和精确文字保证；
- VLM 评分阈值是工作流启发，不是投稿合规或科学正确性证明；
- 未发表或敏感研究内容存在外发风险。

融合判断：**仅借鉴日志与隐私门禁**。复杂图的可选概念草图可用，但不能替代 `drawio-academic-skills` 的 YAML、`.drawio`、SVG/PDF 与语义回归。

### 3.7 LiveFigure

来源：[仓库](https://github.com/tsinghua-fib-lab/LiveFigure)。它不是标准 `SKILL.md` 包，但其 agentic 科研示意图架构有参考价值。

值得借鉴：

- 把 visual planning、procedural generation 与 refinement 分开；
- 从参考图检索风格，再生成统一 style guide；
- 使用预验证的原子绘图 primitives 提高可执行性；
- 输出可编辑 PowerPoint，而不是只给扁平图。

风险：仓库当前历史和工程成熟度需进一步验证；参考图检索、VLM 与图标生成引入外部模型、版权和隐私问题。

融合判断：**概念级借鉴**。现有 draw.io 路线已拥有更强的可编辑、离线和语义门禁，应只吸收“规划—原子生成—细化”分层与本地参考检索。

### 3.8 PaperBanana 开源实现

来源：[仓库](https://github.com/llmsresearch/paperbanana)。它是完整框架，不是轻量 skill。

值得借鉴：

- venue style pack 可由用户/实验室扩展，不直接修改核心；
- manifest 驱动批量绘图、checkpoint/resume、失败重试与报告；
- 从整篇论文规划多个方法图、数据图、caption 与 LaTeX 集成包；
- 统计图使用 VLM 生成 Matplotlib 代码，而不是图像模型直接画数据图。

风险：默认工作流依赖外部 VLM/图像模型，复杂、成本高；critic 满意不等于准确；批量生成扩大错误传播面。

融合判断：**后续阶段借鉴**。优先吸收 style pack schema、batch manifest、resume 和 figure package；不把外部多代理框架设为基本依赖。

### 3.9 底层样式库：SciencePlots 与 TUEplots

来源：[SciencePlots](https://github.com/garrettj403/SciencePlots)；[TUEplots 官方文档](https://tueplots.readthedocs.io/en/latest/index.html)。二者不是 agent skill，但可作为受控样式后端。

可借鉴：

- SciencePlots 的可组合 style、CJK style 和多种颜色循环；
- TUEplots 用 `rcParams` 字典表达字体、版心、尺寸和 venue bundle，适合临时 style context；
- 都能减少散落在生成代码里的手写 rcParams。

限制：样式包是起点，不是期刊合规证明；版本和 venue 模板会过期；LaTeX/CJK 字体依赖需预检。

融合判断：**可选 adapter**。优先保持现有内置、审计过的 style presets；检测到包时才启用，并在 manifest 中记录包版本和实际字体。

## 4. 能力对照与建议落点

| 能力 | 当前状态 | 主要来源 | 建议落点 | 优先级 |
|---|---|---|---|---|
| 科学问题/论证目标 | 有原则，无结构化合同 | SciPilot、Academic Figure | `references/figure_contract.md` + 计划模板 | P0 |
| 数据剖析 | 缺失 | SciPilot | `scripts/profile_data.py`，默认只读 JSON/Markdown | P0 |
| 选图决策 | 规则散落 | SciPilot、Academic Figure | `references/chart_selection.md`，输出推荐/理由/备选/风险 | P0 |
| 渲染后 layout QA | 以人工清单为主 | SciPilot、MatPlotAgent 路线 | `scripts/visual_qa.py` + bounded review protocol | P0 |
| CJK 预检 | 数据图缺失；draw.io 已较强 | SciPilot、SciencePlots | `scripts/font_preflight.py`，报告实际 fallback | P0 |
| 多面板一致性 | 基础支持 | SciPilot、Academic Figure | `scripts/layout_tools.py` + figure manifest | P1 |
| 统计/复现报告 | manifest 已有部分字段 | Academic Figure | 扩展 manifest schema，不自动做未经授权的检验 | P1 |
| 参考图/偏好 | 缺失 | AgentFigureGallery、LiveFigure | 独立、许可核验的轻量 reference index | P1 |
| ggplot2/plotnine | 缺失 | Scientific Publication Plotter | 可选 adapter skill，不塞进核心入口 | P2 |
| style/venue packs | 静态内置 profiles | PaperBanana、TUEplots | 可版本化的 lab/venue profile schema | P2 |
| eval 与回归 | 数据图 skill 缺失；draw.io 较成熟 | Academic Figure | `evals/`：trigger、good/bad、smoke、semantic regression | P0 |
| 批量/恢复 | 缺失 | PaperBanana | manifest + resume，单图链路稳定后再做 | P2 |

## 5. 建议的融合架构

不要把所有能力堆进一个超长 `SKILL.md`。建议保留一个短入口和按需加载的辅助层：

```text
scientific-visualization/
├── SKILL.md                         # 路由、硬边界、主闭环
├── references/
│   ├── figure_contract.md           # 目标、论点、证据、panel、风险
│   ├── chart_selection.md           # 数据形态 × 论证目标
│   ├── visual_review.md             # 数值/文字/几何分层检查
│   └── ...                          # 保留现有引用
├── scripts/
│   ├── profile_data.py              # 只读、确定性、显式阈值来源
│   ├── font_preflight.py            # CJK/数学/负号/fallback
│   ├── visual_qa.py                 # clipping/overlap/缺字/最终尺寸预览
│   ├── layout_tools.py              # panel label 与一致性
│   └── ...                          # 保留现有导出与审计
└── evals/
    ├── trigger_cases.json
    ├── chart_choice_cases.json
    ├── known_good/
    ├── known_bad/
    └── smoke_test.py
```

建议把一次数据图任务固定成下面的状态机：

```text
INTAKE
  -> CONTRACT (问题、论点、受众、目标尺寸、数据语义)
  -> PROFILE (只读；不清洗、不删数据)
  -> PLAN (推荐 + 理由 + 备选 + 风险；复杂/歧义时确认)
  -> RENDER
  -> AUDIT_NUMERIC
  -> AUDIT_TEXT
  -> AUDIT_VISUAL_AT_FINAL_SIZE
  -> REVISE (最多 2 轮，超限则报告残余问题)
  -> EXPORT + MANIFEST + CAPTION/ALT-TEXT DRAFT
```

示意图继续走 `drawio-academic-skills`，只共享以下跨 skill 合同：

- `figure_id`、用途、目标版心尺寸、语言与实际字体；
- caption/legend/abbreviation 字段；
- palette 与非颜色冗余编码；
- source/transform/provenance；
- 每轮视觉问题和最终残余风险；
- 最终 artifact 清单与 hash。

## 6. 明确不融合的规则

1. **不把经验阈值包装成科学门槛。** 例如“显著点必须至少 10 个”“相关系数必须超过 0.3”“n<10 绝不能画某图”只能作为可配置启发或风险提示。
2. **不允许自动静默删行、删列或改变统计单位。** profiler 只报告；改变数据必须由分析流程明确授权并记录。
3. **不把 VLM score 当验收证书。** VLM 只能辅助发现裁切、遮挡、错字、对齐和明显图文不一致。
4. **不默认执行第三方脚本。** 参考资产应先固定 commit、核验许可证、人工审计代码并在受限环境 smoke test。
5. **不以样式名代替实时投稿规范。** `nature`、`ieee` 等只是带日期的起点；提交前仍查官方当前规则。
6. **不把连续变量默认分箱。** 分箱会损失信息；只有科学问题需要离散等级时才做，并记录边界与敏感性。
7. **不把外部图像生成设为必经路径。** 未发表数据、敏感图和精确文字/公式图默认本地、可编辑、确定性生成。
8. **不让交互图替代静态图、alt text 或数据表。** 两者仍是不同交付物。

## 7. 分阶段实施建议

### P0：先补“正确地决定和验证”

建议作为一个独立版本完成：

1. 新增 figure contract 与 chart-selection reference；
2. 新增只读 profiler，输出稳定 JSON schema；
3. 新增 CJK/font preflight；
4. 新增最终尺寸 PNG preview 与确定性 layout QA；
5. 建立 `evals/`，至少覆盖 20 个 trigger、20 个选图、10 个已知坏图和全脚本 smoke test；
6. 将 numeric/textual/visual 三类检查结果写入现有 manifest。

验收条件：

- 同一输入重复运行产生同 schema、同风险分类；
- profiler 不改原始文件；
- 图型建议明确列出证据、假设和备选，不伪造统计结论；
- 已知裁切、缺字、颜色唯一编码、错误单位和 panel 不一致样例能被对应门禁发现；
- 最终交付仍保持当前原子写入、拒绝隐式覆盖和 publisher caveat。

### P1：再补“高质量复用”

- 多面板 layout helper；
- 许可核验的本地 reference mini-pack 与稳定 ID；
- lab preference/style profile；
- 统计/复现报告 schema；
- caption、alt text、LaTeX/Markdown include 片段生成。

### P2：最后补“扩展栈与批量化”

- 可选 ggplot2/plotnine adapter；
- SciencePlots/TUEplots adapter；
- batch manifest、checkpoint/resume 和整篇论文 figure package；
- 更大图库或外部 VLM 仅作为显式 opt-in。

## 8. 最终建议

如果只做一轮增强，优先做 P0，不要先扩充图型模板。现有 skill 已经知道“如何诚实地画并正确导出”，下一步最有价值的是让它在画之前能回答“为什么应该画这张图”，画之后能用可复现证据回答“最终文件是否真的可读、语义是否仍一致”。

代码或资产复用前，逐项目执行：固定 commit → 核验 LICENSE 与第三方素材许可证 → 只挑小模块 → 本地审计 → 加回归测试 → 再合并。本文建议的是能力设计，不构成对任何第三方代码的直接引入授权。

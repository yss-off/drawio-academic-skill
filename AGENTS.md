# Academic Figure Skills 工程约束

## 权威源与安装边界

- `plugins/academic-figure-skills/` 是可安装 Codex 插件的权威源；`.codex-plugin/plugin.json`、插件版本和运行时路径必须与 `pyproject.toml` 同步。
- `plugins/academic-figure-skills/skills/drawio/` 是固定上游导入的通用 draw.io base，来源提交和版本由 `pyproject.toml` 与 `management/08-codex-plugin-refactor.md` 共同记录。
- `plugins/academic-figure-skills/skills/drawio-academic-skills/` 是关系型/示意型论文图 overlay 的权威源。
- `plugins/academic-figure-skills/skills/scientific-visualization/` 是数据驱动科研图 skill 的权威源。
- `pyproject.toml` 是工程、插件和三个 skill 版本清单的唯一权威；各 manifest/frontmatter/eval 版本必须与清单同步并由 `tools/verify_project.py` 校验。
- `/home/yss/.codex/skills/drawio-academic-skills/` 只是已安装运行副本；未经用户明确授权，不得同步、覆盖或删除。
- `/home/yss/.codex/skills/scientific-visualization/` 同样只是已安装运行副本；未经用户明确授权，不得同步、覆盖或删除。
- `/home/yss/.codex/skills/drawio/` 同样只是已安装运行副本；不得把它当作工程源或回写目标。
- bundled `drawio` 只通过固定权威上游 rebase 更新；base 问题不得在 overlay 内复制 runtime 修补。
- `management/` 只保存基线、设计决定、审计和验收记录，不得被 skill 运行时加载。

## 当前范围

- 本仓库统一维护一个自包含三-skill Codex 插件，不再把任何已安装副本当作可回写的权威源。
- 工程根目录维护版本、跨 skill 路由、开发说明、打包工具与验收记录；插件目录保存 manifest、许可和运行时 skills。
- 运行时 skill 目录只保留实际执行所需的 `SKILL.md`、`agents/`、`assets/`、`references/`、`scripts/`、`styles/`、`evals/` 和显式可选运行配置；项目 README、CHANGELOG、安装说明和 management 记录留在工程根目录。
- 插件稳定名为 `academic-figure-skills`，个人工程/插件版本从 `0.3.0` 演进。
- bundled base skill 名保持 `drawio`，固定上游基线为 `bahayonghang/drawio-skills` v2.7.0 commit `27dac02ce3b4901c844aaa623ad64c3d577c3a72`。
- skill 名保持 `drawio-academic-skills` 以兼容现有触发与安装路径；个人工程版本从 `0.1.0` 独立演进。
- skill 名 `scientific-visualization` 同样保持不变；数据图与关系图通过语义输入和绘制后端区分，不靠改名破坏兼容性。
- 跨 skill 请求允许组合交付，但每个 panel 必须保留自己的规范源、生成命令、artifact 和证据。
- 不安装大型图库，不把外部图像生成或视觉模型设为必经路径，不新增联网运行依赖。

## 设计约束

- 保持 overlay 薄且 `SKILL.md` 精简；共享执行继续走同一插件内 sibling base。
- `scientific-visualization` 保持 Python plotting 后端，不把 Matplotlib/Seaborn/Plotly 代码塞入 draw.io overlay，也不强迫数据图生成 `.drawio`。
- 三个 skill 共享插件版本治理和路由 gold cases，但除既有 draw.io base/overlay seam 外，不抽取会破坏独立入口的共享运行时模块。
- 对 `drawio-academic-skills`，YAML 仍是规范源；布局候选只规划语义和几何意图，不直接生成最终图片或改写科学内容。
- 参考索引只保存元数据、许可、来源、可借鉴布局特征和稳定 ID；不得把参考图内容、文字、商标或受保护构图当作可复制资产。
- manifest 记录合同、语义 inventory、布局选择、palette/font/export/QA/provenance；任何未知证据标为 `pending` 或 `not_checked`，不得伪造 PASS。
- 对 `drawio-academic-skills`，学术交付以 `academic-figure-playbook.md § Academic Delivery Matrix` 为唯一选择权威：始终交付 `.drawio`，并在 `raster-publication`、`vector-submission`、`draft-preview` 中选择一个主类别；该合同不得套用到数据图后端。
- 不把启发式、VLM 评分、模板名或 venue 风格名表述为科学正确性、版权安全或投稿合规证明。

## 修改与验证

- 变更保持 skill-local；若 draw.io 问题实际属于 base，记录并停止，不在 overlay 复制 runtime 修补。
- 使用 `make test` 做三 skill 聚焦回归，`make test-routing` 校验路由契约，`make check` 做工程与插件校验，`make check-base` 做 bundled base/overlay 兼容验证，`make package` 生成确定性插件包。
- 运行时 skill 不放项目 README、CHANGELOG、安装说明或 management 记录；这些文件留在工程根目录。
- 新增脚本必须实际运行；先做聚焦测试，再做插件/skill 结构验证、现有 example strict validation 和代表性 exported-artifact forward test。
- forward test 使用原始任务和最少上下文，不向测试代理泄露预期答案；未获用户明确要求时不启动子代理。
- `make package` 生成确定性插件 ZIP；`make package-skills` 只保留兼容性的独立 skill ZIP。
- 未经用户明确要求，不提交、不推送、不发布、不安装到 Codex 运行目录或插件 cache。

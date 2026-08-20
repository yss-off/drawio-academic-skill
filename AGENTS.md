# Draw.io Academic Skill 工程约束

## 权威源与安装边界

- `skill/drawio-academic-skills/` 是本工程维护的权威 overlay 源。
- `pyproject.toml` 是个人工程版本的唯一权威；`evals/evals.json` 必须与其同步并由 `tools/verify_project.py` 校验。
- `/home/yss/.codex/skills/drawio-academic-skills/` 只是已安装运行副本；未经用户明确授权，不得同步、覆盖或删除。
- sibling `/home/yss/.codex/skills/drawio/` 是只读测试依赖；本工程不得修改或 vendor-copy 基础 CLI、schema、renderer、themes、palettes 或 shared workflows。
- `management/` 只保存基线、设计决定、审计和验收记录，不得被 skill 运行时加载。

## 当前范围

- 本仓库是独立维护的个人工程，不再把已安装 overlay 当作可回写的权威源。
- 工程根目录维护版本、开发说明、打包工具与验收记录；运行时 skill 目录只保留 `SKILL.md`、`agents/`、`assets/`、`references/`、`scripts/` 和 `evals/`。
- skill 名保持 `drawio-academic-skills` 以兼容现有触发与安装路径；个人工程版本从 `0.1.0` 独立演进。
- 当前能力包括：复杂图的 2–3 个布局候选、许可/来源可追溯参考索引、统一机器可读 figure manifest、场景化交付合同及对应 eval。
- 不安装大型图库，不把外部图像生成或视觉模型设为必经路径，不新增联网运行依赖。

## 设计约束

- 保持 overlay 薄且 `SKILL.md` 精简；共享执行继续走 sibling base。
- YAML 仍是规范源；布局候选只规划语义和几何意图，不直接生成最终图片或改写科学内容。
- 参考索引只保存元数据、许可、来源、可借鉴布局特征和稳定 ID；不得把参考图内容、文字、商标或受保护构图当作可复制资产。
- manifest 记录合同、语义 inventory、布局选择、palette/font/export/QA/provenance；任何未知证据标为 `pending` 或 `not_checked`，不得伪造 PASS。
- 学术交付以 `academic-figure-playbook.md § Academic Delivery Matrix` 为唯一选择权威：始终交付 `.drawio`，并在 `raster-publication`、`vector-submission`、`draft-preview` 中选择一个主类别；不得再引入通用 PNG 或 SVG 默认值。
- 不把启发式、VLM 评分、模板名或 venue 风格名表述为科学正确性、版权安全或投稿合规证明。

## 修改与验证

- 变更保持 overlay-local；若问题实际属于 base，记录并停止，不在 overlay 复制 runtime 修补。
- 使用 `make test` 做聚焦回归，`make check` 做工程校验，`make check-base` 做 sibling-base 兼容验证，`make package` 生成确定性安装包。
- 运行时 skill 不放项目 README、CHANGELOG、安装说明或 management 记录；这些文件留在工程根目录。
- 新增脚本必须实际运行；先做聚焦测试，再做 skill 结构验证、现有 example strict validation 和代表性 exported-artifact forward test。
- forward test 使用原始任务和最少上下文，不向测试代理泄露预期答案；未获用户明确要求时不启动子代理。
- 未经用户明确要求，不提交、不推送、不发布、不安装到 Codex 运行目录。

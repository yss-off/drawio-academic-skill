# Academic Figure Skills

这是一个自包含的 skills-only Codex 插件，用于统一分发论文示意图、通用 draw.io 和科研数据图能力。插件保留三个独立运行时 skill：

- `drawio`：YAML-first、offline-first 的通用 draw.io base；
- `drawio-academic-skills`：基于 sibling `drawio` 的 thin overlay，处理模型架构、机制、流程、路线和关系型论文图；
- `scientific-visualization`：基于 Matplotlib、Seaborn 或 Plotly，处理数据剖析、统计视觉编码、多面板数据图和导出审计。

三者通过一个插件统一安装和升级，但不混合绘制后端。数据图不强制生成 `.drawio`，关系图也不由 plotting helper 代画。

## 工程结构

```text
.
├── .agents/plugins/marketplace.json
├── plugins/academic-figure-skills/
│   ├── .codex-plugin/plugin.json
│   ├── LICENSE
│   ├── THIRD_PARTY_NOTICES.md
│   └── skills/
│       ├── drawio/                  # 通用 draw.io base
│       ├── drawio-academic-skills/  # 关系型/示意型论文图
│       └── scientific-visualization/# 数据驱动科研图
├── evals/routing-boundaries.json   # 跨 skill 路由 gold cases
├── tools/                          # 统一验证、路由审计和确定性打包
├── management/                     # 基线、决定、来源和验收记录
├── AGENTS.md                       # 工程约束
├── pyproject.toml                  # 工程版本与 skill 清单
└── Makefile                        # 统一开发入口
```

`plugins/academic-figure-skills/` 是可安装插件源，其中 `skills/` 保存三个运行时入口。`/home/yss/.codex/skills/` 和插件 cache 只是部署副本，不得反向覆盖工程源。

## 路由边界

| 请求核心 | 运行时 skill |
|---|---|
| 非出版用途的通用 draw.io、系统架构、网络拓扑、UML、流程图或 `.drawio` 编辑 | `drawio` |
| 论文、学位论文、投稿或 camera-ready 的关系、机制、架构、流程、路线图 | `drawio-academic-skills` |
| 数据变量、重复单位、缺失值、不确定性、统计视觉编码或 Matplotlib/Seaborn/Plotly | `scientific-visualization` |
| 同一交付物同时包含关系图与数据图 | 组合使用两个 skill，分别保留规范源和证据 |
| 只有“画一张论文图”，无法判断数据图还是示意图 | 先澄清图要表达的数据或关系 |

## 快速验证

```bash
make test                # 三个 skill 的离线聚焦回归
make test-routing        # 跨 skill 路由契约
make check               # 插件、三 skill、版本、JSON、CLI 和回归校验
make check-plugin        # 使用 Codex plugin-creator 验证插件 manifest
make check-base          # 验证 bundled drawio 与 academic overlay 的严格兼容性
make package             # 生成确定性 Codex 插件 ZIP
make package-skills      # 生成三个独立 skill ZIP（兼容分发）
make package-base        # 仅打包 drawio base
make package-academic    # 仅打包 drawio-academic-skills
make package-scientific  # 仅打包 scientific-visualization
```

所有命令离线运行。`check-base` 默认使用插件内 bundled `drawio`，也可显式验证另一个 base：

```bash
python3 tools/verify_project.py --with-base --base /path/to/drawio
```

## 本地 marketplace

仓库包含 `.agents/plugins/marketplace.json`，插件源位于 `plugins/academic-figure-skills/`。工程验证不会安装插件；需要安装或刷新本地副本时，必须另行明确授权。

## 运行时能力边界

`drawio-academic-skills` 始终交付可编辑 `.drawio`，并按 `raster-publication`、`vector-submission` 或 `draft-preview` 选择主交付类别；复杂任务可比较布局候选并记录语义、布局、artifact、QA 与 provenance manifest。

`scientific-visualization` 保留原始数据和变换证据，提供只读 CSV/TSV profiler、证据化选图、字体/配色/布局审计、原子导出与期刊规则核验；它不会静默清洗数据、选择统计检验或把经验阈值表述为标准。

## 来源与发布边界

- bundled `drawio` 固定自 `bahayonghang/drawio-skills@27dac02` v2.7.0；许可证和第三方归属见插件内 `THIRD_PARTY_NOTICES.md`。
- `make package` 只写入忽略跟踪的 `dist/`，生成插件 ZIP，不会安装。
- 安装或覆盖任一运行副本、commit、push 和发布仍需要单独明确授权。
- base 问题在 `management/` 记录并通过固定上游 rebase 处理，不在 academic overlay 复制 runtime 修补。

工程、插件和三个 skill 的版本清单见 `pyproject.toml`，变更记录见 [CHANGELOG.md](CHANGELOG.md)。

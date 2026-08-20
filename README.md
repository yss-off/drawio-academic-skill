# Draw.io Academic Skill

这是独立维护的学术 draw.io skill 工程。工程拥有自己的版本、测试、打包和决策记录；运行时仍保持 thin overlay，通过只读 sibling `drawio` skill 复用 CLI、renderer、schema、themes 和 shared workflows。

## 工程结构

```text
.
├── skill/drawio-academic-skills/  # 可安装运行时源
├── tools/                         # 工程验证与确定性打包
├── management/                    # 基线、决定和验收记录
├── AGENTS.md                      # 工程约束
├── pyproject.toml                 # 独立工程版本
└── Makefile                       # 统一开发入口
```

`skill/drawio-academic-skills/` 是唯一运行时权威源。`/home/yss/.codex/skills/drawio-academic-skills/` 只是已安装副本，不得反向覆盖工程源。

## 快速验证

```bash
make test        # overlay-local 离线回归
make check       # 结构、JSON、Python、skill 和回归校验
make check-base  # 额外使用本机 sibling base 严格验证全部示例/模板
make package     # 生成确定性、可安装 ZIP
```

所有命令离线运行。`check-base` 自动查找 `~/.codex/skills/drawio` 或 `~/.agents/skills/drawio`，也可显式指定：

```bash
python tools/verify_project.py --with-base --base /path/to/drawio
```

## 运行时能力

- 复杂论文图的 2–3 个布局候选；
- 带许可证与来源的本地参考索引；
- 语义、布局、artifact、QA 与 provenance 统一 manifest；
- `raster-publication`、`vector-submission`、`draft-preview` 场景化交付合同；
- publication、print、palette、formula、CJK 和闭环语义验收。

始终交付可编辑 `.drawio`。主交付格式由 skill 内 `Academic Delivery Matrix` 决定，不设置通用 PNG 或 SVG 默认值。

## 发布边界

- `make package` 只写入忽略跟踪的 `dist/`，不会安装。
- 安装、覆盖运行副本、commit、push 和发布都需要单独明确授权。
- sibling base 是外部只读依赖；base 问题在 `management/` 记录，不在 overlay vendor-copy 修补。

当前个人工程版本见 `pyproject.toml`，变更记录见 [CHANGELOG.md](CHANGELOG.md)。

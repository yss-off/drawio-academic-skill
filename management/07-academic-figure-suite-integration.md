# Academic Figure Skills 整合决定

## 目标

2026-08-20，用户确认将原独立维护工程 `scientific_visualization_skill` 整合到当前工程，形成一个工程、两个运行时 skill：

- `drawio-academic-skills`：关系型、示意型论文图；
- `scientific-visualization`：数据驱动科研图。

整合统一工程治理、版本清单、路由 gold cases、验证、打包和来源审计，但不合并两个绘制后端，也不改变现有运行时 skill 名称。

## Seam 决定

共享层是论文图的科学语义、期刊场景、字体/配色、最终 artifact 复核和证据诚实性。真正的后端 seam 是图的规范源：

- 节点、边、箭头、机制、架构、流程、路线和可编辑 `.drawio` 走 draw.io；
- 数据变量、重复单位、缺失值、不确定性、统计视觉编码和 plotting library 走 scientific visualization；
- 混合图组合两个后端，各自保留规范源、生成命令、artifact 和 QA；
- 无法判断是在解释数据还是关系时先澄清，不靠“论文图”一词猜测。

这两个后端的实现、依赖和测试表面不同，因此不抽取共享运行时代码。工程层通过统一清单、路由契约和验证器提供治理 locality；运行时 skill 仍可独立打包。

## 迁移来源

- 原工程：`/home/yss/code/scientific_visualization_skill/`
- 迁入运行时源：`skill/scientific-visualization/`
- 迁入历史记录：`management/scientific-visualization/`
- 原始基线与作者/许可证信息继续由 `management/scientific-visualization/00-baseline-provenance.md` 记录。
- P0 第三方参考及许可证审计继续由 `management/scientific-visualization/03-upstream-integration-audit.md` 记录。

迁移排除 `__pycache__` 和 `.pyc`。只有在逐文件核对、双 skill 回归、结构校验、确定性打包和解包验证全部通过后，才删除原独立工程目录。

## 安装和发布边界

本次整合只修改工程源。除非用户另行明确授权，否则不覆盖 `/home/yss/.codex/skills/` 下的两个已安装副本，不 commit、不 push、不发布。

## 验证与旧工程清理

- 原 `skill/scientific-visualization/` 与迁入目录逐文件一致，排除的只有 `__pycache__` 和 `.pyc`。
- 原 `management/` 与迁入的 `management/scientific-visualization/` 逐文件一致。
- `make test`：draw.io 10 项、scientific visualization 6 项，全部通过。
- `make check`：两个 skill 的结构、版本、JSON、skill-creator、smoke 以及 9 个 plotting CLI 帮助入口通过。
- `make check-base`：draw.io sibling base 的 10 个 example/template 严格验证通过。
- 路由契约：14 项通过，其中 draw.io 5、scientific visualization 5、compose 2、clarify 2；保留 2 项 scientific 对 draw.io 的负触发用例。
- 两个独立目录生成的 ZIP SHA-256 一致；解包后的两个 skill 再次通过 skill-creator 和各自 smoke tests。
- `drawio-academic-skills-0.1.0.zip`：30 个文件，SHA-256 `8a6dfcbc8108344f3c6cc52439e74966d36c9a798e3a952fc181a326d0717949`。
- `scientific-visualization-1.2.zip`：29 个文件，SHA-256 `87baf426d99ecbec3d810ece9885f0005e41217c2f8fcab4929eba234df65c8a`。

验证完成后，旧独立工程 `/home/yss/code/scientific_visualization_skill` 已按用户要求移入系统回收站；当前可恢复副本位于 `/home/yss/.local/share/Trash/files/scientific_visualization_skill`。已安装运行副本未修改。

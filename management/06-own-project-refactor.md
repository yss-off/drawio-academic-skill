# 个人工程化重构验收

## 目标与决定

2026-08-20，用户要求把 `drawio-academic-skills` 重构成独立维护的个人工程。重构保留运行时 skill 名和 thin-overlay 架构，以兼容现有触发与 sibling base；权威关系改为：

- 工程源 `skill/drawio-academic-skills/` 是唯一运行时权威；
- `pyproject.toml` 是个人工程版本权威，初始版本 `0.1.0`；
- 已安装目录只是部署副本，不再作为工程回写源；
- sibling base 仍是外部只读依赖，不 vendor-copy。

## 结构变化

- 新增根目录 `README.md`、`CHANGELOG.md`、`LICENSE`、`pyproject.toml` 和 `Makefile`。
- 新增 `tools/verify_project.py`：离线验证项目结构、版本同步、JSON、smoke tests、skill-creator 校验，以及可选的 sibling-base 严格验证。
- 新增 `tools/package_skill.py`：按固定顺序、时间戳和权限生成原子、确定性 ZIP，拒绝隐式覆盖和 symlink。
- 上游 README/CHANGELOG 及不参与运行的历史 eval 快照迁到 `management/upstream/`。
- 运行时 skill 根目录只保留 `SKILL.md`；其余运行资源位于 `agents/`、`assets/`、`evals/`、`references/`、`scripts/`。
- `evals/evals.json` 版本改为 `0.1.0`，并由工程 verifier 强制与 `pyproject.toml` 同步。

## 统一入口

```text
make test        -> overlay-local smoke tests
make check       -> portable project verification
make check-base  -> project verification + 10 bundled YAML strict checks
make package     -> deterministic install-ready ZIP
```

## 验证证据

- `make test`：10/10 通过。
- `make check`：PASS；version `0.1.0`、31 个 runtime source files、6 个 JSON、`SKILL.md` 176 行。
- `make check-base`：10/10 example/template 严格校验通过；保留已知 base SVG 推荐提示。
- skill-creator：`Skill is valid!`。
- 最终包：`dist/drawio-academic-skills-0.1.0.zip`，30 个安装文件。
- 两个独立输出目录生成的 ZIP 字节完全一致。
- ZIP SHA-256：`8a6dfcbc8108344f3c6cc52439e74966d36c9a798e3a952fc181a326d0717949`。
- 解包后再次运行 skill-creator 与 10 个 smoke tests，全部通过；解包后的 skill 根仅含 `SKILL.md`，无项目 README/CHANGELOG。

## 边界与恢复

- 未 commit、push、发布或安装；已安装 overlay 和 sibling base 未写入。
- 重构前备份：`/tmp/drawio-academic-own-project.ILDeSq/`。
- `dist/` 被 Git 忽略；生成包不会自动部署。

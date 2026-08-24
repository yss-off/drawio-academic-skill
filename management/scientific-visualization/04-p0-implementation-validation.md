# P0 临时基线实现与验证记录

> 日期：2026-08-16  
> 范围：只验证权威维护源 `/home/yss/code/scientific_visualization_skill/skill/scientific-visualization/`；未同步已安装副本。

## 实现结果

- `SKILL.md` 从 v1.1 更新为维护源 v1.2，接入 contract、只读 profiler、证据化选图、字体预检和三层 QA；全文 340 行，低于 `skill-creator` 的 500 行建议上限。
- 新增 `references/figure_contract.md`、`references/chart_selection.md` 和 `references/visual_review.md`。
- 新增 `scripts/profile_data.py`、`scripts/font_preflight.py` 和 `scripts/visual_qa.py`。
- `figure_export.py` 增加可选 `workflow={figure_contract, chart_selection, qa}` manifest 扩展；未传该参数时原有报告字段和调用方式保持不变。
- 新增 20 个 trigger cases、20 个 chart-choice cases、10 个 known-bad cases、验收清单和聚焦 smoke test。
- 基线 `compatibility` frontmatter 内容完整迁入正文 `Runtime` 段；不是删除运行要求。

## 自动验证

1. `skill-creator/scripts/quick_validate.py skill/scientific-visualization`：`Skill is valid!`
2. `python -m py_compile`：全部现有和新增 Python helper 通过。
3. `scripts/*.py --help`：全部退出码为 0。
4. 固定环境：Python 3.13 + `matplotlib==3.11.1`；`evals/smoke_test.py` 共 6 项，全部通过：
   - eval 数量与 ID 唯一性；
   - profiler 源文件哈希不变、重复运行一致、Markdown 派生；
   - 多文件分别剖析，generator 形式 missing tokens 对每个文件一致；
   - visual QA 检出刻度标签重叠并拒绝隐式覆盖预览；
   - font preflight 返回存在的字体文件；
   - workflow manifest 写入成功且 export 仍拒绝隐式覆盖。

## 代表性 forward test

- 对原始 `/tmp/scientific-visualization-forward.csv` 运行 CLI，剖析前后 SHA-256 均为 `8090a052026ec768aee76b2049f431be28f6cb306b7b68880eb403b8fd291bee`。
- JSON 与 Markdown 均成功生成；报告 6 行、2 个显式 treatment 分组，并将缺失、低基数数值、跨度和偏度分别标为可追溯 review prompt，没有删除、填补、变换或选图。
- CJK/math 字体预检对 `响应 Δ ± μm −1` 返回 PASS；实际 fallback 为本地 `Noto Sans CJK SC` 与 `Liberation Sans`，无缺字。
- known-bad 渲染实际检出 `visual.text_outside_canvas` 和 `visual.tick_overlap`；人工查看 PNG 确认标题裁切与刻度重叠均真实存在。
- 现有 `style_preview.py` 在 Matplotlib 3.11.1 下成功导出 2100×1560 PNG 和 PDF；`image_metadata.py` 的格式、RGBA 和 alpha 三项筛查全部通过，并人工查看最终 PNG 未见明显裁切或布局回退。

## 安装边界与仓库状态

- 已安装副本仍保持 2026-08-03 的 mtime；其 `SKILL.md` SHA-256 为 `e423d9a186260b5ae3a058cd2ece1f7fde534efc76b0e59d9aca137d42d3809e`，`figure_export.py` 为 `5fc7dd947621b861b12fad2c053f80f465f686b92258c9a7991db618d62b8627`。
- 未修改 `drawio-academic-skills`，未向 `/home/yss/.codex/skills/scientific-visualization/` 同步。
- 工程仍在 `main`，全部工程文件尚未提交；本轮未 commit、push 或发布。

## 保留风险

- P0 profiler 只处理 UTF-8 CSV/TSV，类型是词法推断；复杂科研格式与变量语义仍需显式适配。
- 自动视觉 QA 只覆盖缺字告警、非刻度文字越界和相邻刻度重叠；numeric mapping、单位/图注、图例遮挡、跨 panel 一致性仍必须对照数据和最终渲染人工/视觉复核。
- eval 已建立可执行种子集，但没有把预期答案泄露给新代理做 blind forward test；后续真实任务暴露问题时再增加 gold/bad case。
- publisher profile 仍是带日期起点，投稿前必须实时核验官方要求。

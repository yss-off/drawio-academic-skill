# Draw.io Academic Overlay

Academic overlay for publication-ready draw.io figures: papers, theses, IEEE diagrams, manuscripts, journal figures, formula-heavy visuals, research workflows, roadmaps, and A4/Word/LaTeX deliverables.

This folder is intentionally thin. It depends on the sibling Draw.io Base Skill at `../drawio` instead of copying base runtime files.

> Versioning note: this thin overlay follows the repository release version `2.6.0`. Shared diagram-production capability remains in the sibling Draw.io Base Skill, while this overlay carries publication policy and academic examples.

## Required sibling base

Install or copy both folders side by side:

```text
skills/
├── drawio/
└── drawio-academic-skills/
```

The overlay uses these base paths:

- `../drawio/scripts/cli.js`
- `../drawio/scripts/runtime/diagrams-net-url.js`
- `../drawio/references/docs/`
- `../drawio/references/workflows/`
- `../drawio/references/examples/` (shared general examples)
- `../drawio/assets/themes/`
- `../drawio/styles/built-in/`

Academic policy docs and paper examples are overlay-local:

- `references/docs/academic-figure-playbook.md`
- `references/docs/academic-export-checklist.md`
- `references/examples/` (paper/pipeline examples)

If `../drawio` is missing, install the base skill next to this overlay. Do not vendor-copy base files into the overlay.

## Default workflow

```text
academic request -> preflight + delivery class -> optional layout candidates -> YAML spec -> sibling base CLI validation -> class-matched artifact, sidecars/manifest in .drawio-tmp/<name>/
```

Always deliver editable `.drawio`. Select one primary class: `raster-publication` → 300ppi-effective PNG; `vector-submission` → PDF or path-only SVG subject to venue rules; `draft-preview` → live-text SVG labeled preview. Extra requested formats remain companions.

## Academic preflight

Before rendering, decide:

- venue or audience: paper, thesis, IEEE, journal, manuscript, Word/A4, LaTeX, slides, or draft
- figure type: `architecture`, `roadmap`, or `workflow`
- monochrome vs color policy
- caption, legend, and title needs
- formula and text-position fidelity
- requested export formats and Desktop availability
- primary delivery class; use `draft-preview` when the publication target is not fixed

## Quick export

From inside this overlay directory:

```bash
node ../drawio/scripts/cli.js references/examples/system-architecture-paper.yaml figure.svg --validate --write-sidecars --sidecar-dir .drawio-tmp/figure --strict-warnings
# raster-publication when Desktop is available
node ../drawio/scripts/cli.js references/examples/system-architecture-paper.yaml figure.png --validate --use-desktop
# vector-submission when Desktop is available
node ../drawio/scripts/cli.js references/examples/system-architecture-paper.yaml figure.pdf --validate --use-desktop
```

From the repository root:

```bash
node skills/drawio/scripts/cli.js skills/drawio-academic-skills/references/examples/system-architecture-paper.yaml figure.svg --validate --write-sidecars --sidecar-dir .drawio-tmp/figure --strict-warnings
```

If Desktop is unavailable, use the browser-rasterized derivative gate for required PNG delivery. If an accepted vector exporter is unavailable, report `vector-submission` as blocked and generate a diagrams.net editing URL from the `.drawio` artifact:

```bash
node ../drawio/scripts/runtime/diagrams-net-url.js figure.drawio
```

## MCP position

This overlay intentionally does not include `.mcp.json`. Academic create, edit, replicate, and export tasks stay local and repeatable. Live backend refinement belongs to the base skill only and is not part of the academic default path.

## Style presets

User presets live under:

```text
~/.drawio-academic-skills/styles/
```

Bundled presets live in the sibling base:

```text
../drawio/styles/built-in/
```

Never mutate bundled base presets. Copy a bundled preset into the user preset directory before making it default or editing it.

## Overlay-owned files

- `SKILL.md`: academic policy and sibling-base contract.
- `references/docs/publication-overlay.md`: overlay-only publication notes.
- `evals/`: academic evaluation set and prompt fixtures.

Shared CLI, schemas, themes, examples, workflows, official references, style-extraction guidance, and the vendored direct-XML reference all live in `../drawio`.

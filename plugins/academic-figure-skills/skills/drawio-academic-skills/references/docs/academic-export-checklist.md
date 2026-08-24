# Academic Export Checklist

Use this checklist for `meta.profile: academic-paper`.

## Required

- `meta.figureType` is present and is `architecture`, `roadmap`, or `workflow`.
- `meta.title` is present and suitable for figure captioning.
- Theme is `academic` or `academic-color`.
- Output bundle includes editable `.drawio`, work-dir `.spec.yaml`/`.arch.json`/manifest, and the primary artifact selected by `academic-figure-playbook.md § Academic Delivery Matrix`.
- `manifest.contract.delivery_class` is exactly one of `raster-publication`, `vector-submission`, or `draft-preview`; strict validation confirms PNG, PDF/path-only SVG, or preview SVG respectively.
- All formulas use the math typesetting guidance.
- Colors are not the only carrier of meaning.
- Every directed connector can be stated as `source --relation--> target`; arrowheads, loop closure, fallback paths, and cross-axis relations match the confirmed plan or source.
- Every Latin-letter abbreviation is expanded at its first figure-visible use or defined earlier in a figure-internal legend/caption.
- Word, LibreOffice, Pandoc, and XeLaTeX inputs do not reference SVGs containing `<text>` or `dominant-baseline`; use the publication PNG or a path-only vector artifact.
- Visual checks use the selected class's exported artifact. A derivative-gate browser-rasterized PNG is an artifact; an ad hoc browser/live screenshot is not.

## Recommended

- `meta.description` explains the figure intent or context.
- `meta.legend` is present when icons or mixed connector styles are used.
- Label font classes stay uniform (module title 22 / node 20 / edge label 18 / text 16 by default); manual `style.fontSize` overrides stay class-consistent and inside their boxes.
- Extra whitespace is cropped before final export.
- Line styles, node sizes, and stroke widths are consistent across the figure.
- For `raster-publication`, require a 300ppi-effective PNG. Prefer draw.io Desktop; use a source-preserving browser-rasterized PNG under the derivative gate when Desktop is absent.
- For `vector-submission`, require PDF or path-only SVG and enforce venue restrictions; IEEE requires PS/EPS/PDF.
- For `draft-preview`, allow live-text SVG but label it preview/intermediate and keep publication completion unresolved.
- Treat any SVG containing live text as preview-only. Font installation does not eliminate baseline differences across Chrome, LibreOffice, librsvg, and XeLaTeX chains.
- IEEE vector submissions accept PS/EPS/PDF only (no SVG); attach a Desktop-exported PDF when targeting IEEE.

## SVG-to-PNG Derivative Gate

Apply this gate only when the user explicitly requests a PNG derived from an existing SVG or when a PNG companion is required.

- Preserve the SVG and record its hash when the request is conversion-only. A renderer defect does not authorize compensating edits to source text coordinates.
- Prefer draw.io Desktop for a draw.io-owned source. If Desktop is unavailable, or another SVG renderer shows a measured fidelity defect, a local browser engine may rasterize the existing SVG as the final derivative; label it `browser-rasterized`, not Desktop-exported.
- Match the SVG `viewBox` aspect ratio with an explicit viewport and scale. Record final pixel dimensions, color mode/background, renderer, viewport, and scale.
- Record hashes for the editable source, preview SVG, and publication PNG so a later source edit makes the derivative fail closed instead of silently going stale.
- For CJK text using `dominant-baseline="central"`, `middle`, or equivalent centering, compare a representative label across candidate renderers before choosing one. Do not assume librsvg, ImageMagick, browser engines, and Desktop share baseline behavior.
- Inspect the final PNG at 100% and intended page size. Recheck text centering, clipping, arrowheads, connector attachment, borders, line weights, legend, grayscale meaning, and background after any renderer change.
- When building DOCX, confirm that the embedded media bytes match the accepted PNG. When building PDF, confirm matching image dimensions and at least 300ppi effective resolution, then inspect the rendered page.
- If displacement is systematic, measure intended box centers against rendered text-ink centers across repeated nodes. Record signed offsets, median, maximum absolute offset, and directional bias. A practical regression heuristic is `max(2 output pixels, 2% of box height)` with no systematic one-direction bias; report it as a QA heuristic, not a venue standard.

## Print Sizing

Labels print at `fontSize x print-width-pt / canvas-width-px` pt when the figure fills the target width (cn-thesis text block = 440pt, IEEE single column = 252pt, double column = 516pt). Keep the result at 9pt (CN) / 8pt (IEEE) or higher. Minimum label fontSize:

| Canvas width | cn-thesis (440pt/9pt) | Single column (252pt/8pt) | Double column (516pt/8pt) |
| ------------ | --------------------- | ------------------------- | ------------------------- |
| 630px        | 13                    | 20                        | 10                        |
| 1000px       | 21                    | 32                        | 16                        |
| 1200px       | 25                    | 39                        | 19                        |
| 1600px       | 33                    | 51                        | 25                        |

Set `meta.print: { target: cn-thesis | ieee-single | ieee-double }` (or custom `widthPt`/`minPt`) so the validator checks the figure; without it, only canvases wider than 1500px are checked against the IEEE single-column floor. Design the canvas for the target width instead of scaling down a wide drawing.

## Review Questions

- Is the figure still readable when inserted into an A4 thesis or paper page at normal zoom?
- Would this still be readable when printed in grayscale?
- Does the figure still make sense if the reader cannot distinguish red vs green?
- Are caption, legend, and abbreviations clear without the surrounding paragraph?
- Does the manifest select one delivery class, and does the primary artifact satisfy that class rather than a competing universal PNG/SVG default?

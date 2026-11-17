# Veto background: status report (slides)

Beamer deck (CERN / UZH / SHiP theme) on the Background Tagger status
(Background Tagging report, 16 Nov 2026).

- Main file: `main.tex` (pdfLaTeX; on Overleaf set the main document to `main.tex`).
- Theme: `beamerthemeCERNship.sty`, logos in `logos/`, figures in `figs/` (copied from the report).
- Build locally: `latexmk -pdf main.tex`.
- No CERN logo is bundled: add `logos/cern-logo-white.png` (or `logos/void.pdf`) to show it on the cover and footer.

## Example fin designs (17 Nov 2026)
`designs/make_fin_designs.py` writes `R2f_fins_ubt.json` / `R3f_fins_ubt_strips.json` (R2 / R3 without the SBT, 7 straw
fins per side from 81.13 to 31.63 m, UBT tiles 3.4 x 2.7 m^2). Examples for the slides only, not reference designs.
Evaluated with `bin/run_reco.py` (full + partial, `--em-debris --signal eventcalc --multiple-scattering`,
`VETO_RECO_INPUTS=inputs_nov4full.npz VETO_RATE_MAPS=sample_nov4full.npz`) from a private copy of the nov4-source code
in which the EM-debris tile map is cropped to the smaller tile plane; outputs in `designs/results/` (not committed).
Figure: `scripts/plot_fin_layout.py`.

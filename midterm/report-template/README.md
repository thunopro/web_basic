# Rùa Toán — Midterm report

The report now describes the inspected Rùa Toán source checkout and the public demo snapshot
captured on 1 November 2026. It includes source-based architecture, data/API diagrams,
catalogue charts, and interface screenshots. The Auth.js additions are present in the local
working tree but are uncommitted; production deployment is not confirmed. Test, performance,
accessibility, and photo-upload results are labelled according to the evidence collected.

## Before submission

Complete the group name, class and course codes, member names and IDs, roles, and verified
contribution percentages in `main.tex`. Confirm the instructor/course metadata
and live deployment state. Do not describe the unrun acceptance checks as passing. The report
does not include database or OAuth secret values.

## Compile

1. **Overleaf:** upload the `report-template` folder and select **XeLaTeX**.
2. **Local:** run `latexmk -xelatex main.tex` with TeX Live and XeLaTeX installed.
3. Review the generated PDF and update the source snapshot date/counts if the application or
   catalogue changes.

`Rua_Toan_Detailed_Report.pdf` is the new detailed draft. `main.pdf` and
`Rua_Toan_Midterm_Report.pdf` are retained as they were before this rewrite.

## Structure

- `fdareport.cls` — provided document class; do not edit.
- `main.tex` — cover information, declaration, contribution table, and chapter order.
- `chapters/` — report content.
- `figures/` — source diagrams, charts, and public-demo screenshots.
- `references.bib` — cited framework and library documentation.

Every figure and table has a caption and is referenced in the text. Full application source
and full content records remain in the Rùa Toán repository, not in this report.

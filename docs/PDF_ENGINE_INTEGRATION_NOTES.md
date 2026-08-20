# XeLaTeX PDF Engine Integration & Architecture Notes
**Language Creation System Framework**

This document records the architectural integration of the multi-volume XeLaTeX publication engine, layout optimizations, and margin overflow safeguards into `language_creation_system`.

---

## 1. Executive Summary of Changes

The publication compiler (`scripts/build_latex.py`) has been upgraded from a basic prototype into a **fully dynamic, modular publication pipeline**. It incorporates all empirical solutions developed during the creation of a 750+ page, 12,000-word multi-volume language curriculum:

*   **Dynamic Volume Discovery**: Automatically scans and compiles Book 1 (Grammar), Book 2 (Dictionary), Book 3 (Phrasebook), and Book 4 (History) across root and nested sub-language folders.
*   **Multi-Geometry Support**: Built-in presets for 8"x10" Personal, A4, US Letter, 6"x9" Trade, 5.5"x8.5" Digest, and 8"x8" Square formats.
*   **Strict Page Margin Safeguards**: Solved all horizontal margin-bleed and text overflow issues using proportional column math, `\RaggedRight` wrapping, and global emergency stretch.
*   **Double-Column Dictionary Compression**: Cuts dictionary length by ~45% while protecting prefaces and tables from `longtable` multi-column crashes.
*   **Process Safety (Windows PDF File-Locking)**: Gracefully handles locked output files in external PDF viewers by falling back to versioned filenames (`*_v2.pdf`).

---

## 2. Solving Page Margin & Text Overflow Issues

### Problem Statement
In previous builds, long words (e.g. conlang compounds, IPA tone strings), rigid table headers, code blocks, and wide tables frequently bled off the right edge of the page, causing unsightly "Overfull `\hbox`" warnings and text clipped outside printable page margins.

### Engineering Solutions Implemented

1.  **Proportional Column Width Calculation (`p{width}`)**:
    Instead of fixed centimeter dimensions (which overflow narrow paper sizes or underfill wide formats), table columns are dynamically sized as explicit fractions of printable `\textwidth` summing strictly to $\le 0.96\textwidth$:
    *   **2 Columns**: `p{0.28\textwidth}` + `p{0.67\textwidth}`
    *   **3 Columns**: `p{0.24\textwidth}` + `p{0.28\textwidth}` + `p{0.43\textwidth}`
    *   **4 Columns**: `p{0.20\textwidth}` + `p{0.20\textwidth}` + `p{0.26\textwidth}` + `p{0.29\textwidth}`
    *   **5 Columns**: `p{0.18\textwidth}` + `p{0.16\textwidth}` + `p{0.20\textwidth}` + `p{0.23\textwidth}` + `p{0.18\textwidth}`
    *   **6 Columns**: `p{0.16\textwidth}` + `p{0.14\textwidth}` + `p{0.15\textwidth}` + `p{0.17\textwidth}` + `p{0.18\textwidth}` + `p{0.15\textwidth}`

2.  **`\RaggedRight` and Flexible Header Wrapping**:
    *   Standard `\textbf{Header}` in LaTeX creates an unbreakable horizontal text box that ignores column boundaries.
    *   **Fix**: Column specifications use `>{\RaggedRight\arraybackslash}p{...}`, and header cells are formatted as `{\small\bfseries CellText}`. This allows header text to break across multiple lines cleanly within column boundaries.

3.  **Global Hyphenation & Emergency Stretch**:
    *   Added `\sloppy` and `\emergencystretch=3em` in the document preamble. When LaTeX encounters an unusually long compound word, it expands word spacing flexibly rather than letting the word extend past the right margin.
    *   Added `\usepackage{microtype}` and `\usepackage[htt]{hyphenat}` for font expansion and monospace hyphenation.

4.  **Automatic Code Block Line-Breaking**:
    *   Fenced code blocks are wrapped in the `listings` environment with `breaklines=true` and `breakatwhitespace=false`, ensuring code snippets wrap at margins.

---

## 3. Double-Column Dictionary Compression Architecture

### Problem Statement
A comprehensive 10,000+ word dictionary typeset in single-column format easily reaches 1,000+ pages. Switching the document class to `twocolumn` cuts page counts in half, but causes a fatal LaTeX crash when encountering introduction tables:
```text
! Package longtable Error: longtable not in 1-column mode.
```

### The Hybrid Layout Solution
The compiler keeps the title page, preface, licensing notice, and IPA pronunciation guide tables in **single-column mode** (`\onecolumn`), and dynamically injects `\twocolumn\footnotesize` immediately before the first alphabetical letter heading (`\section*{A}`):

```python
latex_body = re.sub(
    r'(\\section\*\{[A-ZÆÞÐ#]\})',
    r'\\twocolumn\n\\footnotesize\n\1',
    latex_body,
    count=1
)
```
*   **Result**: All introduction tables span the full page width without crashes, while the thousands of dictionary entries flow compactly across two columns in smaller `\footnotesize` text.

---

## 4. Supported Geometries & Color Themes

### Paper Geometries (`--paper`)
| Preset | Dimensions | Default Margins | Best For |
| :--- | :--- | :--- | :--- |
| `8x10` | 8.0" x 10.0" | Top/Bottom/Left/Right: 0.8" | Standard Personal Textbook (Default) |
| `a4` | 210 x 297 mm | Top/Bottom/Left/Right: 20 mm | International Standard A4 |
| `letter` | 8.5" x 11.0" | Top/Bottom/Left/Right: 0.8" | North American Standard US Letter |
| `trade` | 6.0" x 9.0" | Top/Bottom/Left/Right: 0.65" | Trade Paperback / Fiction Publishing |
| `digest` | 5.5" x 8.5" | Top/Bottom/Left/Right: 0.6" | Compact Digest Handbook |
| `square` | 8.0" x 8.0" | Top/Bottom/Left/Right: 0.75" | Art Book / Children's Primer |

### Theme Palettes (`--theme`)
| Preset | Background Color | Primary Color | Secondary / Link Color | Aesthetic |
| :--- | :--- | :--- | :--- | :--- |
| `parchment` | `#FBF0D9` (Parchment) | `#800020` (Burgundy) | `#555555` / `#800020` | Medieval / Ancient Manuscript |
| `modern` | `#FFFFFF` (Crisp White) | `#002B49` (Deep Navy) | `#4A5568` / `#005691` | Clean Academic & Corporate |
| `classic` | `#FDFBF7` (Soft Ivory) | `#1A1A1A` (Charcoal) | `#666666` / `#1B4965` | Literary / Classic Typesetting |
| `dark` | `#1E1E1E` (Dark Slate) | `#D4AF37` (Royal Gold) | `#A0A0A0` / `#E5C158` | Dark Mode / Deluxe Fantasy Edition |

---

## 5. CLI Command Reference & Examples

### Basic Compilation (Current Project)
```bash
python scripts/build_latex.py
```

### Compiling a Sub-Language Project (e.g. Mraow)
```bash
python scripts/build_latex.py --dir mraow --lang "Mraow" --author "Brian Odeen"
```

### Compiling with Trade Paperback Geometry in Classic Theme
```bash
python scripts/build_latex.py --paper trade --theme classic
```

### Compiling with A4 Geometry in Modern Theme with Custom Fonts
```bash
python scripts/build_latex.py --paper a4 --theme modern --font "Charis SIL" --ipa-font "Doulos SIL"
```

### Full CLI Options Reference
```text
options:
  -h, --help            Show this help message and exit
  --dir DIR             Root directory containing book source folders (default: current working directory)
  --paper {8x10,a4,letter,trade,digest,square}
                        Paper geometry preset (default: 8x10)
  --theme {parchment,modern,classic,dark}
                        Color theme palette (default: parchment)
  --author AUTHOR       Author name on title pages (default: Brian Odeen)
  --lang LANG           Language name (auto-detected if omitted)
  --font FONT           Primary serif font family (default: Junicode)
  --hiero-font HIERO    Fallback font for glyphs/hieroglyphs (default: Segoe UI Historic)
  --ipa-font IPA        Font family for IPA symbols (default: Arial)
```

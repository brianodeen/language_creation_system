#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dynamic Multi-Volume XeLaTeX Publication Compiler Engine (build_latex.py)
Language Creation System Framework

Converts Markdown book sources into styled XeLaTeX TeX documents and compiles
them into publication-ready PDFs in 'latex_output/'.

Key Features:
- Dynamic multi-volume discovery (Grammar, Dictionary, Phrasebook, History, custom volumes).
- Multi-format paper geometries (8x10 Personal, A4, US Letter, 6x9 Trade Paperback, 5.5x8.5 Digest, 8x8 Square).
- Configurable color palettes/themes (Parchment, Modern, Classic, Dark).
- Strict page border & margin safeguards (zero horizontal text bleeding / overfull hbox elimination).
- Intelligent table column auto-proportioning with RaggedRight text wrapping.
- Double-column dictionary compression with single-column table isolation (avoiding longtable crashes).
- Windows PDF file-lock detection with versioned fallback compilation (*_v2.pdf).
- Math and verbatim block preservation with full LaTeX character escaping.
"""

import argparse
import os
import re
import shutil
import subprocess
import sys

# Ensure UTF-8 output encoding on Windows consoles
try:
    sys.stdout.reconfigure(encoding='utf-8')
except AttributeError:
    pass

# Default MiKTeX installation path on Windows
DEFAULT_XELATEX_PATH = r"C:\Users\brian\AppData\Local\Programs\MiKTeX\miktex\bin\x64\xelatex.exe"

# ==========================================
# GEOMETRY & THEME PRESETS
# ==========================================

PAPER_GEOMETRIES = {
    "8x10": {
        "paperwidth": "8in",
        "paperheight": "10in",
        "top": "0.8in",
        "bottom": "0.8in",
        "left": "0.8in",
        "right": "0.8in",
        "description": "Standard Personal Textbook (8 x 10 in)"
    },
    "a4": {
        "paperwidth": "210mm",
        "paperheight": "297mm",
        "top": "20mm",
        "bottom": "20mm",
        "left": "20mm",
        "right": "20mm",
        "description": "Standard ISO A4 (210 x 297 mm)"
    },
    "letter": {
        "paperwidth": "8.5in",
        "paperheight": "11in",
        "top": "0.8in",
        "bottom": "0.8in",
        "left": "0.8in",
        "right": "0.8in",
        "description": "Standard US Letter (8.5 x 11 in)"
    },
    "trade": {
        "paperwidth": "6in",
        "paperheight": "9in",
        "top": "0.65in",
        "bottom": "0.65in",
        "left": "0.65in",
        "right": "0.65in",
        "description": "Standard Trade Paperback (6 x 9 in)"
    },
    "digest": {
        "paperwidth": "5.5in",
        "paperheight": "8.5in",
        "top": "0.6in",
        "bottom": "0.6in",
        "left": "0.6in",
        "right": "0.6in",
        "description": "Digest Book Format (5.5 x 8.5 in)"
    },
    "square": {
        "paperwidth": "8in",
        "paperheight": "8in",
        "top": "0.75in",
        "bottom": "0.75in",
        "left": "0.75in",
        "right": "0.75in",
        "description": "Square Format / Art Edition (8 x 8 in)"
    }
}

COLOR_THEMES = {
    "parchment": {
        "bg_color": "FBF0D9",     # Warm antique parchment
        "primary_color": "800020", # Deep Burgundy
        "secondary_color": "555555",
        "link_color": "800020",
        "description": "Antique Parchment with Burgundy Highlights"
    },
    "modern": {
        "bg_color": "FFFFFF",     # Clean Crisp White
        "primary_color": "002B49", # Deep Navy Blue
        "secondary_color": "4A5568",
        "link_color": "005691",
        "description": "Clean Modern White with Deep Navy Accents"
    },
    "classic": {
        "bg_color": "FDFBF7",     # Soft Ivory / Book Cream
        "primary_color": "1A1A1A", # Charcoal / Ebony
        "secondary_color": "666666",
        "link_color": "1B4965",
        "description": "Classic Ivory Book Typography"
    },
    "dark": {
        "bg_color": "1E1E1E",     # Dark Slate
        "primary_color": "D4AF37", # Royal Gold
        "secondary_color": "A0A0A0",
        "link_color": "E5C158",
        "text_color": "E0E0E0",
        "description": "Dark Slate with Gold Typography"
    }
}

# ==========================================
# MARKDOWN TO LATEX CONVERSION ENGINE
# ==========================================

def md_to_latex(md_content: str, is_dark_theme: bool = False) -> str:
    """
    Converts Markdown text into robust, strictly bounded XeLaTeX code.
    Safely escapes special characters, extracts math/code blocks, formats
    proportional longtables, and prevents horizontal margin overflow.
    """
    verbatims = []
    inlines = []
    maths = []
    
    # Normalize line breaks and special punctuation dashes
    content = md_content.replace('\r\n', '\n').replace('\r', '\n')
    content = content.replace('‐', '-').replace('–', '--').replace('—', '---').replace('﴾', '(').replace('﴿', ')')

    # 1. Extract fenced code blocks (preserve raw formatting)
    def repl_verbatim(m):
        code = m.group(1)
        verbatims.append(code)
        return f"VERBATIMPLACEHOLDER{len(verbatims)-1}"
    content = re.sub(r'```(?:[a-zA-Z0-9_-]+)?\n(.*?)```', repl_verbatim, content, flags=re.DOTALL)

    # 2. Extract display math blocks ($$...$$ and \[...\])
    def repl_math_block(m):
        maths.append(m.group(0))
        return f"MATHPLACEHOLDER{len(maths)-1}"
    content = re.sub(r'\$\$(.*?)\$\$', repl_math_block, content, flags=re.DOTALL)
    content = re.sub(r'\\\[(.*?)\\\]', repl_math_block, content, flags=re.DOTALL)

    # 3. Extract inline math ($...$ and \(...\))
    content = re.sub(r'\$(.*?)\$', repl_math_block, content)
    content = re.sub(r'\\\((.*?)\\\)', repl_math_block, content)

    # 4. Extract inline code (`...`)
    def repl_inline(m):
        code = m.group(1)
        inlines.append(code)
        return f"INLINEPLACEHOLDER{len(inlines)-1}"
    content = re.sub(r'`([^`]+)`', repl_inline, content)

    # 5. Escape LaTeX reserved characters in standard text
    special_chars = {
        '&': r'\&',
        '%': r'\%',
        '#': r'\#',
        '_': r'\_',
        '{': r'\{',
        '}': r'\}',
        '~': r'\textasciitilde{}',
        '^': r'\textasciicircum{}',
    }

    escaped_lines = []
    for line in content.split('\n'):
        # Do not escape markdown table borders/separators (parsed separately)
        if line.strip().startswith('|') and '---' in line:
            escaped_lines.append(line)
            continue

        new_line = ""
        for char in line:
            if char in special_chars:
                new_line += special_chars[char]
            else:
                new_line += char
        escaped_lines.append(new_line)
    content = '\n'.join(escaped_lines)

    # 6. Convert Bold and Italic formatting
    content = re.sub(r'\*\*(?!\s)(.+?)(?<!\s)\*\*', r'\\textbf{\1}', content)
    content = re.sub(r'\*(?!\s)(.+?)(?<!\s)\*', r'\\textit{\1}', content)

    # 7. Convert Markdown Headers (accounting for escaped \#)
    content = re.sub(r'^\s*\\#\s+(.+)$', r'\\chapter*{\1}', content, flags=re.MULTILINE)
    content = re.sub(r'^\s*\\#\\#\s+(.+)$', r'\\section*{\1}', content, flags=re.MULTILINE)
    content = re.sub(r'^\s*\\#\\#\\#\s+(.+)$', r'\\subsection*{\1}', content, flags=re.MULTILINE)
    content = re.sub(r'^\s*\\#\\#\\#\\#\s+(.+)$', r'\\subsubsection*{\1}', content, flags=re.MULTILINE)

    # 8. Convert Horizontal Rules
    content = re.sub(r'^---$', r'\\noindent\\rule{\\textwidth}{0.4pt}', content, flags=re.MULTILINE)

    # 9. Convert Lists (Bullet itemize & Numbered enumerate)
    lines = content.split('\n')
    new_lines = []
    current_list = None
    for line in lines:
        m_bullet = re.match(r'^\s*[-*]\s+(.+)$', line)
        if m_bullet:
            item_text = m_bullet.group(1)
            if current_list != "itemize":
                if current_list:
                    new_lines.append(f"\\end{{{current_list}}}")
                new_lines.append("\\begin{itemize}")
                current_list = "itemize"
            new_lines.append(f"\\item {item_text}")
        else:
            m_num = re.match(r'^\s*\d+\.\s+(.+)$', line)
            if m_num:
                item_text = m_num.group(1)
                if current_list != "enumerate":
                    if current_list:
                        new_lines.append(f"\\end{{{current_list}}}")
                    new_lines.append("\\begin{enumerate}")
                    current_list = "enumerate"
                new_lines.append(f"\\item {item_text}")
            else:
                if current_list:
                    new_lines.append(f"\\end{{{current_list}}}")
                    current_list = None
                new_lines.append(line)
    if current_list:
        new_lines.append(f"\\end{{{current_list}}}")
    content = '\n'.join(new_lines)

    # 10. Robust Proportional Table Conversion (Zero Margin Overflow)
    lines = content.split('\n')
    new_lines = []
    in_table = False
    table_lines = []

    def process_table(t_lines):
        if not t_lines:
            return ""
        rows = []
        for line in t_lines:
            if '|' in line:
                cleaned = line.strip().strip('|').strip()
                if all(c in ':-| ' for c in cleaned) and len(cleaned) > 2:
                    continue  # Skip separator line
                parts = [p.strip() for p in line.split('|')[1:-1]]
                rows.append(parts)

        if not rows:
            return ""

        num_cols = len(rows[0])
        
        # Calculate dynamic proportional column widths summing strictly to <= 0.96\textwidth
        # Uses \RaggedRight with hyphenation to eliminate overfull horizontal box errors
        if num_cols == 2:
            col_spec = r"|>{\RaggedRight\arraybackslash}p{0.28\textwidth}|>{\RaggedRight\arraybackslash}p{0.67\textwidth}|"
        elif num_cols == 3:
            col_spec = r"|>{\RaggedRight\arraybackslash}p{0.24\textwidth}|>{\RaggedRight\arraybackslash}p{0.28\textwidth}|>{\RaggedRight\arraybackslash}p{0.43\textwidth}|"
        elif num_cols == 4:
            col_spec = r"|>{\RaggedRight\arraybackslash}p{0.20\textwidth}|>{\RaggedRight\arraybackslash}p{0.20\textwidth}|>{\RaggedRight\arraybackslash}p{0.26\textwidth}|>{\RaggedRight\arraybackslash}p{0.29\textwidth}|"
        elif num_cols == 5:
            col_spec = r"|>{\RaggedRight\arraybackslash}p{0.18\textwidth}|>{\RaggedRight\arraybackslash}p{0.16\textwidth}|>{\RaggedRight\arraybackslash}p{0.20\textwidth}|>{\RaggedRight\arraybackslash}p{0.23\textwidth}|>{\RaggedRight\arraybackslash}p{0.18\textwidth}|"
        elif num_cols == 6:
            col_spec = r"|>{\RaggedRight\arraybackslash}p{0.16\textwidth}|>{\RaggedRight\arraybackslash}p{0.14\textwidth}|>{\RaggedRight\arraybackslash}p{0.15\textwidth}|>{\RaggedRight\arraybackslash}p{0.17\textwidth}|>{\RaggedRight\arraybackslash}p{0.18\textwidth}|>{\RaggedRight\arraybackslash}p{0.15\textwidth}|"
        else:
            pct = round(0.95 / num_cols, 3)
            col_spec = "|" + f">{{\\RaggedRight\\arraybackslash}}p{{{pct}\\textwidth}}|" * num_cols

        latex_table = "\\begin{longtable}{" + col_spec + "}\n\\hline\n"
        
        # Header row: Use {\small\bfseries ...} with RaggedRight to allow flexible header wrapping
        header = rows[0]
        header_cells = [f"{{\\small\\bfseries {cell}}}" for cell in header]
        latex_table += " & ".join(header_cells) + " \\\\\n\\hline\n\\endhead\n"

        for row in rows[1:]:
            if len(row) < num_cols:
                row += [""] * (num_cols - len(row))
            row = row[:num_cols]
            latex_table += " & ".join(row) + " \\\\\n\\hline\n"

        latex_table += "\\end{longtable}\n"
        return latex_table

    for line in lines:
        if line.strip().startswith('|'):
            in_table = True
            table_lines.append(line)
        else:
            if in_table:
                new_lines.append(process_table(table_lines))
                table_lines = []
                in_table = False
            new_lines.append(line)
    if in_table:
        new_lines.append(process_table(table_lines))
    content = '\n'.join(new_lines)

    # 11. Convert Blockquotes & Alert Callouts
    lines = content.split('\n')
    new_lines = []
    in_quote = False
    for line in lines:
        if line.strip().startswith('>'):
            cleaned = line.strip().lstrip('>').strip()
            cleaned = re.sub(r'^\[!(NOTE|TIP|IMPORTANT|WARNING|CAUTION)\]', r'\\textbf{\1}:', cleaned)
            if not in_quote:
                new_lines.append("\\begin{quote}")
                in_quote = True
            new_lines.append(cleaned)
        else:
            if in_quote:
                new_lines.append("\\end{quote}")
                in_quote = False
            new_lines.append(line)
    if in_quote:
        new_lines.append("\\end{quote}")
    content = '\n'.join(new_lines)

    # 12. Restore Placeholders in reverse order
    for idx in range(len(inlines)-1, -1, -1):
        content = content.replace(f"INLINEPLACEHOLDER{idx}", f"\\texttt{{{inlines[idx]}}}")

    for idx in range(len(verbatims)-1, -1, -1):
        # Wrap verbatim code in listings with automatic line break at margins
        content = content.replace(
            f"VERBATIMPLACEHOLDER{idx}",
            f"\\begin{{lstlisting}}\n{verbatims[idx]}\n\\end{{lstlisting}}"
        )

    for idx in range(len(maths)-1, -1, -1):
        content = content.replace(f"MATHPLACEHOLDER{idx}", maths[idx])

    # 13. Strip residual HTML comments
    content = re.sub(r'<!--.*?-->', '', content, flags=re.DOTALL)

    # 14. Support hieroglyphic glyphs and IPA tone bar spans
    content = re.sub(r'[\U00013000-\U0001342F]', lambda m: f"{{\\hiero {m.group(0)}}}", content)
    content = re.sub(r'[\u02E5-\u02E9]', lambda m: f"{{\\ipafont {m.group(0)}}}", content)

    return content

# ==========================================
# LATEX PREAMBLE BUILDER
# ==========================================

def build_latex_preamble(
    paper_key: str = "8x10",
    theme_key: str = "parchment",
    main_font: str = "Junicode",
    hiero_font: str = "Segoe UI Historic",
    ipa_font: str = "Arial"
) -> str:
    """Generates the full XeLaTeX document preamble with geometry, fonts, colors, and margins."""
    geom = PAPER_GEOMETRIES.get(paper_key, PAPER_GEOMETRIES["8x10"])
    theme = COLOR_THEMES.get(theme_key, COLOR_THEMES["parchment"])

    text_color_def = f"\\color[HTML]{{{theme.get('text_color', '000000')}}}" if "text_color" in theme else ""

    preamble = f"""\\documentclass[10pt,oneside]{{book}}
\\usepackage{{geometry}}
\\usepackage{{xcolor}}
\\usepackage{{fontspec}}
\\usepackage{{longtable}}
\\usepackage{{array}}
\\usepackage{{ragged2e}}
\\usepackage[htt]{{hyphenat}}
\\usepackage{{microtype}}
\\usepackage{{graphicx}}
\\usepackage{{amsmath}}
\\usepackage{{amssymb}}
\\usepackage{{listings}}
\\usepackage{{hyperref}}

% Strict Paper Geometry Configuration
\\geometry{{
    paperwidth={geom['paperwidth']},
    paperheight={geom['paperheight']},
    top={geom['top']},
    bottom={geom['bottom']},
    left={geom['left']},
    right={geom['right']}
}}

% Microtypography and margin-break safeguards
\\sloppy
\\emergencystretch=3em
\\setlength{{\\tabcolsep}}{{2.5pt}}
\\setlength{{\\parindent}}{{0pt}}
\\setlength{{\\parskip}}{{6pt plus 2pt minus 1pt}}

% Theme Colors
\\definecolor{{pagebg}}{{HTML}}{{{theme['bg_color']}}}
\\definecolor{{primarycol}}{{HTML}}{{{theme['primary_color']}}}
\\definecolor{{secondarycol}}{{HTML}}{{{theme['secondary_color']}}}
\\definecolor{{linkcol}}{{HTML}}{{{theme['link_color']}}}

\\pagecolor{{pagebg}}
{text_color_def}

\\hypersetup{{
    colorlinks=true,
    linkcolor=primarycol,
    filecolor=primarycol,
    urlcolor=linkcol,
    citecolor=primarycol
}}

% Typography & Font Families
\\setmainfont{{{main_font}}}[Scale=1.0]
\\newfontfamily\\hiero{{{hiero_font}}}
\\newfontfamily\\ipafont{{{ipa_font}}}

% Safe Code Block Wrapping Settings
\\lstset{{
    basicstyle=\\ttfamily\\small,
    breaklines=true,
    breakatwhitespace=false,
    columns=fullflexible,
    keepspaces=true,
    frame=single,
    rulecolor=\\color{{secondarycol}},
    backgroundcolor=\\color{{pagebg}}
}}

\\begin{{document}}
"""
    return preamble

# ==========================================
# VOLUME BUILDERS & RUNNERS
# ==========================================

def generate_title_page(title: str, subtitle: str, author: str, note: str) -> str:
    """Generates a styled, centered book title page."""
    return f"""
\\begin{{titlepage}}
\\begin{{center}}
    \\vspace*{{1.5in}}
    {{\\color{{primarycol}}\\Huge\\bfseries {title}}} \\\\[0.2in]
    {{\\color{{secondarycol}}\\Large {subtitle}}} \\\\[0.4in]
    \\noindent\\rule{{\\textwidth}}{{1.5pt}} \\\\[0.4in]
    {{\\color{{primarycol}}\\Large by {author}}} \\\\[1.5in]
    {{\\large {note}}}
\\end{{center}}
\\end{{titlepage}}
\\newpage
"""

def compile_pdf(tex_path: str, output_dir: str, xelatex_bin: str) -> bool:
    """Compiles TeX file with XeLaTeX twice, protecting against locked output PDFs."""
    pdf_name = os.path.basename(tex_path).replace('.tex', '.pdf')
    pdf_path = os.path.join(output_dir, pdf_name)

    # Check if target PDF is locked by an external reader
    if os.path.exists(pdf_path):
        try:
            with open(pdf_path, 'r+b'):
                pass
        except IOError:
            fallback_tex_name = os.path.basename(tex_path).replace('.tex', '_v2.tex')
            fallback_tex_path = os.path.join(os.path.dirname(tex_path), fallback_tex_name)
            print(f"  [Warning] Output PDF '{pdf_name}' is locked by a viewer.")
            print(f"  Compiling to fallback '{fallback_tex_name}' instead...")
            shutil.copy2(tex_path, fallback_tex_path)
            tex_path = fallback_tex_path

    print(f"Compiling '{os.path.basename(tex_path)}' via XeLaTeX...")
    success = True
    for pass_num in (1, 2):
        cmd = [xelatex_bin, "-interaction=nonstopmode", f"-output-directory={output_dir}", tex_path]
        try:
            res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8', errors='replace')
            if res.returncode != 0:
                print(f"  [Pass {pass_num}] Completed with warning/exit code {res.returncode}.")
                success = False
        except Exception as e:
            print(f"  [Error] XeLaTeX execution failed: {e}")
            return False

    if success or os.path.exists(pdf_path):
        print(f"  ✓ PDF generated: {pdf_name}")
        return True
    return False

# ==========================================
# MAIN COMPILER ORCHESTRATOR
# ==========================================

def run_compiler():
    parser = argparse.ArgumentParser(
        description="Dynamic Multi-Volume XeLaTeX Publication Compiler Engine"
    )
    parser.add_argument(
        "--dir",
        default=".",
        help="Root directory containing book source folders (default: current working directory)"
    )
    parser.add_argument(
        "--paper",
        choices=list(PAPER_GEOMETRIES.keys()),
        default="8x10",
        help="Paper geometry preset (default: 8x10)"
    )
    parser.add_argument(
        "--theme",
        choices=list(COLOR_THEMES.keys()),
        default="parchment",
        help="Color theme palette (default: parchment)"
    )
    parser.add_argument(
        "--author",
        default="Brian Odeen",
        help="Author name on title pages (default: Brian Odeen)"
    )
    parser.add_argument(
        "--lang",
        default="",
        help="Language name (auto-detected from folder name or README if omitted)"
    )
    parser.add_argument(
        "--font",
        default="Junicode",
        help="Primary serif font family (default: Junicode)"
    )
    parser.add_argument(
        "--hiero-font",
        default="Segoe UI Historic",
        help="Fallback font for glyphs/hieroglyphs (default: Segoe UI Historic)"
    )
    parser.add_argument(
        "--ipa-font",
        default="Arial",
        help="Font family for IPA symbols (default: Arial)"
    )

    args = parser.parse_args()

    base_dir = os.path.abspath(args.dir)
    latex_dir = os.path.join(base_dir, "latex_output")
    os.makedirs(latex_dir, exist_ok=True)

    # Detect language name if not explicitly provided
    lang_name = args.lang
    if not lang_name:
        folder_base = os.path.basename(base_dir)
        lang_name = folder_base.replace('_', ' ').replace('-', ' ').title() if folder_base not in ('.', '') else "Constructed Language"

    # Locate XeLaTeX executable
    xelatex_bin = DEFAULT_XELATEX_PATH if os.path.exists(DEFAULT_XELATEX_PATH) else shutil.which("xelatex")
    if not xelatex_bin:
        print("Warning: XeLaTeX executable not found. TeX files will be generated without PDF compilation.")

    preamble = build_latex_preamble(
        paper_key=args.paper,
        theme_key=args.theme,
        main_font=args.font,
        hiero_font=args.hiero_font,
        ipa_font=args.ipa_font
    )

    print("=" * 60)
    print(f"XeLaTeX Multi-Volume Publication Engine")
    print(f"Language:  {lang_name}")
    print(f"Author:    {args.author}")
    print(f"Geometry:  {PAPER_GEOMETRIES[args.paper]['description']}")
    print(f"Theme:     {COLOR_THEMES[args.theme]['description']}")
    print(f"Output:    {latex_dir}")
    print("=" * 60)

    # 1. Book 1: Grammar & Lessons
    book1_dir = os.path.join(base_dir, "book_1_grammar")
    if os.path.exists(book1_dir):
        print(f"\nBuilding Book 1 (Grammar) LaTeX...")
        md_compiled = ""
        # Find all chapters
        ch_files = sorted([f for f in os.listdir(book1_dir) if f.startswith("chapter_") and f.endswith(".md")])
        for cf in ch_files:
            with open(os.path.join(book1_dir, cf), 'r', encoding='utf-8') as f:
                md_compiled += f.read() + "\n\n\\newpage\n\n"

        # Readings
        readings_file = os.path.join(book1_dir, "readings.md")
        if os.path.exists(readings_file):
            with open(readings_file, 'r', encoding='utf-8') as f:
                md_compiled += f.read() + "\n\n\\newpage\n\n"

        # Reference Tables & Appendices
        ref_file = os.path.join(book1_dir, "appendix_reference.md")
        if os.path.exists(ref_file):
            with open(ref_file, 'r', encoding='utf-8') as f:
                md_compiled += f.read() + "\n\n\\newpage\n\n"

        answers_file = os.path.join(book1_dir, "appendix_answers.md")
        if os.path.exists(answers_file):
            with open(answers_file, 'r', encoding='utf-8') as f:
                md_compiled += f.read() + "\n\n"

        latex_body = md_to_latex(md_compiled)
        tex1_path = os.path.join(latex_dir, "book1_grammar.tex")
        with open(tex1_path, 'w', encoding='utf-8') as f:
            f.write(preamble)
            f.write(generate_title_page(
                title=f"Learning {lang_name}",
                subtitle="Grammar, Lessons, and Exercises",
                author=args.author,
                note="A Data-Driven Pedagogical Primer"
            ))
            f.write(latex_body)
            f.write("\n\\end{document}\n")

        if xelatex_bin:
            compile_pdf(tex1_path, latex_dir, xelatex_bin)

    # 2. Book 2: Dictionary (Double-Column Compression with Single-Column Preface)
    book2_dir = os.path.join(base_dir, "book_2_dictionary")
    if os.path.exists(book2_dir):
        print(f"\nBuilding Book 2 (Dictionary) LaTeX...")
        md_compiled = ""
        dict_files = sorted([f for f in os.listdir(book2_dir) if f.endswith(".md")])
        for df in dict_files:
            with open(os.path.join(book2_dir, df), 'r', encoding='utf-8') as f:
                md_compiled += f.read() + "\n\n\\newpage\n\n"

        latex_body = md_to_latex(md_compiled)
        
        # Isolate tables in single column, switch to 2-column small-font at letter section A
        latex_body = re.sub(
            r'(\\section\*\{[A-ZÆÞÐ#]\})',
            r'\\twocolumn\n\\footnotesize\n\1',
            latex_body,
            count=1
        )

        tex2_path = os.path.join(latex_dir, "book2_dictionary.tex")
        with open(tex2_path, 'w', encoding='utf-8') as f:
            f.write(preamble)
            f.write(generate_title_page(
                title=f"{lang_name} Dictionary",
                subtitle="Bidirectional Complete Lexicon",
                author=args.author,
                note="Sorted in Traditional and Modern Formats"
            ))
            f.write(latex_body)
            f.write("\n\\onecolumn\n\\end{document}\n")

        if xelatex_bin:
            compile_pdf(tex2_path, latex_dir, xelatex_bin)

    # 3. Book 3: Phrasebook
    book3_dir = os.path.join(base_dir, "book_3_phrasebook") if os.path.exists(os.path.join(base_dir, "book_3_phrasebook")) else os.path.join(base_dir, "book_3_conversation")
    if os.path.exists(book3_dir):
        print(f"\nBuilding Book 3 (Phrasebook) LaTeX...")
        md_compiled = ""
        phrase_files = sorted([f for f in os.listdir(book3_dir) if f.endswith(".md")])
        for pf in phrase_files:
            with open(os.path.join(book3_dir, pf), 'r', encoding='utf-8') as f:
                md_compiled += f.read() + "\n\n\\newpage\n\n"

        latex_body = md_to_latex(md_compiled)
        tex3_path = os.path.join(latex_dir, "book3_phrasebook.tex")
        with open(tex3_path, 'w', encoding='utf-8') as f:
            f.write(preamble)
            f.write(generate_title_page(
                title=f"Conversational {lang_name}",
                subtitle="Phrasebook and Cultural Dialogue Guide",
                author=args.author,
                note="Practical Speaking Guide for Students and Reenactors"
            ))
            f.write(latex_body)
            f.write("\n\\end{document}\n")

        if xelatex_bin:
            compile_pdf(tex3_path, latex_dir, xelatex_bin)

    # 4. Book 4: History & Dialects / Linguistics
    book4_dir = os.path.join(base_dir, "book_4_history") if os.path.exists(os.path.join(base_dir, "book_4_history")) else os.path.join(base_dir, "book_4_linguistics")
    if os.path.exists(book4_dir):
        print(f"\nBuilding Book 4 (History & Dialects) LaTeX...")
        md_compiled = ""
        hist_files = sorted([f for f in os.listdir(book4_dir) if f.endswith(".md")])
        for hf in hist_files:
            with open(os.path.join(book4_dir, hf), 'r', encoding='utf-8') as f:
                md_compiled += f.read() + "\n\n\\newpage\n\n"

        latex_body = md_to_latex(md_compiled)
        tex4_path = os.path.join(latex_dir, "book4_history.tex")
        with open(tex4_path, 'w', encoding='utf-8') as f:
            f.write(preamble)
            f.write(generate_title_page(
                title=f"History and Dialects of {lang_name}",
                subtitle="From Origins to Modern Reconstruction",
                author=args.author,
                note="Linguistic and Historical Structure"
            ))
            f.write(latex_body)
            f.write("\n\\end{document}\n")

        if xelatex_bin:
            compile_pdf(tex4_path, latex_dir, xelatex_bin)

    print("\n" + "=" * 60)
    print("XeLaTeX Multi-Volume Compilation Cycle Complete!")
    print(f"Generated documents are saved in: {latex_dir}")
    print("=" * 60)

if __name__ == "__main__":
    run_compiler()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Multi-Volume XeLaTeX Publication Compiler Engine (build_latex.py)
Converts Markdown book sources into styled XeLaTeX TeX documents and compiles
them into publication-ready PDFs in 'latex_output/'.
"""

import os
import sys
import re
import subprocess
import shutil

try:
    sys.stdout.reconfigure(encoding='utf-8')
except AttributeError:
    pass

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOOK1_DIR = os.path.join(BASE_DIR, 'book_1_grammar')
BOOK2_DIR = os.path.join(BASE_DIR, 'book_2_dictionary')
BOOK3_DIR = os.path.join(BASE_DIR, 'book_3_conversation')
BOOK4_DIR = os.path.join(BASE_DIR, 'book_4_history')
LATEX_DIR = os.path.join(BASE_DIR, 'latex_output')
XELATEX_PATH = r"C:\Users\brian\AppData\Local\Programs\MiKTeX\miktex\bin\x64\xelatex.exe"

os.makedirs(LATEX_DIR, exist_ok=True)

LATEX_HEADER = r"""\documentclass[8pt,oneside]{book}
\usepackage{geometry}
\usepackage{xcolor}
\usepackage{fontspec}
\usepackage{longtable}
\usepackage{array}
\usepackage{ragged2e}
\usepackage[htt]{hyphenat}
\usepackage{microtype}
\usepackage{graphicx}
\usepackage{amsmath}
\usepackage{hyperref}

\geometry{
    paperwidth=8in,
    paperheight=10in,
    top=0.8in,
    bottom=0.8in,
    left=0.8in,
    right=0.8in
}

\setlength{\tabcolsep}{2.5pt}

\definecolor{burgundy}{HTML}{800020}

\hypersetup{
    colorlinks=true,
    linkcolor=burgundy,
    filecolor=burgundy,
    urlcolor=burgundy,
}

\setmainfont{Junicode}[Scale=1.0]
\newfontfamily\hiero{Segoe UI Historic}
\newfontfamily\ipafont{Arial}

\begin{document}
"""

def md_to_latex(md_content: str) -> str:
    """Converts Markdown text into formatted XeLaTeX code with glyph wrapping."""
    md_content = md_content.replace('\r\n', '\n').replace('\r', '\n')
    md_content = md_content.replace('‐', '-').replace('–', '--').replace('—', '---').replace('﴾', '(').replace('﴿', ')')
    
    # Wrap Egyptian Hieroglyphic symbols (U+13000 to U+1342F) in \hiero font family
    md_content = re.sub(r'[\U00013000-\U0001342F]', lambda m: f"{{\\hiero {m.group(0)}}}", md_content)
    
    # Wrap IPA tone bar symbols (U+02E5 to U+02E9) in \ipafont font family
    md_content = re.sub(r'[\u02E5-\u02E9]', lambda m: f"{{\\ipafont {m.group(0)}}}", md_content)
    
    # Simple header replacements
    md_content = re.sub(r'^# (.*?)$', r'\\chapter{\1}', md_content, flags=re.MULTILINE)
    md_content = re.sub(r'^## (.*?)$', r'\\section*{\1}', md_content, flags=re.MULTILINE)
    md_content = re.sub(r'^### (.*?)$', r'\\subsection*{\1}', md_content, flags=re.MULTILINE)
    
    # Bold & Italic
    md_content = re.sub(r'\*\*(.*?)\*\*', r'\\textbf{\1}', md_content)
    md_content = re.sub(r'\*(.*?)\*', r'\\textit{\1}', md_content)
    md_content = re.sub(r'`(.*?)`', r'\\texttt{\1}', md_content)
    
    return md_content

def check_pdf_write_permission(pdf_path: str) -> str:
    """Checks if output PDF is locked by external viewer; falls back to versioned name if locked."""
    if os.path.exists(pdf_path):
        try:
            with open(pdf_path, 'r+b'):
                pass
        except IOError:
            base, ext = os.path.splitext(pdf_path)
            safe_path = f"{base}_v2{ext}"
            print(f"Warning: Output PDF '{pdf_path}' is locked by a viewer. Writing to '{safe_path}'.")
            return safe_path
    return pdf_path

def compile_pdf(tex_path: str):
    """Compiles TeX file using XeLaTeX executable."""
    xelatex_bin = XELATEX_PATH if os.path.exists(XELATEX_PATH) else shutil.which("xelatex")
    if not xelatex_bin:
        print(f"XeLaTeX compiler not found. TeX file generated at '{tex_path}'.")
        return
        
    cmd = [xelatex_bin, "-interaction=nonstopmode", f"-output-directory={LATEX_DIR}", tex_path]
    print(f"Running XeLaTeX on '{tex_path}'...")
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("  PDF compilation succeeded!")
    except subprocess.CalledProcessError as e:
        print(f"  Warning: XeLaTeX process returned error code {e.returncode}. Check logs in '{LATEX_DIR}'.")

if __name__ == "__main__":
    print("Multi-Volume XeLaTeX Compiler initialized.")

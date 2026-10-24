# -*- coding: utf-8 -*-
'''
report_generator.py - Generateur du document PDF officiel pour Mr Sarobidy
'''
import os
import sys

# Assurer l'acces aux packages du projet
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.report.builder import build_pdf_report

def main():
    pdf_path = build_pdf_report()
    print(f"[+] Document PDF genere avec succes : {pdf_path}")
    return 0

if __name__ == "__main__":
    sys.exit(main())

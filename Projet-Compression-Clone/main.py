# -*- coding: utf-8 -*-
'''
main.py - Lanceur Universel de la Suite de Compression Clone
Supporte : bzip2, lzma, 7-zip, benchmark, report, gui
'''

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

def print_help():
    print("""
========================================================================
   SUITE DE COMPRESSION UNIVERSELLE : bzip2 • lzma • 7-zip (CLONE)
   Auteur : Projet Compression 2026
========================================================================

Usage :
  python main.py <commande> [arguments...]

Commandes disponibles :
  bzip2      : Execute le clone GNU bzip2 (BWT + Huffman)
               Exemple: python main.py bzip2 -v -k fichier.txt

  lzma       : Execute le clone LZMA/XZ (Lempel-Ziv-Markov + Range Coder)
               Exemple: python main.py lzma -v -k fichier.txt

  7z         : Execute le clone Igor Pavlov 7-Zip (LZMA2 / Archive conteneur)
               Exemple: python main.py 7z a archive.7z dossier/

  benchmark  : Execute le benchmark complet sur les 4 types (Texte, Audio, Image, Video)
               et genere les graphiques comparatifs.

  report     : Compile et genere le document PDF officiel du devoir.

  gui        : Lance l'interface graphique interactive (Desktop Tkinter/TTK).

  help       : Affiche ce message d'aide.
========================================================================
""")

def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help", "help"):
        print_help()
        return 0

    subcommand = sys.argv[1].lower()
    sub_args = sys.argv[2:]

    if subcommand in ("bzip2", "bunzip2"):
        import src.bzip2_clone as bz_module
        return bz_module.main(sub_args)

    elif subcommand in ("lzma", "unlzma", "xz"):
        import src.lzma_clone as lz_module
        return lz_module.main(sub_args)

    elif subcommand in ("7z", "7za", "sevenzip"):
        import src.sevenzip_clone as sz_module
        return sz_module.main(sub_args)

    elif subcommand == "benchmark":
        from src.benchmark.run_benchmark import run_full_benchmark
        from src.benchmark.generate_charts import generate_all_charts
        run_full_benchmark()
        generate_all_charts()
        print("\n[+] Benchmark et generation des graphiques termines avec succes.")
        return 0

    elif subcommand == "report":
        from src.report_generator import build_pdf_report
        pdf_path = build_pdf_report()
        print(f"\n[+] Document PDF genere avec succes : {pdf_path}")
        return 0

    elif subcommand == "gui":
        from src.gui.app import launch
        launch()
        return 0

    else:
        print(f"Commande inconnue: {subcommand}")
        print_help()
        return 1

if __name__ == "__main__":
    sys.exit(main())

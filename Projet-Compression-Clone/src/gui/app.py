# -*- coding: utf-8 -*-
'''
app.py - Interface Graphique Moderne pour le Clone des Utilitaires de Compression
Supporte bzip2, lzma et 7-zip avec visualisation des benchmarks et graphiques.
'''

import os
import sys
import time
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk

# Import des modules de compression
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
import src.bzip2_clone as bzip2_clone
import src.lzma_clone as lzma_clone
import src.sevenzip_clone as sevenzip_clone
from src.core.metrics import format_size, calculate_file_entropy, calculate_sha256

class CompressionCloneApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Clone Suite de Compression : bzip2 | lzma | 7-zip - Examen 2026")
        self.geometry("1020x720")
        self.minsize(900, 650)
        self.configure(bg="#f4f6f9")

        # Style TTK
        self.style = ttk.Style()
        try:
            self.style.theme_use("clam")
        except:
            pass

        self.setup_ui()

    def setup_ui(self):
        # Header banner
        header = tk.Frame(self, bg="#1e3a8a", height=70)
        header.pack(fill=tk.X, side=tk.TOP)
        header.pack_propagate(False)

        title_lbl = tk.Label(header, text="COMPRESSION SUITE : bzip2 • lzma • 7-zip",
                             fg="white", bg="#1e3a8a", font=("Segoe UI", 16, "bold"))
        title_lbl.pack(side=tk.LEFT, padx=20, pady=10)

        sub_lbl = tk.Label(header, text="Clone Fonctionnel Universitaire • Auteur: Etudiant • Rendu: 24/10/2026",
                           fg="#bfdbfe", bg="#1e3a8a", font=("Segoe UI", 10))
        sub_lbl.pack(side=tk.RIGHT, padx=20, pady=15)

        # Notebook (Onglets)
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        # Tab 1: Operations de Compression / Décompression
        self.tab_ops = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_ops, text="  Operations de Compression  ")
        self.build_tab_ops()

        # Tab 2: Benchmark Comparatif & Graphiques
        self.tab_bench = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_bench, text="  Benchmark des 4 Types de Fichiers  ")
        self.build_tab_bench()

        # Tab 3: Pedagogie & Algorithmes
        self.tab_algo = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_algo, text="  Architecture Algorithmique  ")
        self.build_tab_algo()

        # Tab 4: Soumission & Informations
        self.tab_about = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_about, text="  Soumission & Depot GitHub  ")
        self.build_tab_about()

    def build_tab_ops(self):
        # Section selection fichier
        frame_file = ttk.LabelFrame(self.tab_ops, text=" 1. Selection du Fichier ou Dossier ", padding=15)
        frame_file.pack(fill=tk.X, padx=15, pady=10)

        self.var_filepath = tk.StringVar()
        entry_file = ttk.Entry(frame_file, textvariable=self.var_filepath, font=("Segoe UI", 10))
        entry_file.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))

        btn_browse_f = ttk.Button(frame_file, text="Parcourir Fichier...", command=self.browse_file)
        btn_browse_f.pack(side=tk.LEFT, padx=5)

        btn_browse_d = ttk.Button(frame_file, text="Parcourir Dossier (7z)...", command=self.browse_dir)
        btn_browse_d.pack(side=tk.LEFT, padx=5)

        # Section paramètres
        frame_params = ttk.LabelFrame(self.tab_ops, text=" 2. Parametres de l'Outil ", padding=15)
        frame_params.pack(fill=tk.X, padx=15, pady=10)

        # Outil selectionné
        lbl_tool = ttk.Label(frame_params, text="Utilitaire:", font=("Segoe UI", 10, "bold"))
        lbl_tool.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)

        self.var_tool = tk.StringVar(value="7-zip")
        tools_combo = ttk.Combobox(frame_params, textvariable=self.var_tool, values=["7-zip", "lzma", "bzip2"], state="readonly", width=15)
        tools_combo.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)

        # Action (Compresser, Decompresser, Tester)
        lbl_act = ttk.Label(frame_params, text="Action:", font=("Segoe UI", 10, "bold"))
        lbl_act.grid(row=0, column=2, sticky=tk.W, padx=(20, 5), pady=5)

        self.var_action = tk.StringVar(value="compresser")
        rb_comp = ttk.Radiobutton(frame_params, text="Compresser", variable=self.var_action, value="compresser")
        rb_decomp = ttk.Radiobutton(frame_params, text="Decompresser", variable=self.var_action, value="decompresser")
        rb_test = ttk.Radiobutton(frame_params, text="Tester Integrite", variable=self.var_action, value="tester")
        rb_comp.grid(row=0, column=3, padx=5)
        rb_decomp.grid(row=0, column=4, padx=5)
        rb_test.grid(row=0, column=5, padx=5)

        # Niveau de compression
        lbl_lvl = ttk.Label(frame_params, text="Niveau de compression (1-9):", font=("Segoe UI", 10))
        lbl_lvl.grid(row=1, column=0, sticky=tk.W, padx=5, pady=10)

        self.var_level = tk.IntVar(value=9)
        slider_lvl = ttk.Scale(frame_params, from_=1, to=9, variable=self.var_level, orient=tk.HORIZONTAL)
        slider_lvl.grid(row=1, column=1, columnspan=2, sticky="ew", padx=5, pady=10)
        self.lbl_level_val = ttk.Label(frame_params, text="9 (Ultra/Best)")
        self.lbl_level_val.grid(row=1, column=3, sticky=tk.W, padx=5)
        slider_lvl.config(command=lambda v: self.lbl_level_val.config(text=f"{int(float(v))} ({'Best' if int(float(v))>=9 else ('Fast' if int(float(v))<=2 else 'Normal')})"))

        # Bouton d'action principal
        btn_run = tk.Button(self.tab_ops, text=" EXECUTER L'OPERATION ", bg="#2563eb", fg="white",
                            font=("Segoe UI", 11, "bold"), relief=tk.FLAT, padx=20, pady=8, command=self.run_operation)
        btn_run.pack(pady=10)

        # Zone de resultats et logs
        frame_logs = ttk.LabelFrame(self.tab_ops, text=" Journal d'Execution et Metriques ", padding=10)
        frame_logs.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)

        self.txt_logs = tk.Text(frame_logs, height=10, bg="#1e293b", fg="#f8fafc", font=("Consolas", 10), insertbackground="white")
        self.txt_logs.pack(fill=tk.BOTH, expand=True)

    def build_tab_bench(self):
        top_frame = ttk.Frame(self.tab_bench, padding=10)
        top_frame.pack(fill=tk.X)

        btn_run_bench = tk.Button(top_frame, text=" Lancer le Benchmark Complet (4 Fichiers) ",
                                  bg="#059669", fg="white", font=("Segoe UI", 11, "bold"),
                                  padx=15, pady=6, relief=tk.FLAT, command=self.run_gui_benchmark)
        btn_run_bench.pack(side=tk.LEFT, padx=10)

        self.lbl_bench_status = ttk.Label(top_frame, text="Pret pour le benchmark.", font=("Segoe UI", 10, "italic"))
        self.lbl_bench_status.pack(side=tk.LEFT, padx=15)

        # Notebook d'onglets pour visualiser les graphiques
        self.nb_charts = ttk.Notebook(self.tab_bench)
        self.nb_charts.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.tab_c1 = ttk.Frame(self.nb_charts)
        self.tab_c2 = ttk.Frame(self.nb_charts)
        self.tab_c3 = ttk.Frame(self.nb_charts)
        self.tab_c4 = ttk.Frame(self.nb_charts)

        self.nb_charts.add(self.tab_c1, text="Gain d'Espace (%)")
        self.nb_charts.add(self.tab_c2, text="Tailles Comparees (MB)")
        self.nb_charts.add(self.tab_c3, text="Debits (MB/s)")
        self.nb_charts.add(self.tab_c4, text="Entropie de Shannon")

        self.load_charts_into_tabs()

    def load_charts_into_tabs(self):
        '''Charge les images des graphiques dans les onglets.'''
        charts = [
            (self.tab_c1, "screenshots/chart_space_saving.png"),
            (self.tab_c2, "screenshots/chart_file_sizes.png"),
            (self.tab_c3, "screenshots/chart_speeds.png"),
            (self.tab_c4, "screenshots/chart_entropy.png"),
        ]
        self.chart_images = []
        for tab, path in charts:
            for widget in tab.winfo_children():
                widget.destroy()
            if os.path.exists(path):
                try:
                    img = Image.open(path)
                    # Redimensionnement adaptatif
                    img.thumbnail((880, 480), Image.Resampling.LANCZOS)
                    tk_img = ImageTk.PhotoImage(img)
                    self.chart_images.append(tk_img)
                    lbl = ttk.Label(tab, image=tk_img)
                    lbl.pack(expand=True, pady=10)
                except Exception as e:
                    ttk.Label(tab, text=f"Erreur d'affichage: {e}").pack(pady=20)
            else:
                ttk.Label(tab, text="Graphique non genere. Cliquez sur 'Lancer le Benchmark Complet'.").pack(pady=20)

    def build_tab_algo(self):
        container = ttk.Frame(self.tab_algo, padding=20)
        container.pack(fill=tk.BOTH, expand=True)

        txt = (
            "ARCHITECTURE ALGORITHMIQUE DES UTILITAIRES DE COMPRESSION\n"
            "=" * 70 + "\n\n"
            "1. bzip2 (Julian Seward - 1996) :\n"
            "   • Pipeline : RLE-1 -> BWT (Burrows-Wheeler Transform) -> MTF (Move-to-Front) -> RLE-2 -> Codage Huffman.\n"
            "   • Force : Ne recherche pas des chaines identiques comme les algorithmes LZ77,\n"
            "     mais permute le bloc pour regrouper les octets ayant le meme contexte gauche.\n"
            "   • Cas optimal : Fichiers texte, code source, donnees structurees avec forte redondance contextuelle.\n\n"
            "2. LZMA (Igor Pavlov - 1998) :\n"
            "   • Pipeline : Lempel-Ziv sliding dictionary (jusqu'a 64MB / 1GB) + Range Coder binaire avec tables de probabilites.\n"
            "   • Force : Ratio de compression exceptionnel, dictionnaire tres etendu et codeur arithmetique/par intervalles.\n"
            "   • Format : Conteneur standard moderne .xz (avec controle CRC64) ou flux brut .lzma.\n\n"
            "3. 7-Zip (Igor Pavlov - 1999) :\n"
            "   • Architecture conteneur modulaire multi-filtres.\n"
            "   • Algorithme par defaut : LZMA2 (decoupage en blocs independants, multi-coeur et gestion des flux incompressibles).\n"
            "   • Fonctionnalites : Archivage multi-fichiers 'Solid', chiffrement fort AES-256 de l'en-tete et du corps,\n"
            "     filtres BCJ pour executables x86/ARM, compression multi-algorithmes (BZip2, PPMd, Deflate).\n"
        )

        lbl_algo = tk.Text(container, bg="#ffffff", fg="#1e293b", font=("Consolas", 10), wrap=tk.WORD, relief=tk.SOLID, borderwidth=1, padx=15, pady=15)
        lbl_algo.insert(tk.END, txt)
        lbl_algo.config(state=tk.DISABLED)
        lbl_algo.pack(fill=tk.BOTH, expand=True)

    def build_tab_about(self):
        container = ttk.Frame(self.tab_about, padding=25)
        container.pack(fill=tk.BOTH, expand=True)

        card = ttk.LabelFrame(container, text=" Fiche d'Evaluation de l'Examen ", padding=20)
        card.pack(fill=tk.BOTH, expand=True)

        info_text = (
            "PROJET D'EXAMEN : CLONE FONCTIONNEL DE BZIP2, LZMA ET 7-ZIP\n\n"
            "• Livrables Attendus :\n"
            "  1. Code source complet accessible sur le depot GitHub\n"
            "  2. Document PDF professionnel incluant captures d'ecran et comparatifs sur 4 types de donnees (Texte, Audio, Image, Video)\n\n"
            "• Destinataire de l'evaluation :\n"
            "  Email : lucsarobidynomenjanahary@gmail.com (Mr Sarobidy)\n\n"
            "• Date limite de soumission :\n"
            "  Samedi 24 octobre 2026 a 23h59\n\n"
            "• Localisation du projet sur la machine locale :\n"
            f"  {os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))}\n\n"
            "• Depot GitHub :\n"
            "  https://github.com/tsiory-bainga/clone-compression-bzip2-lzma-7zip\n"
        )

        lbl_info = tk.Text(card, bg="#f8fafc", fg="#0f172a", font=("Segoe UI", 11), wrap=tk.WORD, relief=tk.FLAT, padx=10, pady=10)
        lbl_info.insert(tk.END, info_text)
        lbl_info.config(state=tk.DISABLED)
        lbl_info.pack(fill=tk.BOTH, expand=True)

    def browse_file(self):
        f = filedialog.askopenfilename()
        if f:
            self.var_filepath.set(f)

    def browse_dir(self):
        d = filedialog.askdirectory()
        if d:
            self.var_filepath.set(d)

    def log(self, text: str):
        self.txt_logs.insert(tk.END, text + "\n")
        self.txt_logs.see(tk.END)

    def run_operation(self):
        path = self.var_filepath.get().strip()
        if not path or not os.path.exists(path):
            messagebox.showerror("Erreur", "Veuillez selectionner un fichier ou dossier existant.")
            return

        tool = self.var_tool.get()
        action = self.var_action.get()
        level = int(self.var_level.get())

        self.log(f"\n[+] Operation demandee : {action.upper()} avec {tool} (Niveau {level})")
        self.log(f"    Cible : {path}")

        def worker():
            try:
                t0 = time.time()
                if action == "compresser":
                    if tool == "bzip2":
                        dst = path + ".bz2"
                        ok = bzip2_clone.compress_file(path, dst_path=dst, compresslevel=level, keep=True, force=True)
                    elif tool == "lzma":
                        dst = path + ".xz"
                        ok = lzma_clone.compress_file(path, dst_path=dst, preset=level, keep=True, force=True)
                    elif tool == "7-zip":
                        dst = path + ".7z"
                        ok = sevenzip_clone.add_to_archive(dst, [path], level=level, method="lzma2")
                    elapsed = time.time() - t0
                    if ok and os.path.exists(dst):
                        orig_sz = os.path.getsize(path) if os.path.isfile(path) else 0
                        comp_sz = os.path.getsize(dst)
                        saving = ((orig_sz - comp_sz) / orig_sz * 100) if orig_sz > 0 else 0
                        self.log(f"SUCCES : Compresse vers {dst}")
                        self.log(f"Metriques : {format_size(orig_sz)} -> {format_size(comp_sz)} | Gain : {saving:.2f}% | Temps : {elapsed:.3f}s")
                    else:
                        self.log(f"ECHEC de l'operation de compression.")

                elif action == "decompresser":
                    if tool == "bzip2":
                        dst = path[:-4] if path.endswith(".bz2") else path + ".decomp"
                        ok = bzip2_clone.decompress_file(path, dst_path=dst, keep=True, force=True)
                    elif tool == "lzma":
                        dst = path[:-3] if path.endswith(".xz") else path + ".decomp"
                        ok = lzma_clone.decompress_file(path, dst_path=dst, keep=True, force=True)
                    elif tool == "7-zip":
                        out_dir = os.path.join(os.path.dirname(path), "extraction_7z")
                        ok = sevenzip_clone.extract_archive(path, output_dir=out_dir)
                    elapsed = time.time() - t0
                    if ok:
                        self.log(f"SUCCES : Decompression terminee avec succes en {elapsed:.3f}s.")
                    else:
                        self.log(f"ECHEC de la decompression.")

                elif action == "tester":
                    if tool == "bzip2":
                        ok = bzip2_clone.test_file_integrity(path, verbose=True)
                    elif tool == "lzma":
                        ok = lzma_clone.test_file_integrity(path, verbose=True)
                    elif tool == "7-zip":
                        ok = sevenzip_clone.test_archive(path)
                    if ok:
                        self.log(f"VERIFICATION INTEGRITE : Fichier 100% Intrege et Valide (CRC OK).")
                    else:
                        self.log(f"ALERTE : Erreur d'integrite detectee !")
            except Exception as e:
                self.log(f"ERREUR : {e}")

        threading.Thread(target=worker, daemon=True).start()

    def run_gui_benchmark(self):
        self.lbl_bench_status.config(text="Benchmark en cours d'execution...")
        def worker():
            from src.benchmark.run_benchmark import run_full_benchmark
            from src.benchmark.generate_charts import generate_all_charts
            run_full_benchmark()
            generate_all_charts()
            self.lbl_bench_status.config(text="Benchmark termine ! Graphiques rafraichis.")
            self.after(500, self.load_charts_into_tabs)
        threading.Thread(target=worker, daemon=True).start()

def launch():
    app = CompressionCloneApp()
    app.mainloop()

if __name__ == "__main__":
    launch()

'''
generate_charts.py
Genere des graphiques comparatifs de qualite professionnelle avec Matplotlib
a partir des resultats du benchmark.
'''

import os
import sys
import json
import matplotlib
matplotlib.use('Agg') # Mode sans affichage direct pour generation d'images
import matplotlib.pyplot as plt
import numpy as np

def generate_all_charts(results_json: str = "src/benchmark/benchmark_results.json", output_dir: str = "screenshots"):
    '''Genere 4 graphiques a integrer dans le PDF et le README.'''
    if not os.path.exists(results_json):
        print(f"Erreur: fichier {results_json} introuvable.")
        return []

    with open(results_json, 'r', encoding='utf-8') as f:
        data = json.load(f)

    os.makedirs(output_dir, exist_ok=True)
    generated_charts = []

    categories = list(data.keys()) # ['texte', 'audio', 'image', 'video']
    cat_labels = [c.capitalize() for c in categories]
    tools = ["bzip2", "lzma", "7-zip"]
    colors = {
        "bzip2": "#2b5c8f",  # Bleu soutenu
        "lzma": "#e67e22",   # Orange
        "7-zip": "#27ae60",  # Vert emeraude
        "orig": "#7f8c8d"    # Gris
    }

    # Données extraites
    saving_data = {t: [] for t in tools}
    comp_size_data = {t: [] for t in tools}
    orig_sizes = []
    speed_data = {t: [] for t in tools}
    decomp_speed_data = {t: [] for t in tools}
    entropy_orig = []

    for cat in categories:
        orig_mb = data[cat]["orig_size"] / (1024 * 1024)
        orig_sizes.append(orig_mb)
        
        benchs = {b["tool"]: b for b in data[cat]["benchmarks"]}
        entropy_orig.append(benchs["bzip2"]["orig_entropy"])
        for t in tools:
            b = benchs[t]
            saving_data[t].append(b["space_saving_percent"])
            comp_size_data[t].append(b["comp_size"] / (1024 * 1024))
            speed_data[t].append(b["speed_mb_s"])
            decomp_speed_data[t].append(b["decomp_speed_mb_s"])

    # Configuration generale du style Matplotlib
    plt.rcParams.update({
        'font.sans-serif': 'Arial',
        'font.family': 'sans-serif',
        'figure.dpi': 200,
        'axes.grid': True,
        'grid.alpha': 0.3,
        'axes.axisbelow': True
    })

    # =========================================================================
    # Graphique 1 : Gain d'espace (% economise)
    # =========================================================================
    fig, ax = plt.subplots(figsize=(10, 6))
    x = np.arange(len(categories))
    width = 0.25

    rects1 = ax.bar(x - width, saving_data["bzip2"], width, label="bzip2 (BWT)", color=colors["bzip2"])
    rects2 = ax.bar(x, saving_data["lzma"], width, label="lzma (LZMA/XZ)", color=colors["lzma"])
    rects3 = ax.bar(x + width, saving_data["7-zip"], width, label="7-zip (LZMA2)", color=colors["7-zip"])

    ax.set_ylabel("Gain d'Espace Economise (%)", fontsize=12, fontweight='bold')
    ax.set_title("Efficacite de la Compression par Type de Fichier (Gain d'Espace)", fontsize=14, fontweight='bold', pad=15)
    ax.set_xticks(x)
    ax.set_xticklabels(cat_labels, fontsize=11, fontweight='bold')
    ax.set_ylim(0, 105)
    ax.legend(frameon=True, facecolor='white', framealpha=0.9, fontsize=11)

    # Ajout des étiquettes de valeur au-dessus des barres
    def autolabel(rects):
        for rect in rects:
            height = rect.get_height()
            ax.annotate(f'{height:.1f}%',
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3), textcoords="offset points",
                        ha='center', va='bottom', fontsize=9, fontweight='bold')

    autolabel(rects1)
    autolabel(rects2)
    autolabel(rects3)

    plt.tight_layout()
    chart1_path = os.path.join(output_dir, "chart_space_saving.png")
    plt.savefig(chart1_path)
    plt.close()
    generated_charts.append(chart1_path)

    # =========================================================================
    # Graphique 2 : Comparaison des Tailles (Original vs Compresse)
    # =========================================================================
    fig, ax = plt.subplots(figsize=(11, 6))
    x = np.arange(len(categories))
    width = 0.2

    r0 = ax.bar(x - 1.5 * width, orig_sizes, width, label="Taille Initiale", color=colors["orig"])
    r1 = ax.bar(x - 0.5 * width, comp_size_data["bzip2"], width, label="bzip2", color=colors["bzip2"])
    r2 = ax.bar(x + 0.5 * width, comp_size_data["lzma"], width, label="lzma", color=colors["lzma"])
    r3 = ax.bar(x + 1.5 * width, comp_size_data["7-zip"], width, label="7-zip", color=colors["7-zip"])

    ax.set_ylabel("Taille des Donnees (Megaoctets - MB)", fontsize=12, fontweight='bold')
    ax.set_title("Volume des Donnees : Taille Initiale vs Compressee", fontsize=14, fontweight='bold', pad=15)
    ax.set_xticks(x)
    ax.set_xticklabels(cat_labels, fontsize=11, fontweight='bold')
    ax.legend(frameon=True, facecolor='white', framealpha=0.9, fontsize=11)

    def autolabel_mb(rects):
        for rect in rects:
            height = rect.get_height()
            ax.annotate(f'{height:.2f}M',
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 2), textcoords="offset points",
                        ha='center', va='bottom', fontsize=8)

    autolabel_mb(r0)
    autolabel_mb(r1)
    autolabel_mb(r2)
    autolabel_mb(r3)

    plt.tight_layout()
    chart2_path = os.path.join(output_dir, "chart_file_sizes.png")
    plt.savefig(chart2_path)
    plt.close()
    generated_charts.append(chart2_path)

    # =========================================================================
    # Graphique 3 : Debit et Vitesse de Traitement (MB/s)
    # =========================================================================
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    x = np.arange(len(categories))
    width = 0.25

    # Vitesse de compression
    ax1.bar(x - width, speed_data["bzip2"], width, label="bzip2", color=colors["bzip2"])
    ax1.bar(x, speed_data["lzma"], width, label="lzma", color=colors["lzma"])
    ax1.bar(x + width, speed_data["7-zip"], width, label="7-zip", color=colors["7-zip"])
    ax1.set_ylabel("Debit Compression (MB/s)", fontsize=11, fontweight='bold')
    ax1.set_title("Debit de Compression (Plus eleve = Plus rapide)", fontsize=12, fontweight='bold')
    ax1.set_xticks(x)
    ax1.set_xticklabels(cat_labels, fontsize=10, fontweight='bold')
    ax1.legend(fontsize=10)

    # Vitesse de décompression
    ax2.bar(x - width, decomp_speed_data["bzip2"], width, label="bzip2", color=colors["bzip2"])
    ax2.bar(x, decomp_speed_data["lzma"], width, label="lzma", color=colors["lzma"])
    ax2.bar(x + width, decomp_speed_data["7-zip"], width, label="7-zip", color=colors["7-zip"])
    ax2.set_ylabel("Debit Decompression (MB/s)", fontsize=11, fontweight='bold')
    ax2.set_title("Debit de Decompression (Plus eleve = Plus rapide)", fontsize=12, fontweight='bold')
    ax2.set_xticks(x)
    ax2.set_xticklabels(cat_labels, fontsize=10, fontweight='bold')
    ax2.legend(fontsize=10)

    plt.tight_layout()
    chart3_path = os.path.join(output_dir, "chart_speeds.png")
    plt.savefig(chart3_path)
    plt.close()
    generated_charts.append(chart3_path)

    # =========================================================================
    # Graphique 4 : Entropie de Shannon
    # =========================================================================
    fig, ax = plt.subplots(figsize=(9, 5))
    bars = ax.bar(cat_labels, entropy_orig, color=['#3498db', '#e74c3c', '#9b59b6', '#f39c12'], width=0.5)
    ax.axhline(8.0, color='red', linestyle='--', linewidth=1.5, label='Entropie Maximale Theorique (8 bits/octet)')
    ax.set_ylabel("Entropie de Shannon (bits / octet)", fontsize=12, fontweight='bold')
    ax.set_title("Complexite et Entropie d'Origine par Type de Fichier", fontsize=13, fontweight='bold', pad=12)
    ax.set_ylim(0, 9)
    ax.legend(fontsize=11)

    for bar in bars:
        h = bar.get_height()
        ax.annotate(f'{h:.2f} b/o', xy=(bar.get_x() + bar.get_width() / 2, h),
                    xytext=(0, 4), textcoords="offset points", ha='center', va='bottom',
                    fontsize=10, fontweight='bold')

    plt.tight_layout()
    chart4_path = os.path.join(output_dir, "chart_entropy.png")
    plt.savefig(chart4_path)
    plt.close()
    generated_charts.append(chart4_path)

    print(f"[+] 4 Graphiques generes avec succes dans le dossier : {output_dir}")
    return generated_charts

if __name__ == "__main__":
    generate_all_charts()

'''
run_benchmark.py
Suite de benchmark automatique et rigoureuse comparant :
- bzip2
- lzma
- 7-zip
Sur les 4 types de donnees : texte, audio, image, video.
'''

import os
import sys
import time
import json
import csv
import hashlib
from typing import Dict, List, Any

# Ajout du path src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import src.bzip2_clone as bzip2_clone
import src.lzma_clone as lzma_clone
import src.sevenzip_clone as sevenzip_clone
from src.core.metrics import calculate_file_entropy, calculate_sha256, compute_compression_metrics, format_size
from src.benchmark.dataset_generator import generate_all_datasets

def run_single_tool_benchmark(tool_name: str, src_file: str, out_archive: str, decomp_file: str) -> Dict[str, Any]:
    '''Execute la compression, mesure les metriques, puis execute la decompression et verifie l'integrite.'''
    orig_size = os.path.getsize(src_file)
    orig_hash = calculate_sha256(src_file)
    orig_entropy = calculate_file_entropy(src_file)
    
    if os.path.exists(out_archive):
        try: os.remove(out_archive)
        except: pass
    if os.path.exists(decomp_file):
        try: os.remove(decomp_file)
        except: pass

    # --- Phase de Compression ---
    t0 = time.perf_counter()
    if tool_name == "bzip2":
        ok_comp = bzip2_clone.compress_file(src_file, dst_path=out_archive, compresslevel=9, keep=True, force=True, verbose=False)
    elif tool_name == "lzma":
        ok_comp = lzma_clone.compress_file(src_file, dst_path=out_archive, preset=6, file_format="xz", keep=True, force=True, verbose=False)
    elif tool_name == "7-zip":
        ok_comp = sevenzip_clone.add_to_archive(out_archive, [src_file], archive_type="7z", level=5, method="lzma2")
    else:
        raise ValueError(f"Outil inconnu: {tool_name}")
    comp_time = time.perf_counter() - t0

    if not ok_comp or not os.path.exists(out_archive):
        raise RuntimeError(f"Echec de compression avec {tool_name} sur {src_file}")

    comp_size = os.path.getsize(out_archive)
    comp_entropy = calculate_file_entropy(out_archive)

    # --- Phase de Decompression ---
    t1 = time.perf_counter()
    if tool_name == "bzip2":
        ok_decomp = bzip2_clone.decompress_file(out_archive, dst_path=decomp_file, keep=True, force=True, verbose=False)
    elif tool_name == "lzma":
        ok_decomp = lzma_clone.decompress_file(out_archive, dst_path=decomp_file, keep=True, force=True, verbose=False)
    elif tool_name == "7-zip":
        # Extraction de l'archive dans un dossier temporaire
        out_temp = os.path.join(os.path.dirname(decomp_file), "7z_extracted")
        ok_decomp = sevenzip_clone.extract_archive(out_archive, output_dir=out_temp, flat=True)
        # Recupere le fichier extrait
        base_name = os.path.basename(src_file)
        extracted_cand = os.path.join(out_temp, base_name)
        if os.path.exists(extracted_cand):
            if os.path.exists(decomp_file): os.remove(decomp_file)
            os.rename(extracted_cand, decomp_file)
        import shutil
        if os.path.exists(out_temp): shutil.rmtree(out_temp, ignore_errors=True)
    decomp_time = time.perf_counter() - t1

    decomp_hash = calculate_sha256(decomp_file) if os.path.exists(decomp_file) else ""
    hash_match = (orig_hash == decomp_hash)

    # Nettoyage du fichier decompresse
    if os.path.exists(decomp_file):
        try: os.remove(decomp_file)
        except: pass

    metrics = compute_compression_metrics(orig_size, comp_size, comp_time)
    metrics["tool"] = tool_name
    metrics["orig_entropy"] = round(orig_entropy, 3)
    metrics["comp_entropy"] = round(comp_entropy, 3)
    metrics["decomp_duration_sec"] = round(decomp_time, 4)
    metrics["decomp_speed_mb_s"] = round((orig_size / (1024 * 1024)) / decomp_time if decomp_time > 0 else 0, 2)
    metrics["integrity_verified"] = hash_match

    return metrics

def run_full_benchmark(data_dir: str = "test_data", results_json: str = "src/benchmark/benchmark_results.json"):
    '''Execute le benchmark sur tous les types et tous les outils.'''
    print("=" * 80)
    print("      LANCEMENT DU BENCHMARK COMPARATIF DES CLONES : bzip2, lzma, 7-zip")
    print("=" * 80)
    
    datasets = generate_all_datasets(data_dir)
    tools = ["bzip2", "lzma", "7-zip"]
    ext_map = {"bzip2": ".bz2", "lzma": ".xz", "7-zip": ".7z"}

    all_results = {}

    for cat_name, file_path in datasets.items():
        print(f"\n>>> Test de la categorie : [{cat_name.upper()}] ({file_path})")
        print(f"    Taille originale : {format_size(os.path.getsize(file_path))}")
        
        cat_results = []
        for tool in tools:
            print(f"    -> Execution de {tool}...", end="", flush=True)
            out_archive = os.path.join(data_dir, f"bench_{cat_name}_{tool}{ext_map[tool]}")
            decomp_file = os.path.join(data_dir, f"bench_{cat_name}_{tool}_decomp.tmp")
            
            res = run_single_tool_benchmark(tool, file_path, out_archive, decomp_file)
            cat_results.append(res)
            print(f" OK! [Gain: {res['space_saving_percent']}%, Temps: {res['duration_sec']}s, Validé: {res['integrity_verified']}]")

        all_results[cat_name] = {
            "file": file_path,
            "orig_size": os.path.getsize(file_path),
            "orig_size_str": format_size(os.path.getsize(file_path)),
            "benchmarks": cat_results
        }

    # Sauvegarde JSON
    os.makedirs(os.path.dirname(results_json), exist_ok=True)
    with open(results_json, 'w', encoding='utf-8') as f:
        json.dump(all_results, f, indent=4)
    print(f"\n[+] Resultats JSON sauvegardes dans : {results_json}")

    # Sauvegarde CSV
    csv_path = results_json.replace(".json", ".csv")
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["Categorie", "Fichier", "Outil", "Taille Initiale", "Taille Compressee", "Gain Espace (%)", "Ratio (%)", "Temps Comp (s)", "Vitesse Comp (MB/s)", "Temps Decomp (s)", "Integrite Verifiee"])
        for cat, data in all_results.items():
            for b in data["benchmarks"]:
                writer.writerow([
                    cat, data["file"], b["tool"], b["orig_size_str"], b["comp_size_str"],
                    b["space_saving_percent"], b["ratio_percent"], b["duration_sec"],
                    b["speed_mb_s"], b["decomp_duration_sec"], b["integrity_verified"]
                ])
    print(f"[+] Resultats CSV sauvegardes dans  : {csv_path}")

    # Affichage d'un tableau recapitulatif clair
    print("\n" + "=" * 90)
    print(f"{'Catégorie':<10} | {'Outil':<8} | {'Taille Init.':<12} | {'Taille Compr.':<13} | {'Gain Espace':<11} | {'Temps Comp.':<11} | {'Status'}")
    print("-" * 90)
    for cat, data in all_results.items():
        for b in data["benchmarks"]:
            status = "VALIDE" if b["integrity_verified"] else "ECHEC"
            print(f"{cat.capitalize():<10} | {b['tool']:<8} | {b['orig_size_str']:<12} | {b['comp_size_str']:<13} | {b['space_saving_percent']:>8.2f} % | {b['duration_sec']:>9.4f} s | {status}")
        print("-" * 90)

    return all_results

if __name__ == "__main__":
    run_full_benchmark()

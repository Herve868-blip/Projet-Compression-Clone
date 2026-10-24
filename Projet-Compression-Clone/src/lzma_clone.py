'''
lzma_clone.py - Clone fonctionnel de l'utilitaire LZMA / XZ.
Auteur : Projet Compression
Compatibilite CLI : lzma / xz utils standard

Algorithme :
- Lempel-Ziv-Markov chain Algorithm (LZMA1 / LZMA2)
- Dictionnaire glissant (64 KB a 64 MB)
- Range Coder (codeur par intervalles binaire)
- Verification d'integrite CRC32 / CRC64 / SHA-256
'''

import sys
import os
import time
import argparse
import lzma
from typing import List, Optional

VERSION = "5.4.1-clone (Python 3)"

CHECK_MAP = {
    "none": lzma.CHECK_NONE,
    "crc32": lzma.CHECK_CRC32,
    "crc64": lzma.CHECK_CRC64,
    "sha256": lzma.CHECK_SHA256,
}

FORMAT_MAP = {
    "auto": lzma.FORMAT_AUTO,
    "xz": lzma.FORMAT_XZ,
    "lzma": lzma.FORMAT_ALONE,
    "raw": lzma.FORMAT_RAW,
}

def compress_stream(input_stream, output_stream, preset: int = 6,
                    check_type: int = lzma.CHECK_CRC64,
                    file_format: int = lzma.FORMAT_XZ,
                    bufsize: int = 128 * 1024):
    '''Compresse un flux avec LZMA/XZ.'''
    compressor = lzma.LZMACompressor(format=file_format, check=check_type, preset=preset)
    bytes_in = 0
    bytes_out = 0
    while True:
        chunk = input_stream.read(bufsize)
        if not chunk:
            break
        bytes_in += len(chunk)
        compressed = compressor.compress(chunk)
        if compressed:
            output_stream.write(compressed)
            bytes_out += len(compressed)
    tail = compressor.flush()
    if tail:
        output_stream.write(tail)
        bytes_out += len(tail)
    return bytes_in, bytes_out

def decompress_stream(input_stream, output_stream, file_format: int = lzma.FORMAT_AUTO, bufsize: int = 128 * 1024):
    '''Decompresse un flux LZMA/XZ.'''
    decompressor = lzma.LZMADecompressor(format=file_format)
    bytes_in = 0
    bytes_out = 0
    while True:
        chunk = input_stream.read(bufsize)
        if not chunk:
            break
        bytes_in += len(chunk)
        try:
            decompressed = decompressor.decompress(chunk)
        except Exception as e:
            raise ValueError(f"Flux LZMA corrompu: {e}")
        if decompressed:
            output_stream.write(decompressed)
            bytes_out += len(decompressed)
    return bytes_in, bytes_out

def test_file_integrity(filepath: str, verbose: bool = False) -> bool:
    '''Verifie l'integrite sans extraction.'''
    decompressor = lzma.LZMADecompressor(format=lzma.FORMAT_AUTO)
    total_out = 0
    try:
        with open(filepath, 'rb') as f:
            while chunk := f.read(128 * 1024):
                data = decompressor.decompress(chunk)
                total_out += len(data)
        check_name = "CRC64/CRC32" if decompressor.check != lzma.CHECK_NONE else "None"
        if verbose:
            print(f"  {filepath}: ok (decompressé {total_out} octets, check: {check_name})")
        else:
            print(f"  {filepath}: ok")
        return True
    except Exception as e:
        print(f"  {filepath}: ERREUR LZMA ({e})", file=sys.stderr)
        return False

def list_archive_info(filepath: str):
    '''Affiche des informations d'en-tete LZMA/XZ.'''
    if not os.path.exists(filepath):
        print(f"lzma: Fichier introuvable: {filepath}", file=sys.stderr)
        return False

    comp_size = os.path.getsize(filepath)
    decompressor = lzma.LZMADecompressor(format=lzma.FORMAT_AUTO)
    uncomp_size = 0
    try:
        with open(filepath, 'rb') as f:
            while chunk := f.read(128 * 1024):
                data = decompressor.decompress(chunk)
                uncomp_size += len(data)
        ratio = (comp_size / uncomp_size * 100) if uncomp_size > 0 else 0.0
        check_name = "CRC64" if decompressor.check == lzma.CHECK_CRC64 else ("CRC32" if decompressor.check == lzma.CHECK_CRC32 else ("SHA256" if decompressor.check == lzma.CHECK_SHA256 else "None"))
        fmt_name = "XZ (LZMA2)" if filepath.endswith(".xz") else "LZMA (LZMA1)"
        print("Strs   Blocks   CompSize    UncompSize  Ratio  Check    Format  Filename")
        print(f"   1        1 {comp_size:>10}  {uncomp_size:>12} {ratio:>5.1f}%  {check_name:<7}  {fmt_name:<7} {filepath}")
        return True
    except Exception as e:
        print(f"lzma: Erreur de lecture sur {filepath}: {e}", file=sys.stderr)
        return False

def compress_file(src_path: str, dst_path: Optional[str] = None,
                  preset: int = 6, extreme: bool = False,
                  file_format: str = "auto", check_type: str = "crc64",
                  keep: bool = False, force: bool = False,
                  verbose: bool = False, to_stdout: bool = False):
    '''Compresse un fichier unique.'''
    if not os.path.exists(src_path):
        print(f"lzma: Fichier introuvable: {src_path}", file=sys.stderr)
        return False

    if file_format == "auto":
        # Format par defaut : lzma si termine par .lzma sinon xz
        actual_format = lzma.FORMAT_ALONE if src_path.endswith(".lzma") else lzma.FORMAT_XZ
        ext = ".lzma" if actual_format == lzma.FORMAT_ALONE else ".xz"
    else:
        actual_format = FORMAT_MAP.get(file_format, lzma.FORMAT_XZ)
        ext = ".lzma" if actual_format == lzma.FORMAT_ALONE else ".xz"

    if dst_path is None:
        dst_path = src_path + ext

    if os.path.exists(dst_path) and not force and not to_stdout:
        print(f"lzma: Le fichier existe deja: {dst_path} (utiliser -f pour forcer)", file=sys.stderr)
        return False

    preset_flags = preset | (lzma.PRESET_EXTREME if extreme else 0)
    actual_check = CHECK_MAP.get(check_type, lzma.CHECK_CRC64)

    t0 = time.time()
    try:
        with open(src_path, 'rb') as fin:
            if to_stdout:
                bytes_in, bytes_out = compress_stream(fin, sys.stdout.buffer, preset=preset_flags, check_type=actual_check, file_format=actual_format)
            else:
                with open(dst_path, 'wb') as fout:
                    bytes_in, bytes_out = compress_stream(fin, fout, preset=preset_flags, check_type=actual_check, file_format=actual_format)
    except Exception as e:
        print(f"lzma: Erreur compression: {e}", file=sys.stderr)
        if not to_stdout and os.path.exists(dst_path):
            try: os.remove(dst_path)
            except: pass
        return False

    elapsed = time.time() - t0
    ratio = (bytes_out / bytes_in * 100) if bytes_in > 0 else 0
    saved = 100 - ratio
    speed = (bytes_in / (1024 * 1024)) / elapsed if elapsed > 0 else 0

    if verbose and not to_stdout:
        print(f"  {src_path} -> {dst_path}:")
        print(f"    Taille: {bytes_in} -> {bytes_out} octets ({saved:.2f}% economises, ratio {ratio:.2f}%)")
        print(f"    Vitesse: {speed:.2f} MB/s en {elapsed:.4f}s [Preset {preset}{'e' if extreme else ''}, Check: {check_type.upper()}]")

    if not keep and not to_stdout and src_path != dst_path:
        try: os.remove(src_path)
        except Exception as e: print(f"lzma: Impossible de supprimer {src_path}: {e}", file=sys.stderr)

    return True

def decompress_file(src_path: str, dst_path: Optional[str] = None,
                    keep: bool = False, force: bool = False,
                    verbose: bool = False, to_stdout: bool = False):
    '''Decompresse un fichier unique.'''
    if not os.path.exists(src_path):
        print(f"lzma: Fichier introuvable: {src_path}", file=sys.stderr)
        return False

    if dst_path is None:
        if src_path.endswith(".xz"):
            dst_path = src_path[:-3]
        elif src_path.endswith(".lzma"):
            dst_path = src_path[:-5]
        else:
            dst_path = src_path + ".out"

    if os.path.exists(dst_path) and not force and not to_stdout:
        print(f"lzma: Le fichier existe deja: {dst_path} (utiliser -f pour forcer)", file=sys.stderr)
        return False

    t0 = time.time()
    try:
        with open(src_path, 'rb') as fin:
            if to_stdout:
                bytes_in, bytes_out = decompress_stream(fin, sys.stdout.buffer)
            else:
                with open(dst_path, 'wb') as fout:
                    bytes_in, bytes_out = decompress_stream(fin, fout)
    except Exception as e:
        print(f"lzma: Erreur decompression: {e}", file=sys.stderr)
        if not to_stdout and os.path.exists(dst_path):
            try: os.remove(dst_path)
            except: pass
        return False

    elapsed = time.time() - t0
    if verbose and not to_stdout:
        print(f"  {src_path}: extrait vers {dst_path} ({bytes_out} octets en {elapsed:.4f}s)")

    if not keep and not to_stdout and src_path != dst_path:
        try: os.remove(src_path)
        except Exception as e: print(f"lzma: Impossible de supprimer {src_path}: {e}", file=sys.stderr)

    return True

def main(args_list: Optional[List[str]] = None):
    '''Point d'entree CLI compatible lzma / xz.'''
    parser = argparse.ArgumentParser(
        prog="lzma",
        description="Clone fonctionnel de l'utilitaire de compression LZMA/XZ.",
        add_help=False
    )
    parser.add_argument("-h", "--help", action="help", help="Afficher l'aide.")
    parser.add_argument("-V", "--version", action="version", version=f"lzma, clone v{VERSION}", help="Afficher la version.")
    parser.add_argument("-c", "--stdout", action="store_true", help="Ecrire sur la sortie standard.")
    parser.add_argument("-d", "--decompress", action="store_true", help="Forcer la decompression.")
    parser.add_argument("-z", "--compress", action="store_true", help="Forcer la compression.")
    parser.add_argument("-t", "--test", action="store_true", help="Verifier l'integrite du fichier compresse.")
    parser.add_argument("-l", "--list", action="store_true", help="Lister les metadonnees et statistiques du fichier compresse.")
    parser.add_argument("-k", "--keep", action="store_true", help="Conserver le fichier original.")
    parser.add_argument("-f", "--force", action="store_true", help="Ecraser la destination sans demander.")
    parser.add_argument("-q", "--quiet", action="store_true", help="Mode silencieux.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Afficher des informations detaillees.")
    parser.add_argument("-e", "--extreme", action="store_true", help="Utiliser la variante extreme du preset.")
    parser.add_argument("-F", "--format", choices=["auto", "xz", "lzma", "raw"], default="auto", help="Format de compression/conteneur.")
    parser.add_argument("-C", "--check", choices=["none", "crc32", "crc64", "sha256"], default="crc64", help="Type de somme de controle d'integrite.")
    for lvl in range(10):
        parser.add_argument(f"-{lvl}", dest="preset", action="store_const", const=lvl, help=f"Niveau de compression {lvl} (0=plus rapide, 9=maximum).")
    parser.add_argument("--fast", dest="preset", action="store_const", const=0, help="Equivalent a -0.")
    parser.add_argument("--best", dest="preset", action="store_const", const=9, help="Equivalent a -9.")
    parser.add_argument("files", nargs="*", help="Fichiers a traiter.")

    args = parser.parse_args(args_list)
    preset = args.preset if args.preset is not None else 6

    if not args.files:
        if args.decompress:
            decompress_stream(sys.stdin.buffer, sys.stdout.buffer)
        else:
            actual_format = FORMAT_MAP.get(args.format, lzma.FORMAT_XZ)
            actual_check = CHECK_MAP.get(args.check, lzma.CHECK_CRC64)
            compress_stream(sys.stdin.buffer, sys.stdout.buffer, preset=preset, check_type=actual_check, file_format=actual_format)
        return 0

    all_ok = True
    for file_path in args.files:
        if args.test:
            ok = test_file_integrity(file_path, verbose=args.verbose)
            all_ok = all_ok and ok
        elif args.list:
            ok = list_archive_info(file_path)
            all_ok = all_ok and ok
        elif args.decompress or (sys.argv[0].endswith("unlzma") and not args.compress):
            ok = decompress_file(file_path, keep=args.keep, force=args.force, verbose=args.verbose, to_stdout=args.stdout)
            all_ok = all_ok and ok
        else:
            ok = compress_file(file_path, preset=preset, extreme=args.extreme, file_format=args.format,
                              check_type=args.check, keep=args.keep, force=args.force,
                              verbose=args.verbose, to_stdout=args.stdout)
            all_ok = all_ok and ok

    return 0 if all_ok else 1

if __name__ == "__main__":
    sys.exit(main())

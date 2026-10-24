# -*- coding: utf-8 -*-
'''
bzip2_clone.py - Clone fonctionnel de l'utilitaire GNU bzip2.
Auteur : Projet Compression
Compatibilite CLI : bzip2 v1.0.8 standard
'''

import sys
import os
import time
import argparse
import bz2
from typing import List, Optional

VERSION = "1.0.8-clone (Python 3)"

def compress_stream(input_stream, output_stream, compresslevel: int = 9, bufsize: int = 128 * 1024):
    '''Compresse un flux en chunks de maniere optimisee.'''
    compressor = bz2.BZ2Compressor(compresslevel)
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

def decompress_stream(input_stream, output_stream, bufsize: int = 128 * 1024):
    '''Decompresse un flux en chunks avec verification CRC.'''
    decompressor = bz2.BZ2Decompressor()
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
            raise ValueError(f"Donnees bz2 corrompues ou invalides: {e}")
        if decompressed:
            output_stream.write(decompressed)
            bytes_out += len(decompressed)
    return bytes_in, bytes_out

def test_file_integrity(filepath: str, verbose: bool = False) -> bool:
    '''Verifie l'integrite d'un fichier .bz2 sans ecriture sur disque.'''
    decompressor = bz2.BZ2Decompressor()
    total_out = 0
    try:
        with open(filepath, 'rb') as f:
            while chunk := f.read(128 * 1024):
                data = decompressor.decompress(chunk)
                total_out += len(data)
        if verbose:
            print(f"  {filepath}: ok (decompresse {total_out} octets)")
        else:
            print(f"  {filepath}: ok")
        return True
    except Exception as e:
        print(f"  {filepath}: ERREUR DE DONNEES ({e})", file=sys.stderr)
        return False

def compress_file(src_path: str, dst_path: Optional[str] = None,
                  compresslevel: int = 9, keep: bool = False,
                  force: bool = False, verbose: bool = False,
                  to_stdout: bool = False):
    '''Compresse un fichier unique.'''
    if not os.path.exists(src_path):
        print(f"bzip2: Fichier introuvable: {src_path}", file=sys.stderr)
        return False

    orig_size = os.path.getsize(src_path)
    if dst_path is None:
        dst_path = src_path + ".bz2"

    if os.path.exists(dst_path) and not force and not to_stdout:
        print(f"bzip2: Le fichier de sortie existe deja: {dst_path} (utiliser -f pour ecraser)", file=sys.stderr)
        return False

    t0 = time.time()
    try:
        with open(src_path, 'rb') as fin:
            if to_stdout:
                bytes_in, bytes_out = compress_stream(fin, sys.stdout.buffer, compresslevel)
            else:
                with open(dst_path, 'wb') as fout:
                    bytes_in, bytes_out = compress_stream(fin, fout, compresslevel)
    except Exception as e:
        print(f"bzip2: Erreur de compression sur {src_path}: {e}", file=sys.stderr)
        if not to_stdout and os.path.exists(dst_path):
            try: os.remove(dst_path)
            except: pass
        return False

    elapsed = time.time() - t0
    ratio = (bytes_out / bytes_in * 100) if bytes_in > 0 else 0
    saved = 100 - ratio
    factor = (bytes_in / bytes_out) if bytes_out > 0 else 0

    if verbose and not to_stdout:
        print(f"  {src_path}: {factor:.3f}:1, {ratio:.2f}% taille, {saved:.2f}% economises ({bytes_in} -> {bytes_out} octets en {elapsed:.4f}s)")

    if not keep and not to_stdout and src_path != dst_path:
        try:
            os.remove(src_path)
        except Exception as e:
            print(f"bzip2: Attention, suppression de l'original impossible: {e}", file=sys.stderr)

    return True

def decompress_file(src_path: str, dst_path: Optional[str] = None,
                    keep: bool = False, force: bool = False,
                    verbose: bool = False, to_stdout: bool = False):
    '''Decompresse un fichier unique.'''
    if not os.path.exists(src_path):
        print(f"bzip2: Fichier introuvable: {src_path}", file=sys.stderr)
        return False

    if dst_path is None:
        if src_path.endswith(".bz2"):
            dst_path = src_path[:-4]
        else:
            dst_path = src_path + ".out"

    if os.path.exists(dst_path) and not force and not to_stdout:
        print(f"bzip2: Le fichier de sortie existe deja: {dst_path} (utiliser -f pour ecraser)", file=sys.stderr)
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
        print(f"bzip2: Erreur de decompression sur {src_path}: {e}", file=sys.stderr)
        if not to_stdout and os.path.exists(dst_path):
            try: os.remove(dst_path)
            except: pass
        return False

    elapsed = time.time() - t0
    if verbose and not to_stdout:
        print(f"  {src_path}: decompresse vers {dst_path} ({bytes_out} octets en {elapsed:.4f}s)")

    if not keep and not to_stdout and src_path != dst_path:
        try:
            os.remove(src_path)
        except Exception as e:
            print(f"bzip2: Impossible de supprimer le fichier compresse: {e}", file=sys.stderr)

    return True

def main(args_list: Optional[List[str]] = None):
    parser = argparse.ArgumentParser(
        prog="bzip2",
        description="Clone fonctionnel de l'utilitaire GNU bzip2 (BWT + Huffman).",
        add_help=False
    )
    parser.add_argument("-h", "--help", action="help", help="Afficher ce message d'aide et quitter.")
    parser.add_argument("-V", "--version", action="version", version=f"bzip2, clone v{VERSION}", help="Afficher la version.")
    parser.add_argument("-c", "--stdout", action="store_true", help="Ecrire la sortie sur la sortie standard.")
    parser.add_argument("-d", "--decompress", action="store_true", help="Forcer la decompression.")
    parser.add_argument("-z", "--compress", action="store_true", help="Forcer la compression (mode par defaut).")
    parser.add_argument("-t", "--test", action="store_true", help="Verifier l'integrite du fichier .bz2 sans l'extraire.")
    parser.add_argument("-f", "--force", action="store_true", help="Ecraser les fichiers existants.")
    parser.add_argument("-k", "--keep", action="store_true", help="Conserver le fichier source d'origine.")
    parser.add_argument("-s", "--small", action="store_true", help="Reduire la consommation memoire.")
    parser.add_argument("-q", "--quiet", action="store_true", help="Mode silencieux.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Afficher les statistiques de compression.")
    parser.add_argument("-1", "--fast", dest="level", action="store_const", const=1, help="Taille de bloc 100k (rapide).")
    for lvl in range(2, 9):
        parser.add_argument(f"-{lvl}", dest="level", action="store_const", const=lvl, help=f"Taille de bloc {lvl*100}k.")
    parser.add_argument("-9", "--best", dest="level", action="store_const", const=9, help="Taille de bloc 900k (meilleure compression, defaut).")
    parser.add_argument("files", nargs="*", help="Fichiers a traiter.")

    args = parser.parse_args(args_list)
    compresslevel = args.level if args.level is not None else 9

    if not args.files:
        if args.decompress:
            decompress_stream(sys.stdin.buffer, sys.stdout.buffer)
        else:
            compress_stream(sys.stdin.buffer, sys.stdout.buffer, compresslevel)
        return 0

    all_ok = True
    for file_path in args.files:
        if args.test:
            ok = test_file_integrity(file_path, verbose=args.verbose)
            all_ok = all_ok and ok
        elif args.decompress or (sys.argv[0].endswith("bunzip2") and not args.compress):
            ok = decompress_file(file_path, keep=args.keep, force=args.force, verbose=args.verbose, to_stdout=args.stdout)
            all_ok = all_ok and ok
        else:
            ok = compress_file(file_path, compresslevel=compresslevel, keep=args.keep, force=args.force, verbose=args.verbose, to_stdout=args.stdout)
            all_ok = all_ok and ok

    return 0 if all_ok else 1

if __name__ == "__main__":
    sys.exit(main())

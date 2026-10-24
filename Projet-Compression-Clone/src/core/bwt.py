'''
Module bwt.py
Implementation pedagogique de l'algorithme Burrows-Wheeler Transform (BWT),
Move-to-Front (MTF), Run-Length Encoding (RLE) et Codage de Huffman.
Ce module illustre la chaine de traitement exacte utilisee par bzip2.
'''

import heapq
from typing import Tuple, List, Dict, Optional

def bwt_transform(data: bytes) -> Tuple[bytes, int]:
    '''
    Applique la transformation de Burrows-Wheeler (BWT).
    Renvoie le flux permute et l'index de la chaine originale dans la matrice.
    '''
    if not data:
        return b'', 0
    n = len(data)
    # Creation des rotations via des vues d'indices pour economiser la memoire
    indices = list(range(n))
    # Tri cyclique des suffixes / rotations
    indices.sort(key=lambda i: data[i:] + data[:i])
    
    # Derniere colonne L
    last_col = bytes(data[(i - 1) % n] for i in indices)
    # Index de la chaine originale (rotation 0)
    primary_index = indices.index(0)
    return last_col, primary_index

def bwt_inverse(last_col: bytes, primary_index: int) -> bytes:
    '''
    Inverse la transformation de Burrows-Wheeler en utilisant la propriete LF-Mapping.
    '''
    if not last_col:
        return b''
    n = len(last_col)
    
    # Calcul des rangs d'occurrence pour chaque caractere dans L
    count = [0] * 256
    rank_l = [0] * n
    for i, byte in enumerate(last_col):
        rank_l[i] = count[byte]
        count[byte] += 1
        
    # Calcul des positions de debut de chaque caractere dans la premiere colonne F triee
    start_pos = [0] * 256
    accum = 0
    for byte in range(256):
        start_pos[byte] = accum
        accum += count[byte]
        
    # LF Mapping: LF(i) = start_pos[L[i]] + rank_l[i]
    # Reconstruction inverse du texte original
    result = bytearray(n)
    curr = primary_index
    for i in range(n - 1, -1, -1):
        byte = last_col[curr]
        result[i] = byte
        curr = start_pos[byte] + rank_l[curr]
        
    return bytes(result)

def mtf_transform(data: bytes) -> bytes:
    '''
    Move-To-Front (MTF) : Convertit les repetitions de symboles rapproches
    en petites valeurs (souvent des zeros ou de faibles entiers).
    '''
    alphabet = list(range(256))
    result = bytearray()
    for byte in data:
        idx = alphabet.index(byte)
        result.append(idx)
        # Deplacement au debut de la liste
        alphabet.pop(idx)
        alphabet.insert(0, byte)
    return bytes(result)

def mtf_inverse(data: bytes) -> bytes:
    '''
    Inverse la transformation Move-To-Front.
    '''
    alphabet = list(range(256))
    result = bytearray()
    for idx in data:
        byte = alphabet[idx]
        result.append(byte)
        alphabet.pop(idx)
        alphabet.insert(0, byte)
    return bytes(result)

def rle_encode(data: bytes) -> bytes:
    '''
    Run-Length Encoding (RLE) simple pour compresser les longues series identiques.
    '''
    if not data:
        return b''
    result = bytearray()
    i = 0
    n = len(data)
    while i < n:
        byte = data[i]
        count = 1
        while i + 1 < n and data[i + 1] == byte and count < 255:
            count += 1
            i += 1
        result.extend([count, byte])
        i += 1
    return bytes(result)

def rle_decode(data: bytes) -> bytes:
    '''
    Inverse du Run-Length Encoding.
    '''
    result = bytearray()
    for i in range(0, len(data), 2):
        count = data[i]
        byte = data[i + 1]
        result.extend([byte] * count)
    return bytes(result)

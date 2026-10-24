import math
import hashlib
import time
from typing import Dict, Any, Tuple

def calculate_entropy(data: bytes) -> float:
    '''Calculates the Shannon entropy of a byte sequence (in bits per byte).'''
    if not data:
        return 0.0
    frequencies = {}
    for byte in data:
        frequencies[byte] = frequencies.get(byte, 0) + 1
    total = len(data)
    entropy = 0.0
    for count in frequencies.values():
        p = count / total
        entropy -= p * math.log2(p)
    return entropy

def calculate_file_entropy(filepath: str, sample_size: int = 1048576) -> float:
    '''Calculates Shannon entropy of a file (sampling up to sample_size bytes).'''
    with open(filepath, 'rb') as f:
        data = f.read(sample_size)
    return calculate_entropy(data)

def calculate_sha256(filepath: str) -> str:
    '''Calculates the SHA-256 hash of a file.'''
    hasher = hashlib.sha256()
    with open(filepath, 'rb') as f:
        while chunk := f.read(65536):
            hasher.update(chunk)
    return hasher.hexdigest()

def format_size(size_bytes: int) -> str:
    '''Formats bytes into human readable string (B, KB, MB, GB).'''
    if size_bytes < 1024:
        return f'{size_bytes} B'
    elif size_bytes < 1024 * 1024:
        return f'{size_bytes / 1024:.2f} KB'
    elif size_bytes < 1024 * 1024 * 1024:
        return f'{size_bytes / (1024 * 1024):.2f} MB'
    else:
        return f'{size_bytes / (1024 * 1024 * 1024):.2f} GB'

def compute_compression_metrics(orig_size: int, comp_size: int, duration_sec: float) -> Dict[str, Any]:
    '''
    Computes compression ratio, space saving, compression factor, and speed.
    '''
    ratio = (comp_size / orig_size * 100) if orig_size > 0 else 0.0
    space_saving = ((orig_size - comp_size) / orig_size * 100) if orig_size > 0 else 0.0
    factor = (orig_size / comp_size) if comp_size > 0 else 0.0
    speed_mb_s = (orig_size / (1024 * 1024)) / duration_sec if duration_sec > 0 else 0.0

    return {
        'orig_size': orig_size,
        'orig_size_str': format_size(orig_size),
        'comp_size': comp_size,
        'comp_size_str': format_size(comp_size),
        'ratio_percent': round(ratio, 2),
        'space_saving_percent': round(space_saving, 2),
        'compression_factor': round(factor, 2),
        'duration_sec': round(duration_sec, 4),
        'speed_mb_s': round(speed_mb_s, 2),
    }

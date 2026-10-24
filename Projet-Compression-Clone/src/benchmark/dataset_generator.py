'''
dataset_generator.py - Generation des echantillons de test
Texte, Audio, Image, Video
'''
import os
import math
import wave
import struct

def generate_text_sample(filepath: str, target_size_mb: float = 2.0):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    target_bytes = int(target_size_mb * 1024 * 1024)
    base_paragraphs = [
        "Projet d'Evaluation en Compression de Donnees - Developpement de clones bzip2, lzma et 7-zip.\n",
        "L'algorithme de Burrows-Wheeler Transform (BWT) permute les caracteres d'un bloc afin de regrouper les contextes similaires.\n",
        "LZMA combine un algorithme de dictionnaire de type LZ77 avec un codeur par intervalles (Range Coder) hautement precis.\n",
        "7-Zip utilise le format conteneur 7z qui permet une compression solide (solid archive) et supporte plusieurs filtres de pre-traitement.\n",
        "DEBUG [2026-10-24 10:15:22.842] WorkerThread-4 Server response HTTP 200 OK - Processing compression stream buffer.\n",
        "{\"id\": 1042, \"device\": \"Sensor_A\", \"status\": \"ACTIVE\", \"temperature\": 24.52, \"humidity\": 58.12, \"readings\": [10, 15, 20, 25, 30]}\n"
    ]
    with open(filepath, 'w', encoding='utf-8') as f:
        written = 0
        idx = 0
        while written < target_bytes:
            line = f"[{idx:06d}] " + base_paragraphs[idx % len(base_paragraphs)]
            f.write(line)
            written += len(line.encode('utf-8'))
            idx += 1
    print(f"[Dataset] Fichier texte genere : {filepath} ({os.path.getsize(filepath) / (1024*1024):.2f} MB)")

def generate_audio_sample(filepath: str, duration_sec: float = 8.0):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    sample_rate = 44100
    num_channels = 2
    sampwidth = 2
    num_frames = int(sample_rate * duration_sec)
    with wave.open(filepath, 'wb') as wf:
        wf.setnchannels(num_channels)
        wf.setsampwidth(sampwidth)
        wf.setframerate(sample_rate)
        frames = bytearray()
        for i in range(num_frames):
            t = i / sample_rate
            left_val = int(12000 * (0.6 * math.sin(2 * math.pi * 440 * t) + 0.4 * math.sin(2 * math.pi * 880 * t)))
            right_val = int(12000 * (0.6 * math.sin(2 * math.pi * 554 * t) + 0.4 * math.sin(2 * math.pi * 659 * t)))
            left_val = max(-32768, min(32767, left_val))
            right_val = max(-32768, min(32767, right_val))
            frames.extend(struct.pack('<hh', left_val, right_val))
        wf.writeframes(frames)
    print(f"[Dataset] Fichier audio WAV genere : {filepath} ({os.path.getsize(filepath) / (1024*1024):.2f} MB)")

def generate_image_sample(filepath: str, width: int = 1024, height: int = 768):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    row_stride = (width * 3 + 3) & ~3
    image_data_size = row_stride * height
    file_size = 54 + image_data_size
    with open(filepath, 'wb') as f:
        f.write(b'BM')
        f.write(struct.pack('<IHHI', file_size, 0, 0, 54))
        f.write(struct.pack('<IIIHHIIIIII', 40, width, height, 1, 24, 0, image_data_size, 2835, 2835, 0, 0))
        padding = b'\x00' * (row_stride - width * 3)
        for y in range(height):
            row = bytearray()
            for x in range(width):
                if (x // 64) % 2 == (y // 64) % 2:
                    b = (x * 255 // width)
                    g = (y * 255 // height)
                    r = 180
                else:
                    b = 40
                    g = ((x + y) * 255 // (width + height))
                    r = (x * 255 // width)
                row.extend([b, g, r])
            row.extend(padding)
            f.write(row)
    print(f"[Dataset] Fichier image BMP genere : {filepath} ({os.path.getsize(filepath) / (1024*1024):.2f} MB)")

def generate_video_sample(filepath: str, width: int = 320, height: int = 240, frames_count: int = 40):
    '''Genere un flux video brut YUV/RGB multi-trames (~3 MB).'''
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    frame_size = width * height * 3
    
    with open(filepath, 'wb') as f:
        # En-tete maison Video Raw Frame Stream
        f.write(b'RAWVID01')
        f.write(struct.pack('<III', width, height, frames_count))
        for frame_idx in range(frames_count):
            ball_x = int((frame_idx * 12) % width)
            ball_y = int(height / 2 + 40 * math.sin(frame_idx * 0.25))
            frame_data = bytearray()
            for y in range(height):
                for x in range(width):
                    dist_sq = (x - ball_x)**2 + (y - ball_y)**2
                    if dist_sq < 20 * 20:
                        frame_data.extend([255, 30, 30])
                    else:
                        frame_data.extend([30, (x * 120 // width), (y * 120 // height)])
            f.write(frame_data)
    print(f"[Dataset] Fichier video RAW genere : {filepath} ({os.path.getsize(filepath) / (1024*1024):.2f} MB)")

def generate_all_datasets(data_dir: str):
    os.makedirs(data_dir, exist_ok=True)
    text_path = os.path.join(data_dir, "texte_source.txt")
    audio_path = os.path.join(data_dir, "audio_source.wav")
    image_path = os.path.join(data_dir, "image_source.bmp")
    video_path = os.path.join(data_dir, "video_source.raw")
    
    if not os.path.exists(text_path): generate_text_sample(text_path)
    if not os.path.exists(audio_path): generate_audio_sample(audio_path)
    if not os.path.exists(image_path): generate_image_sample(image_path)
    if not os.path.exists(video_path): generate_video_sample(video_path)
    
    return {
        "texte": text_path,
        "audio": audio_path,
        "image": image_path,
        "video": video_path
    }

if __name__ == "__main__":
    generate_all_datasets("test_data")

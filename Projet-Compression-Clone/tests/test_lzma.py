# -*- coding: utf-8 -*-
import unittest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import src.lzma_clone as lzma_clone
from src.core.metrics import calculate_sha256

class TestLzmaClone(unittest.TestCase):
    def setUp(self):
        self.test_dir = os.path.join(os.path.dirname(__file__), "tmp_lz")
        os.makedirs(self.test_dir, exist_ok=True)
        self.sample_txt = os.path.join(self.test_dir, "sample.txt")
        with open(self.sample_txt, "w", encoding="utf-8") as f:
            f.write("Test lzma xz clone algorithm " * 1000)

    def tearDown(self):
        import shutil
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_compress_and_decompress(self):
        xz_path = self.sample_txt + ".xz"
        decomp_path = self.sample_txt + ".decomp"

        # Compression
        ok_comp = lzma_clone.compress_file(self.sample_txt, dst_path=xz_path, preset=6, keep=True, force=True)
        self.assertTrue(ok_comp)
        self.assertTrue(os.path.exists(xz_path))
        self.assertLess(os.path.getsize(xz_path), os.path.getsize(self.sample_txt))

        # Test d'integrite
        ok_test = lzma_clone.test_file_integrity(xz_path)
        self.assertTrue(ok_test)

        # Decompression
        ok_decomp = lzma_clone.decompress_file(xz_path, dst_path=decomp_path, keep=True, force=True)
        self.assertTrue(ok_decomp)
        self.assertTrue(os.path.exists(decomp_path))

        # Verification SHA-256
        self.assertEqual(calculate_sha256(self.sample_txt), calculate_sha256(decomp_path))

if __name__ == "__main__":
    unittest.main()

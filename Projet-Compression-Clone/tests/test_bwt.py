# -*- coding: utf-8 -*-
import unittest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.core.bwt import bwt_transform, bwt_inverse, mtf_transform, mtf_inverse, rle_encode, rle_decode

class TestBWTAlgorithms(unittest.TestCase):
    def test_bwt_roundtrip(self):
        data = b"BANANA$BANANA$BURROWS_WHEELER_TRANSFORM"
        transformed, primary_idx = bwt_transform(data)
        reconstructed = bwt_inverse(transformed, primary_idx)
        self.assertEqual(data, reconstructed)

    def test_mtf_roundtrip(self):
        data = b"ABRACADABRA_MOVE_TO_FRONT"
        mtf_data = mtf_transform(data)
        reconstructed = mtf_inverse(mtf_data)
        self.assertEqual(data, reconstructed)

    def test_rle_roundtrip(self):
        data = b"AAAAABBBBBCCCCCCCDDDDEEEEE"
        compressed = rle_encode(data)
        decompressed = rle_decode(compressed)
        self.assertEqual(data, decompressed)

if __name__ == "__main__":
    unittest.main()

# -*- coding: utf-8 -*-
import unittest
import os
import sys
import shutil

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import src.sevenzip_clone as sevenzip_clone
from src.core.metrics import calculate_sha256

class TestSevenZipClone(unittest.TestCase):
    def setUp(self):
        self.test_dir = os.path.join(os.path.dirname(__file__), "tmp_7z")
        os.makedirs(self.test_dir, exist_ok=True)
        self.sample_txt = os.path.join(self.test_dir, "sample.txt")
        with open(self.sample_txt, "w", encoding="utf-8") as f:
            f.write("Test 7-Zip LZMA2 archive clone " * 1000)

    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_7z_workflow(self):
        archive_7z = os.path.join(self.test_dir, "test.7z")
        extract_dir = os.path.join(self.test_dir, "out")

        # 1. Ajout (a)
        ok_a = sevenzip_clone.add_to_archive(archive_7z, [self.sample_txt], level=5, method="lzma2")
        self.assertTrue(ok_a)
        self.assertTrue(os.path.exists(archive_7z))

        # 2. Liste (l)
        ok_l = sevenzip_clone.list_archive(archive_7z)
        self.assertTrue(ok_l)

        # 3. Test d'integrite (t)
        ok_t = sevenzip_clone.test_archive(archive_7z)
        self.assertTrue(ok_t)

        # 4. Extraction (x)
        ok_x = sevenzip_clone.extract_archive(archive_7z, output_dir=extract_dir, flat=True)
        self.assertTrue(ok_x)
        extracted_file = os.path.join(extract_dir, "sample.txt")
        self.assertTrue(os.path.exists(extracted_file))

        # 5. Verification SHA-256
        self.assertEqual(calculate_sha256(self.sample_txt), calculate_sha256(extracted_file))

if __name__ == "__main__":
    unittest.main()

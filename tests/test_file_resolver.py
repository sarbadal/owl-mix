# tests/test_file_resolver.py
import sys
import warnings
from pathlib import Path

warnings.simplefilter('ignore', category=UserWarning)

# Add src to the path
CURRENT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = CURRENT_DIR.parent
SRC_DIR = (PROJECT_ROOT / "src").resolve()
sys.path.append(str(SRC_DIR))


import unittest
import tempfile
import shutil
from pathlib import Path
from owlmix.utils.file_resolver import ConfigFileResolver

class TestConfigFileResolver(unittest.TestCase):
    def setUp(self):
        # Setup temp directory and files
        self.test_dir = tempfile.mkdtemp()
        self.config_path = Path(self.test_dir) / "config.json"
        self.resolved_path = Path(self.test_dir) / "resolved_config.json"
        self.config_path.write_text('{"vif_chart": {"title": "Chart title", "alt_text": "alt text", "description": "desc"}}')

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_resolve_and_save(self):
        resolver = ConfigFileResolver(config=self.config_path)
        resolved_config = resolver.resolve()
        self.assertIn("vif_chart", resolved_config)
        resolver.save(self.resolved_path)
        self.assertTrue(self.resolved_path.exists())

    def test_to_python_string(self):
        resolver = ConfigFileResolver(config=self.config_path)
        resolver.resolve()
        py_str = resolver.to_python_string()
        self.assertIsInstance(py_str, str)
        self.assertIn("vif_chart", py_str)

    def test_invalid_path(self):
        with self.assertRaises(Exception):
            ConfigFileResolver(config=Path("nonexistent.json")).resolve()

if __name__ == "__main__":
    unittest.main()
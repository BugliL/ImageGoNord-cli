from unittest import TestCase

import io
from pathlib import Path
from unittest import TestCase
from unittest.mock import patch


class UnitTestBaseClass(TestCase):
    DATA_PATH = Path(__file__).parent / "data"
    DEFAULT_OUTPUT_FILE_PATH = Path("nord.png")
    DEFAULT_INPUT_FILE_PATH = DATA_PATH / "blue_square.png"

    def tearDown(self) -> None:
        self.stdout_patch.stop()

        # Delete the output image if exists
        std_output_path = Path("nord.png")
        if std_output_path.exists():
            std_output_path.unlink()

        # Delete the output image if exists
        std_output_path = Path("self.mocked_stdout.jpg")
        if std_output_path.exists():
            std_output_path.unlink()

    def setUp(self) -> None:
        self.stdout_patch = patch("sys.stdout", new_callable=io.StringIO)
        self.mocked_stdout = self.stdout_patch.start()

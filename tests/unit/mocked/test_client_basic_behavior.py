from pathlib import Path
import tempfile
import unittest

from image_go_nord_client.main import main
from .unit_test_base_class import UnitTestBaseClass


class ClientShould(UnitTestBaseClass):
    def test_return_docs_when_given_help_parameter(self):
        main(argv=["image-go-nord-client", "--help"])
        self.assertIn(
            "ImageGoNord, a converter for a rgb images to norththeme palette",
            self.mocked_stdout.getvalue(),
        )

        main(argv=["image-go-nord-client", "-h"])
        self.assertIn(
            "ImageGoNord, a converter for a rgb images to norththeme palette",
            self.mocked_stdout.getvalue(),
        )

    def test_return_version_docs_when_given_version_parameter(self):
        main(argv=["image-go-nord-client", "--version"])
        self.assertEqual("0.1.0", self.mocked_stdout.getvalue().strip())

        main(argv=["image-go-nord-client", "-v"])
        self.assertIn("0.1.0", self.mocked_stdout.getvalue().strip())

    def test_no_output_when_convert_to_nord_palette_and_quiet_parameter_provided(self):
        main(argv=["image-go-nord-client", f"-i={self.DEFAULT_INPUT_FILE_PATH}", "-q"])
        self.assertEqual("", self.mocked_stdout.getvalue())

        main(
            argv=[
                "image-go-nord-client",
                f"--img={self.DEFAULT_INPUT_FILE_PATH}",
                "--quiet",
            ]
        )
        self.assertEqual("", self.mocked_stdout.getvalue())

    def test_convert_to_nord_palette_when_given_only_short_img_parameter(self):
        main(argv=["image-go-nord-client", f"-i={self.DEFAULT_INPUT_FILE_PATH}"])
        self.assertTrue(self.DEFAULT_OUTPUT_FILE_PATH.exists())

    def test_convert_to_nord_palette_when_given_only_long_img_parameter(self):
        main(argv=["image-go-nord-client", f"--img={self.DEFAULT_INPUT_FILE_PATH}"])
        self.assertTrue(self.DEFAULT_OUTPUT_FILE_PATH.exists())

    @unittest.skip("TODO: Implement this test")
    def test_convert_to_nord_palette_when_given_only_short_img_and_out_parameters(self):
        with tempfile.TemporaryDirectory() as tmpdirname:
            output_path = Path(tmpdirname) / "output2.png"
            main(
                argv=[
                    "image-go-nord-client",
                    f"-i={self.DEFAULT_INPUT_FILE_PATH}",
                    f"-o={output_path}",
                ]
            )

            self.assertTrue(output_path.exists())

    def test_convert_to_nord_palette_when_given_only_long_img_and_out_parameters(self):
        with tempfile.TemporaryDirectory(suffix="long_img") as tmpdirname:
            output_path = Path(tmpdirname) / "output1.png"
            main(
                argv=[
                    "image-go-nord-client",
                    f"--img={self.DEFAULT_INPUT_FILE_PATH}",
                    f"--out={output_path}",
                ]
            )
            self.assertTrue(output_path.parent.exists())
            self.assertTrue(output_path.exists())

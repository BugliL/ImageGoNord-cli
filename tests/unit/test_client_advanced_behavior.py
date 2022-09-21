import tempfile
from pathlib import Path

from tests.unit.unit_test_base_class import UnitTestBaseClass
from tests.utils import run_image_go_nord_client


class ClientShould(UnitTestBaseClass):
    # Get blue_suqare.png path from data folder
    data = Path(__file__).parent.parent / 'data'
    input_image_path = data / 'blue_square.png'
    expected_image_path = data / 'blue_nord_square.png'

    def test_convert_to_nord_palette_using_no_avg_pixels_parameter(self):
        # Create a temporary folder to store the output image
        # Run the script with the image path input and output and check result
        with tempfile.TemporaryDirectory() as tmpdirname:
            output_image_path = Path(tmpdirname) / 'output.png'
            input_image_path = self.data / 'blue_red_square.png'

            self.run_test(
                input_image_path,
                output_image_path,
                self.data / 'blue_red_nord_na_square.png',
                f'-i={input_image_path}',
                f'-o={output_image_path}',
                '--no-avg-pixels'
            )

    def test_convert_to_nord_palette_using_no_avg_pixels_short_parameter(self):
        # Create a temporary folder to store the output image
        # Run the script with the image path input and output and check result
        with tempfile.TemporaryDirectory() as tmpdirname:
            output_image_path = Path(tmpdirname) / 'output.png'
            input_image_path = self.data / 'blue_red_square.png'

            self.run_test(
                self.data / 'blue_red_square.png',
                output_image_path,
                self.data / 'blue_red_nord_na_square.png',
                f'-i={input_image_path}',
                f'-o={output_image_path}',
                '-na'
            )

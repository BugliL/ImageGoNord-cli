import io
from unittest import TestCase
from unittest.mock import patch

from image_go_nord_client.main import main

class ClientShould(TestCase):
    
    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.argv', ['image-go-nord-client', '--help'])
    def test_return_docs_when_given_help_parameter(self, output: io.StringIO):
        main()
        self.assertIn("ImageGoNord, a converter for a rgb images to norththeme palette", output.getvalue())
        
        
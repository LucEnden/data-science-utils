import unittest
from unittest.mock import patch, MagicMock
from dsutils.setup import setup as dsutils_setup
import json
import os
import shutil


JSON_DATA_FILE = os.path.abspath(os.path.dirname(__file__) + '/../dsutils/files_and_folders.json')
with open(JSON_DATA_FILE) as f:
    json_data = json.load(f)


class TestSetup(unittest.TestCase):
    def setUp(self):
        # Create the test directory
        self.test_dir = os.path.abspath(os.path.dirname(__file__) + '/test_setup_dir/')
        os.mkdir(self.test_dir)            

    def tearDown(self):
        # Remove the contents of the test directory
        shutil.rmtree(self.test_dir)

    @patch('dsutils.create_files_and_folders.dsutils_info')
    @patch('dsutils.create_files_and_folders.dsutils_success')
    @patch('dsutils.setup.create_files_and_folders')
    @patch('dsutils.setup.dsutils_input_yes_no', return_value='y')
    @patch('dsutils.setup.dsutils_info')
    @patch('dsutils.setup.dsutils_success')
    @patch('dsutils.setup.argparse.ArgumentParser.parse_args')
    @patch('os.path.isfile', return_value=False)
    @patch('builtins.open', new_callable=unittest.mock.mock_open)
    @patch('json.load', return_value=json_data)
    def test_main(self, mock_json_load, mock_open, mock_isfile, mock_parse_args, mock_setup_success, mock_setup_info, mock_input_yes_no, mock_create_files_and_folders, mock_cfaf_success, mock_cfaf_info):
        mock_args = MagicMock()
        mock_args.projectroot = self.test_dir
        mock_parse_args.return_value = mock_args

        dsutils_setup()

        mock_parse_args.assert_called_once()
        mock_create_files_and_folders.assert_called_once()

if __name__ == '__main__':
    unittest.main()
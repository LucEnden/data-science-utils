import unittest
from unittest.mock import patch, mock_open
from dsutils.create_files_and_folders import create_files_and_folders
import os
import json
import shutil


JSON_DATA_FILE = os.path.abspath(os.path.dirname(__file__) + '/../dsutils/files_and_folders.json')
with open(JSON_DATA_FILE) as f:
    json_data = json.load(f)


class TestCreateFilesAndFolders(unittest.TestCase):
    def setUp(self):
        # Create the test directory
        self.test_dir = os.path.abspath(os.path.dirname(__file__) + '/test_create_files_and_folders_dir/')
        os.mkdir(self.test_dir)            

    def tearDown(self):
        # Remove the contents of the test directory
        shutil.rmtree(self.test_dir)

    @patch('dsutils.create_files_and_folders.dsutils_info')
    @patch('dsutils.create_files_and_folders.dsutils_success')
    @patch('json.load', return_value=json_data)
    def test_create_files_and_folders(self, mock_json_load, mock_success, mock_info):
        #====      Arange      ====#
        result: list[str] = None

        #====       Act        ====#
        result = create_files_and_folders(self.test_dir)

        #====      Assert      ====#

        # Check if the function calls dsutils_success
        mock_json_load.assert_called_once()

        # Check if the function returns a list
        self.assertIsInstance(result, list)

        # Check if all files and folders passed to the function are returned
        for fReal, fResult in zip(json_data, result):
            self.assertEqual(fResult, json_data[fReal]["path"])

        # Check if all files and folders are created
        for f in result:
            self.assertTrue(os.path.exists(f))


if __name__ == '__main__':
    unittest.main()
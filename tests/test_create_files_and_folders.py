import unittest
from unittest.mock import patch
from dsutils.create_files_and_folders import create_files_and_folders, __get_files_and_folders_from_json__, __remove_files_and_folders__
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
    def test_SYSTEM_create_files_and_folders(self, mock_json_load, mock_success, mock_info):
        """
        Test if the function creates all files and folders passed to it.
        """
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


    @patch('dsutils.create_files_and_folders.__remove_files_and_folders__')
    @patch('dsutils.create_files_and_folders.dsutils_info')
    @patch('dsutils.create_files_and_folders.dsutils_success')
    @patch('dsutils.create_files_and_folders.dsutils_error')
    @patch('json.load', return_value=json_data)
    def test_SYSTEM_create_files_and_folders_with_invalid_path(self, mock_json_load, mock_error, mock_success, mock_info, mock_remove):
        """
        Test if the function handles an invalid path gracefully.
        """
        #====      Arange      ====#
        result: list[str] = None
        none_existing_path = os.path.join(self.test_dir, '/none_existing_path/')

        #====       Act        ====#
        with self.assertRaises(SystemExit):
            result = create_files_and_folders(none_existing_path)

        #====      Assert      ====#
        # Should not raise an exception
        self.assertTrue(True)


    @patch('dsutils.create_files_and_folders.dsutils_info')
    @patch('dsutils.create_files_and_folders.dsutils_success')
    @patch('dsutils.create_files_and_folders.dsutils_warn')
    @patch('dsutils.create_files_and_folders.dsutils_error')
    def test_SYSTEM_call_create_files_and_folders_twice(self, mock_error, mock_warn, mock_success, mock_info):
        """
        Test if warning is given after create_files_and_folders is called twice.
        Should not raise an exception but should give a warning.
        """
        #====      Arange      ====#

        #====       Act        ====#
        create_files_and_folders(self.test_dir)
        create_files_and_folders(self.test_dir)

        #====      Assert      ====#
        # Should not raise an exception
        self.assertTrue(True)
        mock_warn.assert_called()

    @patch('dsutils.internals.dsutils_warn')
    @patch('dsutils.internals.dsutils_error')
    @patch('dsutils.create_files_and_folders.dsutils_info')
    @patch('dsutils.create_files_and_folders.dsutils_warn')
    @patch('dsutils.create_files_and_folders.dsutils_error')
    def test_SYSTEM_create_files_and_folders_with_empty_path(self, mock_cfaf_error, mock_cfaf_warn, mock_cfaf_info, mock_int_error, mock_int_warn):
        """
        Test if the function handles an empty path gracefully.
        """
        #====      Arange      ====#
        result: list[str] = None
        empty_path = ""

        #====       Act        ====#
        with self.assertRaises(SystemExit):
            result = create_files_and_folders(empty_path)

        #====      Assert      ====#
        # Should not raise an exception
        self.assertTrue(True)


    @patch('dsutils.internals.dsutils_warn')
    @patch('dsutils.internals.dsutils_error')
    @patch('dsutils.create_files_and_folders.dsutils_warn')
    @patch('dsutils.create_files_and_folders.dsutils_error')
    def test_SYSTEM_create_files_and_folders_with_None_path(self, mock_cfaf_error, mock_cfaf_warn, mock_int_error, mock_int_warn):
        """
        Test if the function handles an None path gracefully.
        """
        #====      Arange      ====#
        result: list[str] = None
        empty_path = None

        #====       Act        ====#
        with self.assertRaises(SystemExit):
            result = create_files_and_folders(empty_path)

        #====      Assert      ====#
        # Should not raise an exception
        self.assertTrue(True)


    @patch('dsutils.internals.dsutils_warn')
    @patch('dsutils.internals.dsutils_error')
    @patch('dsutils.create_files_and_folders.dsutils_warn')
    @patch('dsutils.create_files_and_folders.dsutils_error')    
    def test_SYSTEM___remove_files_and_folders___with_non_existing_path(self, mock_cfaf_error, mock_cfaf_warn, mock_int_error, mock_int_warn):
        """
        Test if __remove_files_and_folders__ handles an invalid path gracefully.
        """
        #====      Arange      ====#
        result: list[str] = None
        non_existing_path = "none_existing_path"

        #====       Act        ====#
        with self.assertRaises(SystemExit):
            result = __remove_files_and_folders__(non_existing_path)

        #====      Assert      ====#
        # Should not raise an exception
        self.assertTrue(True)


    @patch('dsutils.internals.dsutils_warn')
    @patch('dsutils.internals.dsutils_error')
    @patch('dsutils.create_files_and_folders.dsutils_info')
    @patch('dsutils.create_files_and_folders.dsutils_warn')
    @patch('dsutils.create_files_and_folders.dsutils_error')
    @patch('dsutils.create_files_and_folders.dsutils_success')
    def test_SYSTEM_call_create_and_then_remove_with_valid_path(self, mock_cfaf_success, mock_cfaf_error, mock_cfaf_warn, mock_cfaf_info, mock_int_error, mock_int_warn):
        """
        Tests if the create and remove function removes all created files and folders.
        """
        #====      Arange      ====#
        result: list[str] = None

        #====       Act        ====#
        result = create_files_and_folders(self.test_dir)
        __remove_files_and_folders__(self.test_dir)

        #====      Assert      ====#
        # Should not raise an exception
        self.assertTrue(True)

        # Check if all files and folders are removed
        for f in result:
            self.assertFalse(os.path.exists(f))


if __name__ == '__main__':
    unittest.main()
import unittest
import json
import os


JSON_DATA_FILE = os.path.abspath(os.path.dirname(__file__) + '/../dsutils/files_and_folders.json')
with open(JSON_DATA_FILE) as f:
    json_data = json.load(f)


class TestFilesAndFolders(unittest.TestCase):
    def setUp(self):
        self.files_and_folders = json_data

    def test_CONVENTION_all_entries_have_attributes(self):
        """
        All entries in the files_and_folders.json file should have the following attributes:
        - path
        - isFile
        - fileContents
        """
        for f in self.files_and_folders:
            self.assertIn('path', self.files_and_folders[f])
            self.assertIn('isFile', self.files_and_folders[f])
            self.assertIn('fileContents', self.files_and_folders[f])

    def test_CONVENTION_all_paths_are_string(self):
        """
        All paths in the files_and_folders.json file should be strings.
        """
        for f in self.files_and_folders:
            self.assertIsInstance(self.files_and_folders[f]['path'], str)

    def test_CONVENTION_all_paths_start_with_backslash(self):
        """
        All paths in the files_and_folders.json file should start with a backslash.
        """
        for f in self.files_and_folders:
            self.assertTrue(self.files_and_folders[f]['path'].startswith('/'))

    def test_CONVENTION_all_paths_are_unique(self):
        """
        All paths in the files_and_folders.json file should be unique.
        """
        paths = [self.files_and_folders[f]['path'] for f in self.files_and_folders]
        self.assertEqual(len(paths), len(set(paths)))

    def test_CONVENTION_all_isfile_are_boolean(self):
        """
        All isFile attributes in the files_and_folders.json file should be boolean.
        """
        for f in self.files_and_folders:
            self.assertIsInstance(self.files_and_folders[f]['isFile'], bool)

    def test_CONVENTION_all_file_contents_are_string_or_list(self):
        """
        All fileContents attributes in the files_and_folders.json file should be string or list.
        """
        for f in self.files_and_folders:
            self.assertIsInstance(self.files_and_folders[f]['fileContents'], (str, list))


if __name__ == '__main__':
    unittest.main()
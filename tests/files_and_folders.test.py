import unittest
import json


class TestFilesAndFoldersEntries(unittest.TestCase):
    def setUp(self) -> None:
        self.json_file = 'files_and_folders.json'
        with open(self.json_file, 'r') as file:
            self.files_and_folders = json.load(file)
        
        return super().setUp()
    
    def test_all_entries_have_entries(self):
        for f in self.files_and_folders:
            self.assertIn('path', self.files_and_folders[f])
            self.assertIn('isFile', self.files_and_folders[f])
            self.assertIn('fileContents', self.files_and_folders[f])

    def test_all_paths_are_string(self):
        for f in self.files_and_folders:
            self.assertIsInstance(self.files_and_folders[f]['path'], str)

    def test_all_paths_start_with_backslash(self):
        for f in self.files_and_folders:
            self.assertTrue(self.files_and_folders[f]['path'].startswith('/'))

    def test_all_paths_are_unique(self):
        paths = [self.files_and_folders[f]['path'] for f in self.files_and_folders]
        self.assertEqual(len(paths), len(set(paths)))

    def test_all_isfile_are_boolean(self):
        for f in self.files_and_folders:
            self.assertIsInstance(self.files_and_folders[f]['isFile'], bool)

    def test_all_file_contents_are_string_or_list(self):
        for f in self.files_and_folders:
            self.assertIsInstance(self.files_and_folders[f]['fileContents'], (str, list))


if __name__ == '__main__':
    unittest.main()
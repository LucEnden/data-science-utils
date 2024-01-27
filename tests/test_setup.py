import unittest
from unittest.mock import patch
from dsutils.setup import setup


class TestSetup(unittest.TestCase):
    # @patch('os.path.isfile', return_value=True)
    # @patch('os.remove')
    # @patch('setup.__remove_files_and_folders__')
    # def test_cleanup(self, mock_remove_files_and_folders, mock_os_remove, mock_isfile):
    #     __cleanup__()
    #     mock_isfile.assert_called_once()
    #     mock_os_remove.assert_called_once()
    #     mock_remove_files_and_folders.assert_called_once()

    @patch('argparse.ArgumentParser.parse_args')
    @patch('setup.create_files_and_folders')
    @patch('setup.dsutils_input', return_value='test_directory')
    @patch('os.path.isdir', return_value=True)
    @patch('os.path.isfile', return_value=False)
    @patch('builtins.open', new_callable=unittest.mock.mock_open)
    def test_main(self, mock_open, mock_isfile, mock_isdir, mock_dsutils_input, mock_create_files_and_folders, mock_parse_args):
        setup()
        mock_parse_args.assert_called_once()
        mock_dsutils_input.assert_called_once()
        mock_isdir.assert_called_once()
        mock_isfile.assert_called_once()
        mock_open.assert_called_once()
        mock_create_files_and_folders.assert_called_once()

if __name__ == '__main__':
    unittest.main()
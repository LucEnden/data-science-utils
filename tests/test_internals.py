import unittest
from unittest.mock import patch, MagicMock
from dsutils.internals import dsutils_read_env, ENV_FILE
import os
import shutil

class TestInternals(unittest.TestCase):
    def setUp(self):
        # Create the test directory
        self.test_dir = os.path.abspath(os.path.dirname(__file__) + '/test_internals_dir/')
        if os.path.isdir(self.test_dir):
            shutil.rmtree(self.test_dir)
        os.mkdir(self.test_dir)            

    def tearDown(self):
        # Remove the contents of the test directory
        if os.path.isdir(self.test_dir):
            shutil.rmtree(self.test_dir)


    def test_UNIT_dsutils_read_env_returns_dict(self):
        """
        Test that dsutils_read_env returns a dictionary containing the environment variables
        """
        #====      Arange      ====#
        dict_to_write = {
            'TEST_VAR_1': 'test_var_value_1',
            'TEST_VAR_2': 'test_var_value_2',
            'TEST_VAR_3': 'test_var_value_3'
        }
        with open(self.test_dir + ENV_FILE, 'w') as f:
            f.write('\n'.join([f'{key}={value}' for key, value in dict_to_write.items()]))

        #====      Act      ====#
        result = dsutils_read_env(self.test_dir)
        
        #====      Assert      ====#
        self.assertEqual(result, dict_to_write)


    @patch('dsutils.internals.dsutils_error')
    def test_UNIT_dsutils_read_env_should_exit_with_code_1_when_env_file_does_not_exist(self, mock_dsutils_error):
        """
        Test that dsutils_read_env should exit with code 1 when the env file does not exist
        """
        #====      Arange      ====#

        #====      Act      ====#
        with self.assertRaises(SystemExit) as cm:
            dsutils_read_env()

        #====      Assert      ====#
        self.assertEqual(cm.exception.code, 1)


if __name__ == '__main__':
    unittest.main()
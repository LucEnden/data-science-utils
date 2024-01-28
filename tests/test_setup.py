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
        if os.path.isdir(self.test_dir):
            shutil.rmtree(self.test_dir)
        os.mkdir(self.test_dir)            

    def tearDown(self):
        # Remove the contents of the test directory
        if os.path.isdir(self.test_dir):
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
    def test_SYSTEM_setup_with_expected_inputs_should_succeed(self, mock_json_load, mock_open, mock_isfile, mock_parse_args, mock_setup_success, mock_setup_info, mock_input_yes_no, mock_create_files_and_folders, mock_cfaf_success, mock_cfaf_info):
        """
        Tests what happens when the setup function is called and the user enters a valid project root directory.
        - The user enters the correct project root directory
        - The .dsutils.env file does not exist
        - The user says agrees with every yes/no question

        The test should succeed without any errors.
        As such, we do not need to catch any exceptions.
        """
        #====      Arange      ====#
        mock_args = MagicMock()
        mock_args.projectroot = self.test_dir
        mock_parse_args.return_value = mock_args

        #====       Act        ====#
        dsutils_setup()

        #====      Assert      ====#
        mock_parse_args.assert_called_once()
        mock_create_files_and_folders.assert_called_once()


    @patch('dsutils.setup.__cleanup__')
    @patch('dsutils.setup.create_files_and_folders')
    @patch('dsutils.setup.dsutils_input_yes_no')
    @patch('dsutils.setup.dsutils_info')
    @patch('dsutils.setup.dsutils_success')
    @patch('dsutils.setup.dsutils_error')
    @patch('dsutils.setup.argparse.ArgumentParser.parse_args')
    def test_SYSTEM_setup_keyboard_interrupt(self, mock_parse_args, mock_error, mock_success, mock_info, mock_input_yes_no, mock_create_files_and_folders, mock_cleanup):
        """
        Tests what happens when the setup function is called and a KeyboardInterrupt is raised during the setting of the project root directory.
        - The user enters any project root directory
        - The setup function asks the user if the root directory is correct
        - A KeyboardInterrupt is pressed

        The test should exit with status 1 and raise a KeyboardInterrupt.
        Files and folders should also not be created.
        """
        #====      Arange      ====#
        mock_args = MagicMock()
        mock_args.projectroot = self.test_dir
        mock_parse_args.return_value = mock_args

        # Make dsutils_input_yes_no raise a KeyboardInterrupt
        mock_input_yes_no.side_effect = KeyboardInterrupt

        #====       Act        ====#
        with self.assertRaises(SystemExit) as cm:
            dsutils_setup()

        #====      Assert      ====#
        # Check that create_files_and_folders was not called
        mock_create_files_and_folders.assert_not_called()

        # Check that the program exited with status 1
        self.assertEqual(cm.exception.code, 1)


    @patch('dsutils.setup.dsutils_input')
    @patch('dsutils.setup.dsutils_input_yes_no')
    @patch('dsutils.setup.create_files_and_folders')
    @patch('dsutils.setup.dsutils_info')
    @patch('dsutils.setup.dsutils_warn')
    @patch('dsutils.setup.dsutils_success')
    @patch('dsutils.setup.argparse.ArgumentParser.parse_args')
    def test_SYSTEM_setup_missing_project_root_arg(self, mock_parse_args, mock_success, mock_warn, mock_info, mock_cfaf, mock_input_yes_no, mock_input):
        """
        Tests what happens when the setup function is called and the user does not pass a value for the project root directory argument.
        - The user does not enter pass a value for the project root directory argument
        - The setup function calls the input function to ask the user for the project root directory
        - The user does not enter an ampty string as the new project root directory
        - The setup function sets the project root directory to the current working directory
        - The setup function calls the input_yes_no function to ask the user if the project root directory is correct
        - The user enters 'n'
        - The setup function calls the input function to ask the user for the project root directory
        - The user enters the a different project root directory
        - The setup function calls the input_yes_no function to ask the user if the project root directory is correct
        - The user enters 'y'
        - The setup function calls the create_files_and_folders function
        - The setup function calls the success function to inform the user that the project root directory was set

        After this, the test should succeed without any errors.
        """

        #====      Arange      ====#
        empty_project = ""
        new_project_dir = self.test_dir
        yes_no_first = False
        yes_no_second = True

        mock_input_yes_no.side_effect = [yes_no_first, yes_no_second]
        mock_input.side_effect = [empty_project, new_project_dir]
        mock_args = MagicMock()
        mock_args.projectroot = None
        mock_parse_args.return_value = mock_args

        #====       Act        ====#
        dsutils_setup()

        #====      Assert      ====#
        mock_parse_args.assert_called_once()
        self.assertEqual(mock_input.call_count, 2)
        self.assertEqual(mock_input_yes_no.call_count, 2)
        mock_cfaf.assert_called_once()
        mock_success.assert_called()


    @patch('dsutils.setup.input')
    @patch('dsutils.setup.dsutils_input_yes_no')
    @patch('dsutils.setup.create_files_and_folders')
    @patch('dsutils.setup.dsutils_success')
    @patch('dsutils.setup.dsutils_info')
    @patch('dsutils.setup.dsutils_warn')
    @patch('dsutils.setup.argparse.ArgumentParser.parse_args')
    def test_SYSTEM_setup_env_file_exists_and_users_overwrites_it(self, mock_parse_args, mock_warn, mock_info, mock_success, mock_create_files_and_folders, mock_input_yes_no, mock_input):
        """
        Tests what happens when the setup function is called and the .dsutils.env file already exists and the user wants to overwrite it.
        - The user enters the correct project root directory
        - The setup function asks the user if the project root directory is correct
        - The user enters 'y'
        - The .dsutils.env file exists
        - The setup function asks the user if they want to overwrite the existing environment file
        - The user enters 'y'
        - The setup function calls the create_files_and_folders function
        - The setup function calls the success function to inform the user that the project root directory was set

        The test should succeed without any errors.
        As such, we do not need to catch any exceptions.
        """
        #====      Arrange      ====#
        mock_args = MagicMock()
        mock_args.projectroot = self.test_dir
        mock_parse_args.return_value = mock_args

        mock_input_yes_no.side_effect = ['y', 'y']

        # Create the .dsutils.env file
        with open(self.test_dir + '/.dsutils.env', 'w') as f:
            f.write('')

        #====       Act        ====#
        if os.path.isfile(self.test_dir + '/.dsutils.env'):
            # Call the setup function
            dsutils_setup()
        else:
            raise Exception("Test failed to create the required .dsutils.env file")

        #====      Assert      ====#
        # Check that the dsutils_error function was called
        mock_warn.assert_called()
        mock_input_yes_no.assert_called()
        mock_create_files_and_folders.assert_called()
        mock_success.assert_called()


    @patch('dsutils.setup.create_files_and_folders')
    @patch('dsutils.setup.dsutils_input_yes_no')
    @patch('dsutils.setup.dsutils_info')
    @patch('dsutils.setup.dsutils_warn')
    @patch('dsutils.setup.dsutils_success')
    @patch('dsutils.setup.argparse.ArgumentParser.parse_args')
    def test_SYSTEM_setup_dont_overwrite_env_file(self, mock_parse_args, mock_success, mock_warn, mock_info, mock_input_yes_no, mock_cfaf):
        """
        Emulates the user not wanting to overwrite the existing environment file.
        - The user enters a correct project root directory
        - The setup function asks the user if the project root directory is correct
        - The user enters 'y'
        - The .dsutils.env file exists
        - The setup function asks the user if they want to overwrite the existing environment file
        - The user enters 'n'
        - The setup function exits with status 0

        The test should succeed without any errors.
        As such, we do not need to catch any exceptions.
        """
        #====      Arrange      ====#
        mock_args = MagicMock()
        mock_args.projectroot = self.test_dir
        mock_parse_args.return_value = mock_args

        mock_input_yes_no.side_effect = [True, False]

        # Create the .dsutils.env file
        with open(self.test_dir + '/.dsutils.env', 'w') as f:
            f.write('')

        #====       Act        ====#
        if os.path.isfile(self.test_dir + '/.dsutils.env'):
            # Call the setup function
            with self.assertRaises(SystemExit):
                dsutils_setup()
        else:
            raise Exception("Test failed to create the required .dsutils.env file")

        #====      Assert      ====#
        mock_parse_args.assert_called_once()
        mock_input_yes_no.assert_called()
        self.assertEqual(mock_input_yes_no.call_count, 2)
        # Program should exit with status 0
        mock_cfaf.assert_not_called()



            
if __name__ == '__main__':
    unittest.main()
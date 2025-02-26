#!/usr/bin/env python3

import unittest
from unittest.mock import patch, MagicMock
import os
import tempfile
import subprocess
from tools.git_automation import (
    run_command,
    get_changed_files,
    get_branch_name,
    create_commit_message,
    commit_changes,
    create_pr,
    create_feature_branch
)

class TestGitAutomation(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures."""
        self.mock_process = MagicMock()
        self.mock_process.stdout = "test output"
        self.mock_process.stderr = "test error"
        
    @patch('subprocess.run')
    def test_run_command_success(self, mock_run):
        """Test successful command execution."""
        mock_run.return_value = self.mock_process
        result = run_command(['test', 'command'])
        mock_run.assert_called_once_with(
            ['test', 'command'],
            capture_output=True,
            text=True,
            check=True
        )
        self.assertEqual(result, self.mock_process)
    
    @patch('subprocess.run')
    def test_run_command_failure(self, mock_run):
        """Test command execution failure."""
        mock_run.side_effect = subprocess.CalledProcessError(1, ['test'], 'error')
        with self.assertRaises(SystemExit):
            run_command(['test', 'command'])
    
    @patch('tools.git_automation.run_command')
    def test_get_changed_files(self, mock_run):
        """Test getting changed files."""
        mock_run.return_value.stdout = " M file1.py\n M file2.py\n"
        files = get_changed_files()
        self.assertEqual(files, ['file1.py', 'file2.py'])
        mock_run.assert_called_once_with(['git', 'status', '--porcelain'])
    
    @patch('tools.git_automation.run_command')
    def test_get_branch_name(self, mock_run):
        """Test getting branch name."""
        mock_run.return_value.stdout = "feature/test-branch\n"
        branch = get_branch_name()
        self.assertEqual(branch, "feature/test-branch")
        mock_run.assert_called_once_with(['git', 'branch', '--show-current'])
    
    def test_create_commit_message(self):
        """Test commit message creation."""
        # Test for test files
        files = ['tests/test_file.py']
        msg = create_commit_message(files, "Add test")
        self.assertIn("[Cursor] test:", msg)
        
        # Test for documentation
        files = ['README.md']
        msg = create_commit_message(files, "Update docs")
        self.assertIn("[Cursor] docs:", msg)
        
        # Test for feature
        files = ['tools/new_feature.py']
        msg = create_commit_message(files, "Add feature")
        self.assertIn("[Cursor] feat:", msg)
        
        # Test for chore
        files = ['random_file.txt']
        msg = create_commit_message(files, "Update file")
        self.assertIn("[Cursor] chore:", msg)
    
    @patch('tools.git_automation.get_changed_files')
    @patch('tools.git_automation.run_command')
    @patch('tempfile.NamedTemporaryFile')
    def test_commit_changes(self, mock_temp, mock_run, mock_get_files):
        """Test committing changes."""
        # Mock file operations
        mock_file = MagicMock()
        mock_temp.return_value.__enter__.return_value = mock_file
        mock_file.name = 'temp_commit_msg'
        
        # Mock changed files
        mock_get_files.return_value = ['file1.py', 'file2.py']
        
        # Test commit
        commit_changes("Test commit")
        
        # Verify git commands
        mock_run.assert_any_call(['git', 'add', 'file1.py', 'file2.py'])
        mock_run.assert_any_call(['git', 'commit', '-F', 'temp_commit_msg'])
    
    @patch('tools.git_automation.run_command')
    def test_create_pr(self, mock_run):
        """Test creating a pull request."""
        # Mock gh cli check
        mock_run.return_value = MagicMock()
        
        # Mock tempfile
        with patch('tempfile.NamedTemporaryFile') as mock_temp:
            mock_file = MagicMock()
            mock_temp.return_value.__enter__.return_value = mock_file
            mock_file.name = 'temp_pr_body'
            
            # Test PR creation
            create_pr("Test PR", "PR description")
            
            # Verify gh command
            mock_run.assert_any_call(['gh', '--version'])
            mock_run.assert_any_call([
                'gh', 'pr', 'create',
                '--title', '[Cursor] Test PR',
                '--body-file', 'temp_pr_body',
                '--base', 'main'
            ])
    
    @patch('tools.git_automation.run_command')
    def test_create_feature_branch(self, mock_run):
        """Test creating a feature branch."""
        create_feature_branch("New Feature")
        mock_run.assert_called_once_with(['git', 'checkout', '-b', 'feature/new-feature'])

if __name__ == '__main__':
    unittest.main() 
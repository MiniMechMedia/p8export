from BaseTest import BaseTest
from src.FileSystemOrchestrator import FileSystemOrchestrator
from os.path import exists
import os
import shutil
from pathlib import Path


class TestFileSystemOperations(BaseTest):
    orchestrationBaseDir: Path = BaseTest.getTempFolderPath() / "orch"

    # super - soldiers
    # ORCHESTRATION_TEST_FILE
    @classmethod
    def setUpClass(cls) -> None:
        os.makedirs(cls.orchestrationBaseDir, exist_ok=False)

    def setUp(self):
        self.currentTestFolder: Path = self.orchestrationBaseDir / self._testMethodName
        os.makedirs(self.currentTestFolder, exist_ok=False)

    def test_is_idempotent(self):

        pass

    def test_can_skip_both(self):

        pass

    # This will be pretty rare
    def test_can_rename_containing_folder_only(self):
        pass

    # This will be pretty rare
    def test_can_rename_p8_file_only(self):
        pass

    def test_can_rename_both_containing_folder_and_p8_file(self):
        pass

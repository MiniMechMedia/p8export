from BaseTest import BaseTest
from src.FileSystemOrchestrator import FileSystemOrchestrator
from os.path import exists
import os
import shutil
from pathlib import Path
from src.FileRegistry import TempFileEnum, TestFileEnum


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
        originalFolderInner: Path = self.currentTestFolder / "new-game-2"
        os.makedirs(originalFolderInner, exist_ok=False)
        copiedFile: Path = originalFolderInner / "somefile.p8"
        shutil.copy(
            self.getTestFilePath(TestFileEnum.ORCHESTRATION_TEST_FILE),
            copiedFile,
        )

        finalDir: Path = self.currentTestFolder / "super-soldiers"
        finalP8FileName = "super-soldiers.p8"
        FileSystemOrchestrator.prepareExportDir(copiedFile, finalP8FileName, finalDir)

        self.assertPathDoesNotExist(copiedFile)
        self.assertPathDoesNotExist(originalFolderInner)
        self.assertPathExists(finalDir)
        self.assertPathExists(finalDir / finalP8FileName)

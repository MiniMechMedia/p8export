from test.BaseTest import BaseTest
from src.FileSystemOrchestrator import FileSystemOrchestrator, FileSystemLocations
from os.path import samefile
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
        self.test_can_rename_both_containing_folder_and_p8_file()
        originalFile: Path = (
            self.currentTestFolder / "super-soldiers" / "super-soldiers.p8"
        )
        result: FileSystemLocations = FileSystemOrchestrator.prepareExportDir(
            originalFile, "super-soldiers.p8", self.currentTestFolder / "super-soldiers"
        )
        # TODO make sure no other folders/files exist... but that's fine
        self.assertPathExists(originalFile)
        self.assertTrue(originalFile == result.p8FilePath)

    def test_can_skip_both(self):
        originalFolderInner: Path = self.currentTestFolder / "super-soldiers"
        os.makedirs(originalFolderInner, exist_ok=False)
        copiedFile: Path = originalFolderInner / "super-soldiers.p8"
        shutil.copy(
            self.getTestFilePath(TestFileEnum.ORCHESTRATION_TEST_FILE),
            copiedFile,
        )

        finalDir: Path = self.currentTestFolder / "super-soldiers"
        finalP8FileName = "super-soldiers.p8"
        result: FileSystemLocations = FileSystemOrchestrator.prepareExportDir(
            copiedFile, finalP8FileName, finalDir
        )

        self.assertPathExists(finalDir)
        self.assertPathExists(finalDir / finalP8FileName)
        self.assertTrue(finalDir / finalP8FileName == result.p8FilePath)

    # This will be pretty rare
    def test_can_rename_containing_folder_only(self):
        originalFolderInner: Path = self.currentTestFolder / "new-game-2"
        os.makedirs(originalFolderInner, exist_ok=False)
        copiedFile: Path = originalFolderInner / "super-soldiers.p8"
        shutil.copy(
            self.getTestFilePath(TestFileEnum.ORCHESTRATION_TEST_FILE),
            copiedFile,
        )

        finalDir: Path = self.currentTestFolder / "super-soldiers"
        finalP8FileName = "super-soldiers.p8"
        result: FileSystemLocations = FileSystemOrchestrator.prepareExportDir(
            copiedFile, finalP8FileName, finalDir
        )

        self.assertPathDoesNotExist(copiedFile)
        self.assertPathDoesNotExist(originalFolderInner)

        self.assertPathExists(finalDir)
        self.assertPathExists(finalDir / finalP8FileName)

        self.assertTrue(finalDir / finalP8FileName == result.p8FilePath)

    # This will be pretty rare
    def test_can_rename_p8_file_only(self):
        originalFolderInner: Path = self.currentTestFolder / "super-soldiers"
        os.makedirs(originalFolderInner, exist_ok=False)
        copiedFile: Path = originalFolderInner / "somefile.p8"
        shutil.copy(
            self.getTestFilePath(TestFileEnum.ORCHESTRATION_TEST_FILE),
            copiedFile,
        )

        finalDir: Path = self.currentTestFolder / "super-soldiers"
        finalP8FileName = "super-soldiers.p8"
        result: FileSystemLocations = FileSystemOrchestrator.prepareExportDir(
            copiedFile, finalP8FileName, finalDir
        )

        self.assertPathDoesNotExist(copiedFile)

        self.assertPathExists(finalDir)
        self.assertPathExists(finalDir / finalP8FileName)

        self.assertTrue(finalDir / finalP8FileName == result.p8FilePath)

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
        result: FileSystemLocations = FileSystemOrchestrator.prepareExportDir(
            copiedFile, finalP8FileName, finalDir
        )

        self.assertPathDoesNotExist(copiedFile)
        self.assertPathDoesNotExist(originalFolderInner)
        self.assertPathExists(finalDir)
        self.assertPathExists(finalDir / finalP8FileName)

        self.assertTrue(finalDir / finalP8FileName == result.p8FilePath)

    def test_handles_initialized_folders(self):
        imagesFolder: Path = self.currentTestFolder / "images"
        exportFolder: Path = self.currentTestFolder / "export"
        os.makedirs(imagesFolder)
        os.makedirs(exportFolder)
        additionalImage: Path = imagesFolder / "someimage.png"
        existingCover: Path = imagesFolder / "cover.png"
        existingExportFile: Path = exportFolder / "blah.txt"
        with open(additionalImage, "w"):
            pass
        with open(existingCover, "w"):
            pass
        with open(existingExportFile, "w"):
            pass

        FileSystemOrchestrator.prepareSubfolders(self.currentTestFolder)

        self.assertPathExists(additionalImage)
        self.assertPathDoesNotExist(existingCover)
        self.assertPathExists(exportFolder)
        self.assertPathDoesNotExist(existingExportFile)

    def test_handles_uninitialized_folders(self):
        imagesFolder: Path = self.currentTestFolder / "images"
        exportFolder: Path = self.currentTestFolder / "export"

        self.assertPathDoesNotExist(imagesFolder)
        self.assertPathDoesNotExist(exportFolder)

        FileSystemOrchestrator.prepareSubfolders(self.currentTestFolder)

        self.assertPathExists(exportFolder)
        self.assertPathExists(exportFolder)

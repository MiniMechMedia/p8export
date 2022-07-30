from src.p8export import P8Export

# from TestFileSystemOperations import TestFileSystemOperations
from BaseTest import BaseTest, TempFileEnum, TestFileEnum
import os
import shutil
from pathlib import Path


class TestP8Export(BaseTest):
    p8exportBaseDir: Path = BaseTest.getTempFolderPath() / "p8export-test"

    # super - soldiers
    # ORCHESTRATION_TEST_FILE
    @classmethod
    def setUpClass(cls) -> None:
        os.makedirs(cls.p8exportBaseDir, exist_ok=False)

    def setUp(self):
        self.currentTestFolder: Path = self.p8exportBaseDir / self._testMethodName
        os.makedirs(self.currentTestFolder, exist_ok=False)

    def test_export_all_requires_some_files(self):
        pattern: str = str(self.currentTestFolder / "*.p8")
        with self.assertRaises(Exception):
            P8Export.exportDirectory(globPattern=pattern, uploadToItch=False)

    def test_export_all_cannot_handle_multiple_in_root_folder(self):
        pattern: str = str(self.currentTestFolder / '*.p8')
        shutil.copy(
            self.getTestFilePath(TestFileEnum.GAME_CART_TEST_FILE),
            self.currentTestFolder / 'game1.p8'
        )
        shutil.copy(
            self.getTestFilePath(TestFileEnum.GAME_CART_TEST_FILE),
            self.currentTestFolder / 'game2.p8'
        )
        with self.assertRaisesRegex(Exception, 'Multiple files found in same folder'):
            P8Export.exportDirectory(globPattern=pattern, uploadToItch=False)

    def test_export_all_cannot_handle_multiple_in_nested_folder(self):
        nestedFolder1: Path = self.currentTestFolder / 'nested1'
        nestedFolder2: Path = self.currentTestFolder / 'nested2'
        os.makedirs(nestedFolder1, exist_ok=False)
        os.makedirs(nestedFolder2, exist_ok=False)

        pattern: str = str(self.currentTestFolder / '*' / '*.p8')
        shutil.copy(
            self.getTestFilePath(TestFileEnum.GAME_CART_TEST_FILE),
            nestedFolder1 / 'game1.p8'
        )
        shutil.copy(
            self.getTestFilePath(TestFileEnum.GAME_CART_TEST_FILE),
            nestedFolder2 / 'game2.p8'
        )
        shutil.copy(
            self.getTestFilePath(TestFileEnum.GAME_CART_TEST_FILE),
            nestedFolder2 / 'game3.p8'
        )

        with self.assertRaisesRegex(Exception, 'Multiple files found in same folder'):
            P8Export.exportDirectory(globPattern=pattern, uploadToItch=False)

    def test_export_all_finds_all_files(self):
        nestedFolder1: Path = self.currentTestFolder / 'nested1'
        nestedFolder2: Path = self.currentTestFolder / 'nested2'
        os.makedirs(nestedFolder1, exist_ok=False)
        os.makedirs(nestedFolder2, exist_ok=False)

        pattern: str = str(self.currentTestFolder / '*' / '*.p8')
        shutil.copy(
            self.getTestFilePath(TestFileEnum.GAME_CART_TEST_FILE),
            nestedFolder1 / 'game1.p8'
        )
        shutil.copy(
            self.getTestFilePath(TestFileEnum.GAME_CART_TEST_FILE),
            nestedFolder2 / 'game2.p8'
        )

        count: int = P8Export.exportDirectory(globPattern=pattern, uploadToItch=False)
        self.assertEquals(count, 2)

    def test_folder_structure(self):
        templateDir: Path = self.currentTestFolder / "game-template"
        os.makedirs(templateDir)
        p8fileStart: Path = templateDir / "new-game.p8"
        shutil.copy(
            self.getTestFilePath(TestFileEnum.GAME_CART_TEST_FILE), p8fileStart
        )
        P8Export.export(p8fileStart, uploadToItch=False)

        expectedGameDir = self.currentTestFolder / "mongo-bongo"

        self.assertPathExists(expectedGameDir)
        self.assertPathExists(expectedGameDir / "images/")
        self.assertPathExists(expectedGameDir / "images" / "itch-cover.png")
        self.assertPathExists(expectedGameDir / "images" / "cover.png")
        self.assertPathExists(expectedGameDir / "export/")
        self.assertPathExists(expectedGameDir / "mongo-bongo.p8")
        self.assertPathExists(expectedGameDir / "export" / "html_export" / "index.html")
        self.assertPathExists(expectedGameDir / "export" / "html_export" / "index.js")
        self.assertPathExists(expectedGameDir / "export" / "html_export" / "index.zip")

        # TODO fix this
        # self.assertPathExists(expectedGameDir / "export" / "mongo-bongo.p8.png")

        self.assertPathExists(expectedGameDir / "README.md")
    #
    # def test_folder_structure(self):
    #     templateDir: Path = self.currentTestFolder / "game-template"
    #     os.makedirs(templateDir)
    #     p8fileStart: Path = templateDir / "new-game.p8"
    #     shutil.copy(
    #         self.getTestFilePath(TestFileEnum.BASIC_GAME_TEMPLATE_FILE), p8fileStart
    #     )
    #     P8Export.export(p8fileStart, uploadToItch=False)

    def test_optional_dir(self):
        pass

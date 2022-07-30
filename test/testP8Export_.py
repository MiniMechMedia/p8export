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

    # Note: A partial export will still happen, which isn't ideal
    def test_cannot_export_multiple_games_with_same_name(self):
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

        # with self.assertRaisesRegex(Exception, 'P8export error - Cannot perform a folder rename if folder already exists'):
        results = P8Export.exportDirectory(globPattern=pattern, uploadToItch=False)
        self.assertTrue(results.isError)
        self.assertTrue('P8export error - Cannot perform a folder rename if folder already exists' in results.formattedResults)

    def _copyWithChange(self, targetPath: Path, newGameName: str):
        shutil.copy(
            self.getTestFilePath(TestFileEnum.GAME_CART_TEST_FILE),
            targetPath
        )
        with open(targetPath) as file:
            contents = file.read()
            contents = contents.replace("Mongo Bongo", newGameName)
        with open(targetPath, 'w') as file:
            file.write(contents)


    def test_can_export_multiple_games(self):
        # self.currentTestFolder /= 'containing-folder'
        cartsFolder: Path = self.currentTestFolder / 'carts'
        nestedFolder1: Path = cartsFolder / 'nested1'
        nestedFolder2: Path = cartsFolder / 'nested2'
        os.makedirs(nestedFolder1, exist_ok=False)
        os.makedirs(nestedFolder2, exist_ok=False)

        # with open(self.currentTestFolder / 'README.md', 'w'):
        #     pass

        pattern: str = str(cartsFolder / '*' / '*.p8')
        self._copyWithChange(nestedFolder1 / 'game1.p8', 'Awesome Saucem')
        self._copyWithChange(nestedFolder2 / 'game2.p8', 'Doggo Froggo')

        results: dict[str,str] = P8Export.exportDirectory(globPattern=pattern, uploadToItch=False)
        self.assertEqual(len(results), 2)

        self.assertExportsAreAsExpected(cartsFolder, 'awesome-saucem')
        self.assertExportsAreAsExpected(cartsFolder, 'doggo-froggo')
        self.assertFileExists(TempFileEnum.MULTIPLE_EXPORT_README)


    # def test_can_handle_errors_in_export_all(self):
    #     raise NotImplemented

    def assertExportsAreAsExpected(self, containingFolder: Path, gameSlug: str):
        expectedGameDir: Path = containingFolder / gameSlug
        self.assertPathExists(expectedGameDir)
        self.assertPathExists(expectedGameDir / "images/")
        self.assertPathExists(expectedGameDir / "images" / "itch-cover.png")
        self.assertPathExists(expectedGameDir / "images" / "cover.png")
        self.assertPathExists(expectedGameDir / "export/")
        self.assertPathExists(expectedGameDir / f"{gameSlug}.p8")
        self.assertPathExists(expectedGameDir / "export" / "html_export" / "index.html")
        self.assertPathExists(expectedGameDir / "export" / "html_export" / "index.js")
        self.assertPathExists(expectedGameDir / "export" / "html_export" / "index.zip")

    def test_folder_structure(self):
        templateDir: Path = self.currentTestFolder / "game-template"
        os.makedirs(templateDir)
        p8fileStart: Path = templateDir / "new-game.p8"
        shutil.copy(
            self.getTestFilePath(TestFileEnum.GAME_CART_TEST_FILE), p8fileStart
        )
        P8Export.export(p8fileStart, uploadToItch=False)

        self.assertExportsAreAsExpected(self.currentTestFolder, 'mongo-bongo')

        # TODO fix this
        # self.assertPathExists(expectedGameDir / "export" / "mongo-bongo.p8.png")

        self.assertPathExists(self.currentTestFolder / 'mongo-bongo' / "README.md")

    def test_optional_dir(self):
        pass

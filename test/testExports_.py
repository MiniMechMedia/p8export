import unittest

from CompilationTargetBaseTest import CompilationTargetBaseTest
from src.FileRegistry import TestFileEnum, TemplateFileEnum, TempFileEnum
from src.pico8fileparser import Pico8FileParser
from src.ParsedContents import ParsedContents
from src.TemplateEvaluator import TemplateEvaluator
from src.HtmlFileCompilationTarget import HtmlFileCompilationTarget
from src.P8PngCompilationTarget import P8PngCompilationTarget


class TestExports(CompilationTargetBaseTest):
    def test_html_export(self):
        parsed: ParsedContents = self.parseTestFile(
            TestFileEnum.GAME_CART_TEST_FILE
        )
        HtmlFileCompilationTarget.compileToHtmlToDirectory(
            parsed.filePath,
            parsed.config,  # self.getTempFilePath(TempFileEnum.LABEL_IMAGE_TEMP_FILE)
            self.getTempFilePath(TempFileEnum.HTML_EXPORT_TEMP_DIR),
        )
        self.assertFileExists(TempFileEnum.HTML_EXPORT_TEMP_FILE_HTML)
        self.assertFileExists(TempFileEnum.HTML_EXPORT_TEMP_FILE_JS)
        self.assertFileExists(TempFileEnum.HTML_EXPORT_TEMP_FILE_ZIP)

    # @unittest.skip("TODO fix this")
    def test_p8png_export(self):
        parsed: ParsedContents = self.parseTestFile(
            TestFileEnum.GAME_CART_TEST_FILE
        )
        P8PngCompilationTarget.compileToP8PngToDirectory(
            config=parsed.config,
            p8InputPath=parsed.filePath,
            p8PngOutputPath=self.getTempFolderPath()
            / (parsed.metadata.correctedGameSlug + ".p8.png"),
        )
        self.assertFileExists(TempFileEnum.P8_PNG_EXPORT_TEMP_FILE)

    @unittest.skip
    def test_aggregate_readme_is_idempotent(self):
        pass

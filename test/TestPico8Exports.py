from CompilationTargetBaseTest import CompilationTargetBaseTest
from src.FileRegistry import TestFileEnum, TemplateFileEnum, TempFileEnum
from src.pico8fileparser import Pico8FileParser
from src.ParsedContents import ParsedContents
from src.TemplateEvaluator import TemplateEvaluator
from src.HtmlFileCompilationTarget import HtmlFileCompilationTarget
from src.P8PngCompilationTarget import P8PngCompilationTarget


class TestPico8Exports(CompilationTargetBaseTest):
    def test_html_export(self):
        parsed: ParsedContents = self.parseTestFile(
            TestFileEnum.BASIC_GAME_TEMPLATE_FILE
        )
        HtmlFileCompilationTarget.compileToHtmlToDirectory(
            parsed,  # self.getTempFilePath(TempFileEnum.LABEL_IMAGE_TEMP_FILE)
            self.getTempFolderPath(),
        )
        self.assertFileExists(TempFileEnum.HTML_EXPORT_TEMP_FILE_HTML)
        self.assertFileExists(TempFileEnum.HTML_EXPORT_TEMP_FILE_JS)

    def test_p8png_export(self):
        parsed: ParsedContents = self.parseTestFile(
            TestFileEnum.BASIC_GAME_TEMPLATE_FILE
        )
        P8PngCompilationTarget.compileToP8PngToDirectory(
            parsed,
            self.getTempFolderPath(),  # self.getTempFilePath(TempFileEnum.P8_PNG_EXPORT_TEMP_FILE)
        )
        self.assertFileExists(TempFileEnum.P8_PNG_EXPORT_TEMP_FILE)

from CompilationTargetBaseTest import CompilationTargetBaseTest
from src.FileRegistry import TestFileEnum, TemplateFileEnum, TempFileEnum
from src.pico8fileparser import Pico8FileParser
from src.ParsedContents import ParsedContents
from src.TemplateEvaluator import TemplateEvaluator
from src.HtmlFileCompilationTarget import HtmlFileCompilationTarget


class TestHtmlExport(CompilationTargetBaseTest):
    def test_html_export(self):
        parsed: ParsedContents = self.parseTestFile(
            TestFileEnum.BASIC_GAME_TEMPLATE_FILE
        )
        HtmlFileCompilationTarget.compileToHtml(parsed)

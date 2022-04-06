# Does the submission.html
from ParsedContents import ParsedContents
from CompilationTarget import CompilationTarget
from pathlib import Path


class HtmlFileCompilationTarget(CompilationTarget):
    # Returns html, js file
    def compileToHtml(self) -> tuple[str, str]:
        pass

    def compileToHtmlToDirectory(self, outputDir: Path):
        pass

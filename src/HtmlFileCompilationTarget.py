# Does the submission.html
from ParsedContents import ParsedContents
from CompilationTarget import CompilationTarget
from pathlib import Path
import os


class HtmlFileCompilationTarget(CompilationTarget):
    # Returns html, js file
    def compileToHtml(self, parsedContents: ParsedContents) -> tuple[str, str]:
        os.system(
            f"{parsedContents.config.pico8ExePath} -export index.html {parsedContents.filePath}"
        )

        return "", ""

    def compileToHtmlToDirectory(self, outputDir: Path):
        pass

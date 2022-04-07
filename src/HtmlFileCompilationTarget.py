# Does the submission.html
from src.ParsedContents import ParsedContents
from src.CompilationTarget import CompilationTarget
from pathlib import Path

# import os
import subprocess
import tempfile


class HtmlFileCompilationTarget(CompilationTarget):
    # # Returns html, js file
    # @classmethod
    # def compileToHtml(cls, parsedContents: ParsedContents) -> tuple[str, str]:
    #     with tempfile.TemporaryDirectory() as tempDir:
    #         args: list[str] = [
    #             parsedContents.config.pico8ExePath,
    #             "-export",
    #             f"{tempDir}/index.html",
    #             str(parsedContents.filePath),
    #         ]
    #         # subprocess.call(r"C:\Program Files (x86)\PICO-8\pico8.exe")
    #         subprocess.run(args, check=True)
    #         x = 10
    #     # os.system(
    #     #     f"{parsedContents.config.pico8ExePath} -export index.html {parsedContents.filePath}"
    #     # )
    #
    #     return "", ""

    @classmethod
    def compileToHtmlToDirectory(
        cls, parsedContents: ParsedContents, outputDir: Path
    ) -> None:
        args: list[str] = [
            parsedContents.config.pico8ExePath,
            "-export",
            str(outputDir / "index.html"),
            str(parsedContents.filePath),
        ]
        # subprocess.call(r"C:\Program Files (x86)\PICO-8\pico8.exe")
        subprocess.run(args, check=True)

# Does the submission.html
from src.ParsedContents import ParsedContents
from src.CompilationTarget import CompilationTarget
from pathlib import Path
import shutil

# import os
import subprocess
import tempfile
from os.path import exists
import os


class HtmlFileCompilationTarget(CompilationTarget):
    @classmethod
    def compileToHtmlToDirectory(
        cls, parsedContents: ParsedContents, outputDir: Path
    ) -> None:
        os.makedirs(outputDir, exist_ok=True)

        args: list[str] = [
            parsedContents.config.pico8ExePath,
            "-export",
            str(outputDir / "index.html"),
            str(parsedContents.filePath),
        ]
        # subprocess.call(r"C:\Program Files (x86)\PICO-8\pico8.exe")
        subprocess.run(args, check=True)
        # Since pico8.exe doesn't tell you it failed, we need to check!
        if not exists(outputDir / "index.html") or not exists(outputDir / "index.js"):
            raise Exception("HTML export failed")

        shutil.make_archive(str(outputDir / "index"), "zip", outputDir)

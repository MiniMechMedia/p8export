# Does the submission.html
from src.ParsedContents import Config
from src.CompilationTarget import CompilationTarget
from pathlib import Path
import shutil

# import os
import subprocess
import tempfile
from os.path import exists
import os


class HtmlFileCompilationTarget(CompilationTarget):
    # Results in 3 files:
    # outputDir / 'index.html'
    # outputDir / 'index.js'
    # outputDir / 'index.zip'
    # Returns path of index.zip
    # TODO I feel like every compilation target should receive Config automatically?
    @classmethod
    def compileToHtmlToDirectory(
        cls, p8filePath: Path, config: Config, outputDir: Path
    ) -> Path:
        os.makedirs(outputDir, exist_ok=True)

        args: list[str] = [
            config.pico8ExePath,
            "-export",
            str(outputDir / "index.html"),
            str(p8filePath),
        ]
        # subprocess.call(r"C:\Program Files (x86)\PICO-8\pico8.exe")
        subprocess.run(args, check=True)
        # Since pico8.exe doesn't tell you it failed, we need to check!
        if not exists(outputDir / "index.html") or not exists(outputDir / "index.js"):
            raise Exception("HTML export failed")

        shutil.make_archive("index", "zip", outputDir)
        shutil.move("index.zip", outputDir / "index.zip")

        return outputDir / "index.zip"

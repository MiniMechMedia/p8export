from src.ParsedContents import ParsedContents
from src.CompilationTarget import CompilationTarget
from pathlib import Path
import subprocess


class P8PngCompilationTarget(CompilationTarget):
    @classmethod
    def compileToP8PngToDirectory(cls, parsedContents: ParsedContents, outputDir: Path):

        args: list[str] = [
            parsedContents.config.pico8ExePath,
            "-export",
            outputDir / (parsedContents.metadata.correctedGameSlug + ".p8.png"),
            str(parsedContents.filePath),
        ]
        # subprocess.call(r"C:\Program Files (x86)\PICO-8\pico8.exe")
        subprocess.run(args, check=True)
        x = 10

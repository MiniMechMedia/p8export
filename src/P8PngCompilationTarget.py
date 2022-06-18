from src.ParsedContents import Config
from src.CompilationTarget import CompilationTarget
from pathlib import Path
import subprocess


class P8PngCompilationTarget(CompilationTarget):
    @classmethod
    def compileToP8PngToDirectory(
        cls, config: Config, p8InputPath: Path, p8PngOutputPath: Path
    ):
        args: list[str] = [
            config.pico8ExePath,
            str(p8InputPath.absolute().resolve()),
            "-export",
            str(p8PngOutputPath.absolute()),
        ]
        argsconcat = ' '.join(args)
        # print(' '.join(args))
        # subprocess.call(r"C:\Program Files (x86)\PICO-8\pico8.exe")
        subprocess.run(args, check=True)
        if not p8PngOutputPath.exists():
            raise Exception("PICO-8 png export failed")

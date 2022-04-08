from os.path import samefile, basename, exists
import os
import shutil
from pathlib import Path


class FileSystemOrchestrator:
    # returns the new path of the input p8 file. This will always be exportDir / finalP8FileName
    @classmethod
    def prepareExportDir(
        cls, inputP8FilePath: Path, finalP8FileName: str, exportDir: Path
    ) -> Path:

        containingDir: Path = inputP8FilePath / ".."

        if basename(inputP8FilePath) != finalP8FileName:
            os.rename(inputP8FilePath, finalP8FileName)

        if not samefile(containingDir, exportDir):
            if exists(exportDir):
                raise Exception(
                    "P8export error - Cannot perform a folder rename if folder already exists"
                )
            shutil.move(containingDir, exportDir)

        return exportDir / finalP8FileName

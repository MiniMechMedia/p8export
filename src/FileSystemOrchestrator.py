from os.path import samefile, basename, exists
import os
import shutil
from pathlib import Path
from dataclasses import dataclass


@dataclass
class FileSystemLocations:
    exportsBaseDir: Path
    screenshotsDir: Path
    exportsSubDir: Path
    coverPath: Path
    itchCoverPath: Path


class FileSystemOrchestrator:
    @classmethod
    def prepareSubfolders(cls, exportsBaseDir: Path) -> FileSystemLocations:
        shutil.rmtree(exportsBaseDir / "export", ignore_errors=True)

        screenshotsDir: Path = exportsBaseDir / "images"
        coverPath: Path = screenshotsDir / "cover.png"
        itchCoverPath: Path = screenshotsDir / "itch-cover.png"

        if exists(screenshotsDir):
            try:
                os.remove(screenshotsDir / "cover.png")
            except OSError:
                pass

            try:
                os.remove(screenshotsDir / "itch-cover.png")
            except OSError:
                pass
        else:
            os.makedirs(screenshotsDir)
        # TODO rename this
        exportsSubDir: Path = exportsBaseDir / "export"
        try:
            shutil.rmtree(exportsSubDir)
        except FileNotFoundError:
            pass
        os.makedirs(exportsSubDir)

        return FileSystemLocations(
            exportsBaseDir=exportsBaseDir,
            screenshotsDir=screenshotsDir,
            exportsSubDir=exportsSubDir,
            coverPath=coverPath,
            itchCoverPath=itchCoverPath,
        )

    # returns the new path of the input p8 file. This will always be exportDir / finalP8FileName
    @classmethod
    def prepareExportDir(
        cls, inputP8FilePath: Path, finalP8FileName: str, exportDir: Path
    ) -> Path:

        containingDir: Path = inputP8FilePath.parent

        if basename(inputP8FilePath) != finalP8FileName:
            os.rename(inputP8FilePath, containingDir / finalP8FileName)

        if exists(exportDir):
            if not samefile(containingDir, exportDir):
                raise Exception(
                    "P8export error - Cannot perform a folder rename if folder already exists"
                )
        else:
            shutil.move(containingDir, exportDir)

        return exportDir / finalP8FileName

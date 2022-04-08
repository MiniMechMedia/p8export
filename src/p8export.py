from pathlib import Path
import sys
from src.ParsedContents import ParsedContents
from os.path import exists
from src.pico8fileparser import Pico8FileParser
from src.FileSystemOrchestrator import FileSystemOrchestrator, FileSystemLocations
from typing import Optional

from src.HtmlFileCompilationTarget import HtmlFileCompilationTarget

# from src.P8PngCompilationTarget import P8PngCompilationTarget
from src.ImagesCompilationTarget import ImagesCompilationTarget

# from src.ItchDescriptionCompilationTarget import ItchDescriptionCompilationTarget


class P8Export:
    # Be warned: will use the directory the p8 file is currently in as the export dir

    @classmethod
    def export(cls, targetFile: Path, targetExportDir: Optional[Path] = None):
        if targetExportDir is not None:
            raise NotImplemented("this feature is not yet available")
        if not exists(targetFile):
            raise Exception("invalid target")

        parsedContents: ParsedContents = Pico8FileParser.parse(targetFile)

        # TODO validate??

        slug: str = parsedContents.metadata.correctedGameSlug
        targetDir: Path = (
            targetExportDir or parsedContents.filePath.parent.parent / slug
        )

        locations: FileSystemLocations = FileSystemOrchestrator.prepareExportDir(
            parsedContents.filePath, f"{slug}.p8", targetDir
        )

        # TODO remove need to overwrite this
        # parsedContents.filePath = locations.p8FilePath

        ImagesCompilationTarget.writeCoverImage(
            parsedImage=parsedContents.labelImage, outputPath=locations.itchCoverPath
        )
        ImagesCompilationTarget.writeLabelImage(
            parsedImage=parsedContents.labelImage, outputPath=locations.coverPath
        )
        HtmlFileCompilationTarget.compileToHtmlToDirectory(
            p8filePath=locations.p8FilePath,
            config=parsedContents.config,
            outputDir=locations.htmlExportDir,
        )
        # FileSystemOrchestrator.prepareSubfolders()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise Exception("must provide target")
    P8Export.export(Path(sys.argv[1]))

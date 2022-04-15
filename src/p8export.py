from pathlib import Path
import sys
from src.ParsedContents import ParsedContents
from os.path import exists
from src.pico8fileparser import Pico8FileParser
from src.FileSystemOrchestrator import FileSystemOrchestrator, FileSystemLocations
from typing import Optional

from src.HtmlFileCompilationTarget import HtmlFileCompilationTarget

from src.P8PngCompilationTarget import P8PngCompilationTarget
from src.ImagesCompilationTarget import ImagesCompilationTarget
from src.ReadmeCompilationTarget import ReadmeCompilationTarget
from src.ItchGameCompilationTarget import ItchGameCompilationTarget

# from src.ItchDescriptionCompilationTarget import ItchDescriptionCompilationTarget


class P8Export:
    # Be warned: will use the directory the p8 file is currently in as the export dir

    @classmethod
    def export(
        cls,
        targetFile: Path,
        uploadToItch: bool,
        targetExportDir: Optional[Path] = None,
    ):
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

        parsedContents.coverPath = "images/cover.png"
        parsedContents.folderRelativePath = (
            f"carts/{parsedContents.metadata.correctedGameSlug}"
        )
        parsedContents.coverPathAbs = (
            f"{parsedContents.folderRelativePath}/images/cover.png"
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
            config=parsedContents.config,
            p8filePath=locations.p8FilePath,
            outputDir=locations.htmlExportDir,
        )
        P8PngCompilationTarget.compileToP8PngToDirectory(
            config=parsedContents.config,
            p8InputPath=locations.p8FilePath,
            p8PngOutputPath=locations.exportsSubDir
            / (parsedContents.metadata.correctedGameSlug + ".p8.png"),
        )
        ReadmeCompilationTarget.createIndividualReadme(
            parsedContents=parsedContents,
            readmeOutputPath=locations.exportsBaseDir / "README.md",
        )

        # TODO don't like inferring the location of the aggregate readme
        ReadmeCompilationTarget.addToAggregateReadme(
            parsedContents=parsedContents,
            readmeOutputPath=targetDir.parent.parent / "README.md",
        )
        if uploadToItch:
            ItchGameCompilationTarget.uploadToItch(parsedContents, locations.exportsBaseDir)
        # parsedContents=parsedContents,
        #                                              outputDir=locations.exportsSubDir / parsedContents.)
        # FileSystemOrchestrator.prepareSubfolders()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise Exception("must provide target")
    P8Export.export(Path(sys.argv[1]), uploadToItch=True)

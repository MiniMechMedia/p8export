from dataclasses import dataclass
from pathlib import Path
import sys
from src.ParsedContents import ParsedContents
from os.path import exists
from src.pico8fileparser import Pico8FileParser
from src.FileSystemOrchestrator import FileSystemOrchestrator, FileSystemLocations
from typing import Optional
import glob
import traceback

from src.HtmlFileCompilationTarget import HtmlFileCompilationTarget

from src.P8PngCompilationTarget import P8PngCompilationTarget
from src.ImagesCompilationTarget import ImagesCompilationTarget
from src.ReadmeCompilationTarget import ReadmeCompilationTarget
from src.ItchGameCompilationTarget import ItchGameCompilationTarget
from src.XmlCompilationTarget import XmlCompilationTarget
from src.P8FileTransformerCompilationTarget import P8FileTransformerCompilationTarget


# from src.ItchDescriptionCompilationTarget import ItchDescriptionCompilationTarget
@dataclass
class ExportResults:
    resultMap: dict[str, str]

    SUCCESSINDICATOR = "success"

    @property
    def isError(self):
        return self.errorCount > 0

    @property
    def formattedResults(self):
        summary = ""
        for path, result in self.resultMap.items():
            slug = path.split("/")[-1].split(".")[0].ljust(40)
            summary += f"{slug}: {result}\n"

        # summary = '\n'.join(f'{game}: {result}' for game, result in self.resultMap.items())
        return f"Errors encountered ({self.errorCount} out of {len(self)}):\n{summary}\nErrors encountered ({self.errorCount} out of {len(self)})"

    @property
    def errorCount(self):
        return len(self.resultMap) - self.successCount

    @property
    def successCount(self):
        return len(
            [
                result
                for result in self.resultMap.values()
                if result == self.SUCCESSINDICATOR
            ]
        )

    def __len__(self):
        return len(self.resultMap)


class P8Export:
    # Be warned: will use the directory the p8 file is currently in as the export dir

    @classmethod
    def exportDirectory(cls, globPattern: str, uploadToItch: bool) -> ExportResults:
        if not globPattern.endswith(".p8"):
            raise Exception("must target .p8 files")
        allFiles = glob.glob(globPattern)

        # # DEBUGG!!!
        # with open('/Users/nathandunn/Projects/p8export3/p8export-fresh/tmp/info.txt') as file:
        #     targetFile = file.read().strip()
        # for file in allFiles[:]:
        #     if file != targetFile:
        #         allFiles.remove(file)
        # # DEBUGG!!!

        if not allFiles:
            raise Exception("No files found")

        allRoots = [Path(absPath).resolve().parent for absPath in allFiles]
        if len(allRoots) != len(set(allRoots)):
            # TODO might want to support this?
            raise Exception("Multiple files found in same folder")

        resultMap: dict[str, str] = {}
        for file in allFiles:
            try:
                cls.export(targetFile=Path(file), uploadToItch=uploadToItch)
            except Exception as e:
                stack = traceback.format_exc()
                resultMap[file] = f"{e.__class__}{e}{stack}"
            else:
                resultMap[file] = ExportResults.SUCCESSINDICATOR

        return ExportResults(resultMap)

    # TODO return the resulting files
    @classmethod
    def export(
        cls,
        targetFile: Path,
        uploadToItch: bool,
        targetExportDir: Optional[Path] = None,
    ) -> None:
        if targetExportDir is not None:
            raise NotImplemented("this feature is not yet available")
        if not str(targetFile).endswith(".p8"):
            raise Exception("Must target .p8 file")
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

        # finalP8FileName
        P8FileTransformerCompilationTarget.transformP8File(
            p8FilePath=locations.p8FilePath, parsed=parsedContents
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

        XmlCompilationTarget.compileToXml(
            xmlDestination=locations.exportsSubDir / "game.xml",
            metadata=parsedContents.metadata,
        )

        if uploadToItch and True:
            ItchGameCompilationTarget.uploadToItch(
                parsedContents, locations.exportsBaseDir
            )
        # parsedContents=parsedContents,
        #                                              outputDir=locations.exportsSubDir / parsedContents.)
        # FileSystemOrchestrator.prepareSubfolders()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise Exception("must provide target")
    # TODO arg parsing
    uploadToItch = True
    if len(sys.argv) > 2 and sys.argv[2] == "--no-itch":
        uploadToItch = False
    target: str = sys.argv[1]
    if "*" in target:
        results = P8Export.exportDirectory(target, uploadToItch=uploadToItch)
        if results.isError:
            raise Exception(results.formattedResults)
    else:
        P8Export.export(Path(target), uploadToItch=uploadToItch)

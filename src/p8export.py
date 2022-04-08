from pathlib import Path
import sys
from ParsedContents import ParsedContents
from os.path import exists
from pico8fileparser import Pico8FileParser
from FileSystemOrchestrator import FileSystemOrchestrator, FileSystemLocations


class P8Export:
    # Be warned: will use the directory the p8 file is currently in as the export dir
    @classmethod
    def export(cls, targetFile: Path):
        if not exists(targetFile):
            raise Exception("invalid target")

        parsedContents: ParsedContents = Pico8FileParser.parse(targetFile)
        slug: str = parsedContents.metadata.correctedGameSlug
        targetDir: Path = parsedContents.filePath / ".." / ".." / slug

        locations: FileSystemLocations = FileSystemOrchestrator.prepareExportDir(
            parsedContents.filePath, f"{slug}.p8", targetDir
        )

        # FileSystemOrchestrator.prepareSubfolders()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise Exception("must provide target")
    P8Export.export(Path(sys.argv[1]))

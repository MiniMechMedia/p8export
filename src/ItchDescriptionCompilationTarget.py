# Does the submission.html
from ParsedContents import ParsedContents
from CompilationTarget import CompilationTarget
from pathlib import Path


class ItchDescriptionCompilationTarget(CompilationTarget):
    @classmethod
    def compileDescription(cls, data: object) -> str:
        pass

    @classmethod
    # I suppose this is where the Itch API would come in...butler and such??
    def compileDescriptionToFile(cls, data: object, outputFile: Path) -> None:
        contents = cls.compileDescription(data)
        with open(outputFile, "w") as file:
            file.write(contents)

# Does the submission.html
from src.ParsedContents import ParsedContents
from src.CompilationTarget import CompilationTarget
from pathlib import Path

# import selenium
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options


class ItchGameCompilationTarget(CompilationTarget):
    @classmethod
    def uploadToItch(cls, parsedContents: ParsedContents):
        # selenium.
        browser: Chrome = Chrome()
        browser.get("https://itch.io")

    pass
    # @classmethod
    # def compileDescription(cls, data: object) -> str:
    #     pass
    #
    # @classmethod
    # # I suppose this is where the Itch API would come in...butler and such??
    # def compileDescriptionToFile(cls, data: object, outputFile: Path) -> None:
    #     contents = cls.compileDescription(data)
    #     with open(outputFile, "w") as file:
    #         file.write(contents)

import pathlib
import yaml


class Pico8FileParser:
    # def __init__(self):
    #     pass
    # self.rawContents = None

    @staticmethod
    def parse(filepath: pathlib.Path) -> "ParsedContents":
        return ParsedContents(filepath)

    @staticmethod
    def parseRawFileContents(filepath: pathlib.Path) -> str:
        with open(filepath) as file:
            return file.read()

    @staticmethod
    def parseRawYamlFromFileContents(rawFileContents: str) -> str:
        rawYaml: str = rawFileContents.split("--[[")[1]
        rawYaml = rawYaml.split("--]]")[0]
        return rawYaml.strip()

    @staticmethod
    def parseYamlFromRawYaml(rawYaml: str) -> None:
        return yaml.safe_load(rawYaml)


class ParsedContents:
    def __init__(self, filePath: pathlib.Path):
        self.rawContents: str = Pico8FileParser.parseRawFileContents(filePath)
        self.rawYaml: str = Pico8FileParser.parseRawYamlFromFileContents(
            rawFileContents=self.rawContents
        )
        self.parsedYaml = Pico8FileParser.parseYamlFromRawYaml(self.rawYaml)

    def getRawYaml(self) -> str:
        return self.rawYaml

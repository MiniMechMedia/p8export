import pathlib
import yaml
import typing


class Pico8FileParser:
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
    def parseYamlFromRawYaml(rawYaml: str) -> dict:
        ret: typing.Any = yaml.safe_load(rawYaml)
        if type(ret) is not dict:
            raise Exception("could not parse to a dict")
        return ret

    @staticmethod
    def parseRawLabelImage(rawContents) -> str:
        if "__label__" not in rawContents:
            raise Exception("Capture label image first")

        rawLabelImage: str = rawContents.split("__label__")[1]
        rawLabelImage = rawLabelImage.split("__")[0]
        return rawLabelImage.strip()


class ParsedContents:
    def __init__(self, filePath: pathlib.Path):
        self.rawContents: str = Pico8FileParser.parseRawFileContents(filePath)
        self.rawYaml: str = Pico8FileParser.parseRawYamlFromFileContents(
            rawFileContents=self.rawContents
        )
        self.parsedYaml = Pico8FileParser.parseYamlFromRawYaml(self.rawYaml)
        self.rawLabelImage = Pico8FileParser.parseRawLabelImage(self.rawContents)

    def getRawYaml(self) -> str:
        return self.rawYaml

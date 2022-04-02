import pathlib
import yaml
import typing


class ParsedLabelImage:
    def __init__(self, data: list[list[int]]):
        self.data = data

    def __getitem__(self, xy) -> int:
        x: int = xy[0]
        y: int = xy[1]
        return self.data[y][x]

    @property
    def width(self) -> int:
        return len(self.data[0])

    @property
    def height(self) -> int:
        return len(self.data)

    # def padData(self, hori):
    #     ret: list[list[int]] = []
    #     for row in self.data:
    #         ret.append(row)


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
    def parseRawLabelImage(rawContents: str) -> str:
        if "__label__" not in rawContents:
            raise Exception("Capture label image first")

        rawLabelImage: str = rawContents.split("__label__")[1]
        rawLabelImage = rawLabelImage.split("__")[0]
        return rawLabelImage.strip()

    @staticmethod
    def parseImageLabel(rawLabelImage: str) -> ParsedLabelImage:
        ret: list[list[int]] = []
        for row in rawLabelImage.split():
            rowList: list[int] = []
            for pixel in row.upper():
                pico8ColorIndex: int = "0123456789ABCDEFGHIJKLMNOPQRSTUV".index(pixel)
                rowList.append(pico8ColorIndex)

            ret.append(rowList)
        return ParsedLabelImage(ret)


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

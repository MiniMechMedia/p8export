import pathlib
import yaml
import typing
from .ParsedContents import ParsedContents, ParsedLabelImage, MetaData, ControlEnum
from dacite import from_dict, Config


class Pico8FileParser:
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

    @staticmethod
    def parseMetadata(rawMetadata: dict) -> MetaData:
        # TODO be tolerant of old file formats i.e. dict missing entries
        return from_dict(
            data_class=MetaData, data=rawMetadata, config=Config(cast=[ControlEnum])
        )

    @classmethod
    def parse(
        cls: typing.Type["Pico8FileParser"], filePath: pathlib.Path
    ) -> ParsedContents:
        ret: ParsedContents = ParsedContents()
        ret.rawContents = cls.parseRawFileContents(filePath)
        ret.rawYaml = cls.parseRawYamlFromFileContents(ret.rawContents)
        ret.parsedYaml = cls.parseYamlFromRawYaml(ret.rawYaml)
        ret.rawLabelImage = cls.parseRawLabelImage(ret.rawContents)
        ret.metadata = cls.parseMetadata(ret.parsedYaml)

        return ret

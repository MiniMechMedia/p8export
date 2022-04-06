import pathlib
import yaml
import typing
from .ParsedContents import ParsedContents, ParsedLabelImage, MetaData, ControlEnum
from dacite import from_dict, Config


class Pico8FileParser:
    @classmethod
    def parseRawFileContents(cls, filepath: pathlib.Path) -> str:
        with open(filepath) as file:
            return file.read()

    @classmethod
    def parseRawYamlFromFileContents(cls, rawFileContents: str) -> str:
        rawYaml: str = rawFileContents.split("--[[")[1]
        rawYaml = rawYaml.split("--]]")[0]
        return rawYaml.strip()

    @classmethod
    def parseSourceCodeFromFileContents(cls, rawFileContents: str) -> str:
        rawSourceCode: str = rawFileContents.split("--]]")[1]
        rawSourceCode = rawSourceCode.split("__gfx__")[0]
        return rawSourceCode.strip()

    @classmethod
    def parseYamlFromRawYaml(cls, rawYaml: str) -> dict:
        ret: typing.Any = yaml.safe_load(rawYaml)
        if type(ret) is not dict:
            raise Exception("could not parse to a dict")
        return ret

    @classmethod
    def parseRawLabelImage(cls, rawContents: str) -> str:
        if "__label__" not in rawContents:
            raise Exception("Capture label image first")

        rawLabelImage: str = rawContents.split("__label__")[1]
        rawLabelImage = rawLabelImage.split("__")[0]
        return rawLabelImage.strip()

    @classmethod
    def parseImageLabel(cls, rawLabelImage: str) -> ParsedLabelImage:
        ret: list[list[int]] = []
        for row in rawLabelImage.split():
            rowList: list[int] = []
            for pixel in row.upper():
                pico8ColorIndex: int = "0123456789ABCDEFGHIJKLMNOPQRSTUV".index(pixel)
                rowList.append(pico8ColorIndex)

            ret.append(rowList)
        return ParsedLabelImage(ret)

    @classmethod
    def parseMetadata(cls, rawMetadata: dict) -> MetaData:
        # TODO be tolerant of old file formats i.e. dict missing entries
        return from_dict(
            data_class=MetaData, data=rawMetadata, config=Config(cast=[ControlEnum])
        )

    @classmethod
    def parse(cls, filePath: pathlib.Path) -> ParsedContents:
        # ret: ParsedContents = ParsedContents()
        rawContents: str = cls.parseRawFileContents(filePath)
        sourceCode: str = cls.parseSourceCodeFromFileContents(rawContents)
        rawYaml: str = cls.parseRawYamlFromFileContents(rawContents)
        parsedYaml: dict = cls.parseYamlFromRawYaml(rawYaml)
        rawLabelImage: str = cls.parseRawLabelImage(rawContents)
        metadata: MetaData = cls.parseMetadata(parsedYaml)

        return ParsedContents(
            rawContents=rawContents,
            sourceCode=sourceCode,
            rawLabelImage=rawLabelImage,
            metadata=metadata,
        )

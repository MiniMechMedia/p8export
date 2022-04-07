import pathlib
import yaml
import typing
from .ParsedContents import (
    ParsedContents,
    ParsedLabelImage,
    Metadata,
    ControlEnum,
    Config,
)
from dacite import from_dict, Config as daciteConfig


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
    def parseMetadata(cls, rawMetadata: dict) -> Metadata:
        # TODO be tolerant of old file formats i.e. dict missing entries
        ret: Metadata = from_dict(
            data_class=Metadata,
            data=rawMetadata,
            config=daciteConfig(cast=[ControlEnum]),
        )

        return ret

    # @classmethod
    # def deriveGameSlug(cls, game_name: str):
    #     return slugify(game_name)
    #     # TODO use the package
    # return str.replace(" ", "_").lower()

    # TODO populate this stuff from a config file? Or cmdline args or something?
    @classmethod
    def getConfig(cls) -> Config:
        return Config(
            gameAuthor="Caterpillar Games",
            itchAuthor="caterpillargames",
            sourceControlRootUrl="https://github.com/CaterpillarGames/pico8-games/tree/master/carts",
            pico8ExePath=r"C:\Program Files (x86)\PICO-8\pico8.exe",
            pico8WorkingDir="",
        )

    @classmethod
    def parse(cls, filePath: pathlib.Path) -> ParsedContents:
        rawContents: str = cls.parseRawFileContents(filePath)
        sourceCode: str = cls.parseSourceCodeFromFileContents(rawContents)
        rawYaml: str = cls.parseRawYamlFromFileContents(rawContents)
        parsedYaml: dict = cls.parseYamlFromRawYaml(rawYaml)
        rawLabelImage: str = cls.parseRawLabelImage(rawContents)
        metadata: Metadata = cls.parseMetadata(parsedYaml)
        config: Config = cls.getConfig()
        return ParsedContents(
            filePath=filePath,
            rawContents=rawContents,
            sourceCode=sourceCode,
            rawLabelImage=rawLabelImage,
            metadata=metadata,
            config=config,
        )

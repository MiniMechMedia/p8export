import pathlib
import yaml
import typing
from src.ParsedContents import (
    ParsedContents,
    ParsedLabelImage,
    Metadata,
    ControlEnum,
    Config,
)
from dacite import from_dict, Config as daciteConfig
from decouple import config
import re
from src.Pico8EduUrlCompliationTarget import Pico8EduUrlCompilationTarget

class Pico8FileParser:
    @classmethod
    def parseRawFileContents(cls, filepath: pathlib.Path) -> str:
        with open(filepath) as file:
            return file.read()

    @classmethod
    def parseRawYamlFromFileContents(cls, rawFileContents: str) -> str:
        if "__meta:cart_info_start__" not in rawFileContents:
            raise Exception("Need __meta:cart_info_start__. Is this an old format?")
        rawYaml: str = rawFileContents.split("__meta:cart_info_start__")[1]
        rawYaml = rawYaml.split("__meta:cart_info_end__")[0]
        return rawYaml.strip()

    @classmethod
    def parseSourceCodeFromFileContents(cls, rawFileContents: str) -> str:
        rawSourceCode: str = rawFileContents.split("__lua__")[1]

        # One of these will be first...
        rawSourceCode = rawSourceCode.split("__gfx__")[0]
        rawSourceCode = rawSourceCode.split("__label__")[0]

        rawSourceCode = rawSourceCode.strip()
        lines = rawSourceCode.split("\n")
        for i in range(2):
            if lines[0].startswith("--"):
                lines.pop(0)
        rawSourceCode = "\n".join(lines)
        return rawSourceCode.strip()

    @classmethod
    def clarifySourceCode(cls, sourceCode: str) -> str:
        clarified = sourceCode
        # The comment breaks can just go away
        clarified = re.sub(r"--\n", "\n", clarified)

        # clarified = re.sub(r"^--end$", "end", clarified, flags=re.MULTILINE)

        # raise Exception(clarified)
        # clarified = re.sub(r"--\[\[then$", "then--[[", clarified, flags=re.MULTILINE)
        # clarified = re.sub(r'--\[\[then$','wtf', clarified, flags=re.MULTILINE)
        # raise Exception(clarified)

        # no need for (empty) multiline comments
        # clarified = re.sub(r"--\[\[([\s\n]+)\]\]", r"\1", clarified)
        clarified = re.sub(r'--\[\[([\s\S]*?)\]\]', r'\1', clarified)
        # raise Exception(clarified)
        # The ang_ form
        clarified = re.sub(r"([a-zA-Z]\w+)_\b", r"\1", clarified)
        # The vy_w form
        clarified = re.sub(r"([a-zA-Z]\w+)_[a-zA-Z]\b", r"\1", clarified)
        return clarified

    @classmethod
    def minifySourceCode(cls, sourceCode: str) -> str:
        minified = sourceCode
        # minified = minified.replace('--\n', '')
        minified = re.sub(r'--\[\[then$', '--[[', minified, flags=re.MULTILINE)
        minified = re.sub(r"--\[\[[\s\S]*?\]\]", "", minified)
        minified = re.sub(r"^\s+", "", minified, flags=re.MULTILINE)
        minified = re.sub("--.*\n", "", minified)
        # For the --end hack. Don't like this
        minified = re.sub(r"^--end$", "\n", minified)
        # stash=minified
        # raise  Exception(stash + '\n\n' + minified)
        # The ang_ form
        minified = re.sub(r"([a-zA-Z])\w+_\b", r"\1", minified)
        # The vy_w form
        minified = re.sub(r"[a-zA-Z]\w+_([a-zA-Z])\b", r"\1", minified)
        return minified

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
    def getConfig(cls, metadata: Metadata) -> Config:
        return Config(
            gameAuthor=config("GAME_AUTHOR"),
            itchAuthor=config("ITCH_USERNAME").lower(),
            sourceControlRootUrl="https://github.com/MiniMechMedia/pico8-games/tree/master/carts",
            # pico8ExePath=r"C:\Program Files (x86)\PICO-8\pico8.exe",
            pico8ExePath=config("PICO8EXE"),
            exportDir="",
        )

    @classmethod
    def parse(cls, filePath: pathlib.Path) -> ParsedContents:
        rawContents: str = cls.parseRawFileContents(filePath)
        sourceCode: str = cls.parseSourceCodeFromFileContents(rawContents)
        minifiedSourceCode: str = cls.minifySourceCode(sourceCode)
        clarifiedSourceCode: str = cls.clarifySourceCode(sourceCode)
        rawYaml: str = cls.parseRawYamlFromFileContents(rawContents)
        parsedYaml: dict = cls.parseYamlFromRawYaml(rawYaml)
        rawLabelImage: str = cls.parseRawLabelImage(rawContents)
        parsedLabelImage: ParsedLabelImage = cls.parseImageLabel(rawLabelImage)
        metadata: Metadata = cls.parseMetadata(parsedYaml)
        config: Config = cls.getConfig(metadata)
        ret = ParsedContents(
            filePath=filePath,
            rawContents=rawContents,
            sourceCode=sourceCode,
            minifiedSourceCode=minifiedSourceCode,
            clarifiedSourceCode=clarifiedSourceCode,
            labelImage=parsedLabelImage,
            metadata=metadata,
            config=config,
            pico8EduUrlMinified=None,
            pico8EduUrlClarified=None,
        )
        # Yeah, it's a hack
        ret.pico8EduUrlMinified = Pico8EduUrlCompilationTarget.compileToPico8Url(parsedContents=ret, useMinified=True)
        ret.pico8EduUrlClarified = Pico8EduUrlCompilationTarget.compileToPico8Url(parsedContents=ret, useMinified=False)
        return ret

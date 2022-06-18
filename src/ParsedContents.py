import pathlib
import yaml
import typing
from dataclasses import dataclass
from typing import Optional
from datetime import timedelta
from enum import Enum
from slugify import slugify
from pathlib import Path


class ParsedLabelImage:
    def __init__(self, data: list[list[int]]):
        self.data = data

    def __getitem__(self, xy: tuple[int, int]) -> int:
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


# TODO do something with auto() to avoid repetition
# https://stackoverflow.com/a/44785241
class ControlEnum(Enum):
    ARROW_KEYS = "ARROW_KEYS"
    X = "X"
    Z = 'Z'
    MOUSE = 'MOUSE'
    LEFT_CLICK = 'LEFT_CLICK'
    RIGHT_CLICK = 'RIGHT_CLICK'


class CartType(Enum):
    GAME = "game"
    TWEET = "tweet"
    UNKNOWN = "unknown"


@dataclass
class Metadata:
    @dataclass
    class JamInfo:
        # def __init__(self, **kwargs):
        #     self.__dict__.update(kwargs)

        jam_name: str
        jam_number: Optional[int]
        jam_theme: str
        jam_url: Optional[str]
        # TODO would prefer some general data schema like data-*
        minijam_limitation: Optional[str]

        # TODO seems like this class is getting too smart
        @property
        def correctedJamUrl(self) -> str:
            if self.jam_url:
                return self.jam_url
            if self.isTriJam:
                return f"https://itch.io/jam/trijam-{self.jam_number}/entries"
            return ""

        @property
        def isTriJam(self):
            return self.jam_name == "TriJam"

    @dataclass
    class Control:
        inputs: list[ControlEnum]
        desc: str

    description: str
    tagline: str
    game_name: str
    game_slug: Optional[str]
    jam_info: list[JamInfo]
    # TODO ponder making this a timedelta
    develop_time: Optional[str]
    controls: list[Control]  # list[dict[str, str]]  # list[Control]
    hints: str
    acknowledgements: str
    to_do: list[str]
    version: str  # TODO make a strongly typed object
    about_extra: str
    cart_type: str
    img_alt: str
    pico_url: Optional[str]

    @property
    def stronglyTypedCartType(self) -> CartType:
        try:
            return CartType(self.cart_type)
        except ValueError:
            return CartType.UNKNOWN

    @property
    def correctedGameSlug(self):
        # TODO this stuff should go in a separate layer
        return self.game_slug or slugify(self.game_name)

    @property
    def p8FileGameName(self):
        return f'{self.game_name.lower().ljust(31)}v{self.version}'

    def getTemplate(self) -> str:
        raise NotImplemented

        # # Suitable for
        # class PreparedMetadata:
        #     pass
        #
        # rawContents: str = cls.parseRawFileContents(filePath)
        # sourceCode: str = cls.parseSourceCodeFromFileContents(rawContents)
        # rawYaml: str = cls.parseRawYamlFromFileContents(rawContents)
        # parsedYaml: dict = cls.parseYamlFromRawYaml(rawYaml)
        # rawLabelImage: str = cls.parseRawLabelImage(rawContents)
        # metadata: MetaData = cls.parseMetadata(parsedYaml)


@dataclass
class Config:
    gameAuthor: str
    itchAuthor: str
    sourceControlRootUrl: str
    pico8ExePath: str
    # Where to put the exported files...
    exportDir: str


@dataclass
class ParsedContents:
    filePath: Path
    rawContents: str
    sourceCode: str
    labelImage: ParsedLabelImage
    metadata: Metadata
    config: Config

    # TODO put these as a separate object?
    coverPath: str = ""
    coverPathAbs: str = ""
    folderRelativePath: str = ""
    # def __init__(self, rawContents:):
    #     self.rawContents: str = ""
    #     self.rawYaml: str = ""
    #     # Do not use this directly. Use self.metadata
    #     self.parsedYaml: dict = {}
    #     self.rawLabelImage = None
    #     # noinspection PyTypeChecker
    #     self.metadata: MetaData = None
    #     self.sourceCode: str = ""

    @property
    def sourceCodeP8sciiCharCount(self):
        return len(self.sourceCode)

    @property
    def sourceCodeTwitterCharCount(self):
        raise NotImplemented

    # def getRawYaml(self) -> str:
    #     return self.rawYaml

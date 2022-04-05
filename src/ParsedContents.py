import pathlib
import yaml
import typing
from dataclasses import dataclass
from typing import Optional
from datetime import timedelta
from enum import Enum


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


# TODO do something with auto() to avoid repetition
# https://stackoverflow.com/a/44785241
class ControlEnum(Enum):
    ARROW = "ARROW"
    X = "X"


@dataclass
class MetaData:
    @dataclass
    class JamInfo:
        # def __init__(self, **kwargs):
        #     self.__dict__.update(kwargs)

        jam_name: str
        jam_number: Optional[int]
        jam_theme: str
        jam_url: Optional[str]

    @dataclass
    class Control:
        key: ControlEnum
        desc: str

    description: str
    tagline: str
    game_name: str
    game_slug: Optional[str]
    jam_info: list[JamInfo]
    # TODO ponder making this a timedelta
    develop_time: Optional[str]
    controls: list[Control]  # list[dict[str, str]]  # list[Control]
    # hints: list[str] or str
    acknowledgements: str
    to_do: list[str]
    version: str  # TODO make a strongly typed object
    about_extra: str

    def getTemplate(self) -> str:
        raise NotImplemented


class ParsedContents:
    def __init__(self):
        self.rawContents: str = ""
        self.rawYaml: str = ""
        # Do not use this directly. Use self.metadata
        self.parsedYaml: dict = {}
        self.rawLabelImage = None
        # noinspection PyTypeChecker
        self.metadata: MetaData = None
        self.sourceCode: str = ""

    @property
    def sourceCodeP8sciiCharCount(self):
        return len(self.sourceCode)

    @property
    def sourceCodeTwitterCharCount(self):
        raise NotImplemented

    def getRawYaml(self) -> str:
        return self.rawYaml

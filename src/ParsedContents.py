import pathlib
import yaml
import typing
from dataclasses import dataclass
from typing import Optional
from datetime import timedelta


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


@dataclass
class MetaData:
    @dataclass
    class JamInfo:
        pass

    @dataclass
    class Control:
        key: str

    description: str
    tagline: str
    game_name: str
    game_slug: Optional[str]
    # jam_info: list[JamInfo]
    develop_time: Optional[timedelta]
    # controls: list[Control]
    # hints: list[str] or str
    acknowledgements: str
    left_todo: list[str]
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
        self.metadata: MetaData

    def getRawYaml(self) -> str:
        return self.rawYaml

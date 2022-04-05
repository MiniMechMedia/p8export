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

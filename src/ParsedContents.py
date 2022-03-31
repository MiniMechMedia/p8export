import pathlib


# class Pico8FileParser:
#     def __init__(self):
#         self.rawContents = None
#
#     def parse(self, filepath: pathlib.Path) -> ParsedContents:
#         with open(filepath) as file:
#             self.rawContents = file.read()
#
#         return ParsedContents()


class ParsedContents:
    def __init__(self, rawContents: str):
        self.rawContents: str = rawContents
        self.rawYaml: str = ""
        self.parseYaml()

    def parseYaml(self):
        rawYaml: str = self.rawContents.split("--[[")[1]
        rawYaml = rawYaml.split("--]]")[0]
        self.rawYaml = rawYaml.strip()
        # self.rawYaml: str =

    @classmethod
    def fromPath(cls, filepath: pathlib.Path) -> "ParsedContents":
        with open(filepath) as file:
            return cls(file.read())

    def getRawYaml(self) -> str:
        return self.rawYaml

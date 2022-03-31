from src.CompilationTarget import CompilationTarget
from src.ParsedContents import ParsedLabelImage, ParsedContents
from PIL import Image
from typing import Final
import pathlib


class ImagesCompilationTarget(CompilationTarget):
    SCALE: Final[int] = 3

    def compile(self, data: ParsedContents):
        raise NotImplemented

    @staticmethod
    def writeLabelImage(parsedImage: ParsedLabelImage, outputPath: pathlib.Path):
        img: Image = Image.new(
            "RGB",
            (
                ImagesCompilationTarget.SCALE * parsedImage.width,
                ImagesCompilationTarget.SCALE * parsedImage.height,
            ),
        )
        pixels: list[tuple[int]] = []
        for row in parsedImage.data:
            for i in range(ImagesCompilationTarget.SCALE):
                for index in row:
                    for j in range(ImagesCompilationTarget.SCALE):
                        pixels.append(
                            ImagesCompilationTarget.convertToPico8Palette(index)
                        )

        # noinspection PyTypeChecker
        img.putdata(pixels)

        img.save(outputPath)

    # https://pico-8.fandom.com/wiki/Palette
    @staticmethod
    def convertToPico8Palette(index: int) -> tuple[int]:
        return [
            (0, 0, 0),
            (29, 43, 83),
            (126, 37, 83),
            (0, 135, 81),
            (171, 82, 54),
            (95, 87, 79),
            (194, 195, 199),
            (255, 241, 232),
            (255, 0, 77),
            (255, 163, 0),
            (255, 236, 39),
            (0, 228, 54),
            (41, 173, 255),
            (131, 118, 156),
            (255, 119, 168),
            (255, 204, 170),
            (41, 24, 20),
            (17, 29, 53),
            (66, 33, 54),
            (18, 83, 89),
            (116, 47, 41),
            (73, 51, 59),
            (162, 136, 121),
            (243, 239, 125),
            (190, 18, 80),
            (255, 108, 36),
            (168, 231, 46),
            (0, 181, 67),
            (6, 90, 181),
            (117, 70, 101),
            (255, 110, 89),
            (255, 157, 129),
        ][index]

    @staticmethod
    def writeCoverImage(parsedImage: ParsedLabelImage):
        pass

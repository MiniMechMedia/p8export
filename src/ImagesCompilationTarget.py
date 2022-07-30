from src.CompilationTarget import CompilationTarget
from src.ParsedContents import ParsedLabelImage, ParsedContents
from PIL import Image
from typing import Final
import pathlib


class ImagesCompilationTarget(CompilationTarget):
    SCALE: Final[int] = 3
    SIDEBAR_WIDTH: Final[int] = 34

    @classmethod
    def writeCoverImage(
        cls, parsedImage: ParsedLabelImage, outputPath: pathlib.Path
    ) -> None:
        width = cls.SCALE * (parsedImage.width + cls.SIDEBAR_WIDTH)
        height = cls.SCALE * parsedImage.height
        img: Image = Image.new("RGB", (width, height))
        pixels: list[tuple[int, int, int]] = []
        for row in parsedImage.data:

            for i in range(cls.SCALE):
                for _ in range(cls.SIDEBAR_WIDTH // 2 * cls.SCALE):
                    pixels.append((0, 0, 0))
                for index in row:
                    for j in range(cls.SCALE):
                        pixels.append(cls.convertToPico8Palette(index))
                for _ in range(cls.SIDEBAR_WIDTH // 2 * cls.SCALE):
                    pixels.append((0, 0, 0))

        # noinspection PyTypeChecker
        img.putdata(pixels)

        img.save(outputPath)

    @classmethod
    def writeLabelImage(
        cls, parsedImage: ParsedLabelImage, outputPath: pathlib.Path
    ) -> None:
        img: Image = Image.new(
            "RGB",
            (
                cls.SCALE * parsedImage.width,
                cls.SCALE * parsedImage.height,
            ),
        )
        pixels: list[tuple[int, int, int]] = []
        for row in parsedImage.data:
            for i in range(cls.SCALE):
                for index in row:
                    for j in range(cls.SCALE):
                        pixels.append(cls.convertToPico8Palette(index))

        # noinspection PyTypeChecker
        img.putdata(pixels)

        img.save(outputPath)

    # https://pico-8.fandom.com/wiki/Palette
    @staticmethod
    def convertToPico8Palette(index: int) -> tuple[int, int, int]:
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

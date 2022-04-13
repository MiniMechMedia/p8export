import unittest

from BaseTest import BaseTest
from src.FileRegistry import TestFileEnum, TemplateFileEnum, TempFileEnum
from src.pico8fileparser import Pico8FileParser
from src.ParsedContents import ParsedContents
from src.TemplateEvaluator import TemplateEvaluator, RenderType


class TestTemplating(BaseTest):
    def test_can_evaluate_description(self) -> None:
        parsed: ParsedContents = Pico8FileParser.parse(
            self.getTestFilePath(TestFileEnum.TWEET_CART_TEMPLATE_FILE)
        )

        evaluated: str = TemplateEvaluator.evaluateStringTemplateToString(
            parsedContents=parsed,
            strTemplate="{description}",
            renderType=RenderType.BASIC,
        )

        self.assertContentsEqual(
            actual=evaluated,
            expected=TestFileEnum.BASIC_DESCRIPTION_EVALUATED_FILE,
        )

    def test_can_evaluate_tweet_characteristics(self) -> None:
        parsed: ParsedContents = Pico8FileParser.parse(
            self.getTestFilePath(TestFileEnum.TWEET_CART_TEMPLATE_FILE)
        )

        evaluated: str = TemplateEvaluator.evaluateStringTemplateToString(
            parsedContents=parsed,
            strTemplate="{char_count} chars\n\n{source_code}",
            renderType=RenderType.BASIC,
        )

        self.assertContentsEqual(
            actual=evaluated,
            expected=TestFileEnum.TWEET_CART_TEMPLATE_EVALUATED_DESCRIPTION_FILE,
        )

    def test_can_evaluate_entry(self) -> None:
        parsed: ParsedContents = Pico8FileParser.parse(
            self.getTestFilePath(TestFileEnum.BASIC_GAME_TEMPLATE_FILE)
        )
        TemplateEvaluator.evaluateTemplateToFile(
            parsedContents=parsed,
            template=TemplateFileEnum.ITCH_GAME_DESCRIPTION_MD,
            outputFile=self.getTempFilePath(
                TempFileEnum.ITCH_DESCRIPTION_EVALUATED_FILE
            ),
        )

        self.assertFilesEqual(
            actual=TempFileEnum.ITCH_DESCRIPTION_EVALUATED_FILE,
            expected=TestFileEnum.ITCH_DESCRIPTION_EVALUATED_FILE,
        )

    # def test_can_evaluate_controls(self):

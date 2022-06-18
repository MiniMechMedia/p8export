import unittest

from BaseTest import BaseTest
from src.FileRegistry import TestFileEnum, TemplateFileEnum, TempFileEnum
from src.pico8fileparser import Pico8FileParser
from src.ParsedContents import ParsedContents
from src.TemplateEvaluator import TemplateEvaluator, RenderType


class TestTemplating(BaseTest):
    def test_can_evaluate_description(self) -> None:
        parsed: ParsedContents = Pico8FileParser.parse(
            self.getTestFilePath(TestFileEnum.TWEET_CART_TEST_FILE)
        )

        evaluated: str = TemplateEvaluator.evaluateStringTemplateToString(
            parsedContents=parsed,
            strTemplate="{{description}}",
            renderType=RenderType.BASIC,
        )

        self.assertContentsEqual(
            actual=evaluated,
            expected=TestFileEnum.GAME_STRING_TEMPLATE_EXPECTED,
        )

    def test_can_evaluate_tweet_characteristics(self) -> None:
        parsed: ParsedContents = Pico8FileParser.parse(
            self.getTestFilePath(TestFileEnum.TWEET_CART_TEST_FILE)
        )

        evaluated: str = TemplateEvaluator.evaluateStringTemplateToString(
            parsedContents=parsed,
            strTemplate="{{char_count}} chars\n\n{{source_code}}",
            renderType=RenderType.BASIC,
        )

        self.assertContentsEqual(
            actual=evaluated,
            expected=TestFileEnum.TWEET_STRING_TEMPLATE_EXPECTED,
        )

    def assertCartRendersAsExpected(self,
                                    cartFile: TestFileEnum,
                                    templateFile: TemplateFileEnum,
                                    tempFile: TempFileEnum,
                                    expectedFile: TestFileEnum) -> None:
        parsed: ParsedContents = Pico8FileParser.parse(self.getTestFilePath(cartFile))
        TemplateEvaluator.evaluateTemplateToFile(
            parsedContents=parsed,
            template=templateFile,
            outputFile = self.getTempFilePath(tempFile)
        )

        self.assertFilesEqual(
            actual=tempFile,
            expected=expectedFile
        )

    def test_descriptions(self):
        with self.subTest("game itch description"):
            self.assertCartRendersAsExpected(
                cartFile=TestFileEnum.GAME_CART_TEST_FILE,
                templateFile=TemplateFileEnum.GAME_ITCH_DESCRIPTION_TEMPLATE,
                tempFile=TempFileEnum.GAME_ITCH_DESCRIPTION_ACTUAL,
                expectedFile=TestFileEnum.GAME_ITCH_DESCRIPTION_EXPECTED
            )

        with self.subTest("game github description"):
            self.assertCartRendersAsExpected(
                cartFile=TestFileEnum.GAME_CART_TEST_FILE,
                templateFile=TemplateFileEnum.GAME_GITHUB_README_TEMPLATE,
                tempFile=TempFileEnum.GAME_GITHUB_README_ACTUAL,
                expectedFile=TestFileEnum.GAME_GITHUB_README_EXPECTED
            )

        # TODO add missing test
        with self.subTest("tweet itch description"):
            self.assertCartRendersAsExpected(
                cartFile=TestFileEnum.TWEET_CART_TEST_FILE,
                templateFile=TemplateFileEnum.TWEET_ITCH_DESCRIPTION_TEMPLATE,
                tempFile=TempFileEnum.TWEET_ITCH_DESCRIPTION_ACTUAL,
                expectedFile=TestFileEnum.TWEET_ITCH_DESCRIPTION_EXPECTED
            )

        with self.subTest("tweet github description"):
            self.assertCartRendersAsExpected(
                cartFile=TestFileEnum.TWEET_CART_TEST_FILE,
                templateFile=TemplateFileEnum.TWEET_GITHUB_README_TEMPLATE,
                tempFile=TempFileEnum.TWEET_ITCH_DESCRIPTION_ACTUAL,
                expectedFile=TestFileEnum.TWEET_GITHUB_README_EXPECTED
            )

    # TODO needs more test around html and stuff??

    # def test_can_evaluate_controls(self):

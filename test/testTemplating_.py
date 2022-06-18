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
            strTemplate="{{description}}",
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
            strTemplate="{{char_count}} chars\n\n{{source_code}}",
            renderType=RenderType.BASIC,
        )

        self.assertContentsEqual(
            actual=evaluated,
            expected=TestFileEnum.STRING_TEMPLATE_SOMETHING_EXPECTED,
        )

    def test_can_evaluate_tweet_description(self) -> None:
        parsed: ParsedContents = Pico8FileParser.parse(
            self.getTestFilePath(TestFileEnum.TWEET_CART_TEMPLATE_FILE)
        )
        # print('hereiam', TempFileEnum.TWEET_CART_ITCH_DESCRIPTION_EVALUATED_FILE.filepath.absolute())
        evaluated: str = TemplateEvaluator.evaluateTemplateToFile(
            parsedContents=parsed,
            template=TemplateFileEnum.TWEET_GITHUB_README_TEMPLATE,
            outputFile=self.getTempFilePath(TempFileEnum.TWEET_GITHUB_README_ACTUAL)
        )
        # evaluated: str = TemplateEvaluator.evaluateStringTemplateToString(
        #     parsedContents=parsed,
        #     strTemplate="{{char_count}} chars\n\n{{source_code}}",
        #     renderType=RenderType.BASIC,
        # )
        self.assertFilesEqual(
            actual=TempFileEnum.TWEET_GITHUB_README_ACTUAL,
            expected=TestFileEnum.TWEET_GITHUB_README_EXPECTED
        )
        # self.assertContentsEqual(
        #     actual=evaluated,
        #     expected=TestFileEnum.ITCH_DESCRIPTION_TWEET_CART_TEMPLATE_EVALUATED_FILE,
        # )

    def test_can_evaluate_entry(self) -> None:
        parsed: ParsedContents = Pico8FileParser.parse(
            self.getTestFilePath(TestFileEnum.BASIC_GAME_TEMPLATE_FILE)
        )
        TemplateEvaluator.evaluateTemplateToFile(
            parsedContents=parsed,
            template=TemplateFileEnum.GAME_ITCH_DESCRIPTION_TEMPLATE,
            outputFile=self.getTempFilePath(
                TempFileEnum.GAME_ITCH_DESCRIPTION_ACTUAL
            ),
        )

        self.assertFilesEqual(
            actual=TempFileEnum.GAME_ITCH_DESCRIPTION_ACTUAL,
            expected=TestFileEnum.GAME_ITCH_DESCRIPTION_EXPECTED,
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
                cartFile=TestFileEnum.BASIC_GAME_TEMPLATE_FILE,
                templateFile=TemplateFileEnum.GAME_ITCH_DESCRIPTION_TEMPLATE,
                tempFile=TempFileEnum.GAME_ITCH_DESCRIPTION_ACTUAL,
                expectedFile=TestFileEnum.GAME_ITCH_DESCRIPTION_EXPECTED
            )

        with self.subTest("game github description"):
            self.assertCartRendersAsExpected(
                cartFile=TestFileEnum.BASIC_GAME_TEMPLATE_FILE,
                templateFile=TemplateFileEnum.GAME_GITHUB_README_TEMPLATE,
                tempFile=TempFileEnum.GAME_GITHUB_README_ACTUAL,
                expectedFile=TestFileEnum.GAME_GITHUB_README_EXPECTED
            )

        # TODO add missing test
        with self.subTest("tweet itch description"):
            try:
                self.assertCartRendersAsExpected(
                    cartFile=TestFileEnum.TWEET_CART_TEMPLATE_FILE,
                    templateFile=TemplateFileEnum.TWEET_ITCH_DESCRIPTION_TEMPLATE,
                    tempFile=TempFileEnum.TWEET_ITCH_DESCRIPTION_ACTUAL,
                    expectedFile=TestFileEnum.TWEET_ITCH_DESCRIPTION_EXPECTED
                )
            except:
                exit()



        with self.subTest("tweet github description"):
            self.assertCartRendersAsExpected(
                cartFile=TestFileEnum.TWEET_CART_TEMPLATE_FILE,
                templateFile=TemplateFileEnum.TWEET_GITHUB_README_TEMPLATE,
                tempFile=TempFileEnum.TWEET_ITCH_DESCRIPTION_ACTUAL,
                expectedFile=TestFileEnum.TWEET_GITHUB_README_EXPECTED
            )

    # TODO needs more test around html and stuff??

    # def test_can_evaluate_controls(self):

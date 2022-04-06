from BaseTest import BaseTest
from src.FileRegistry import TestFileEnum
from src.pico8fileparser import Pico8FileParser
from src.ParsedContents import ParsedContents
from src.TemplateEvaluator import TemplateEvaluator


class TestTemplating(BaseTest):
    def test_can_evaluate_description(self):
        parsed: ParsedContents = Pico8FileParser.parse(
            TestFileEnum.TWEET_CART_TEMPLATE_FILE.filepath
        )

        TemplateEvaluator.evaluateStringTemplateToString(
            parsedContents=parsed, strTemplate="{description}"
        )

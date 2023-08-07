from test.BaseTest import BaseTest
from src.Pico8EduUrlCompliationTarget import Pico8EduUrlCompilationTarget
from src.pico8fileparser import Pico8FileParser
from src.ParsedContents import ParsedContents, Metadata, ControlEnum
from src.FileRegistry import TestFileEnum, TempFileEnum

class TestP8EduUrl(BaseTest):
    def test_can_create_minified_source(self):
        parsedContents = self.parseFile(TestFileEnum.TWEET_CART_ANNOTATED_TEST_FILE)
        result = Pico8EduUrlCompilationTarget.createMinifiedCartContents(parsedContents)
        assert parsedContents.minifiedSourceCode in result

    def test_can_create_rom(self):
        parsedContents = self.parseFile(TestFileEnum.TWEET_CART_ANNOTATED_TEST_FILE)
        result = Pico8EduUrlCompilationTarget.writeFullRomMinified(
            parsedContents.config,
            parsedContents
        )
        # assert parsedContents.minifiedSourceCode in result
        self.assertFileExists(TempFileEnum.TWEET_CART_MINIFIED_ROM)
        assert len(result) == 32768

    def test_can_extract_source(self):
        parsedContents = self.parseFile(TestFileEnum.TWEET_CART_ANNOTATED_TEST_FILE)
        result = Pico8EduUrlCompilationTarget.writeFullRomMinified(
            parsedContents.config,
            parsedContents
        )
        code = Pico8EduUrlCompilationTarget.extractCodeFromRom(result)
        assert len(code) == 348
        # raise Exception(str(code))

    def test_can_get_url(self):
        parsedContents = self.parseFile(TestFileEnum.TWEET_CART_ANNOTATED_TEST_FILE)
        url = Pico8EduUrlCompilationTarget.compileToPico8Url(parsedContents)
        assert url == 'https://pico-8-edu.com/?c=AHB4YQGiAVzrwVscfvP5h9-vgdeYMEP1Du9w-hs8wwuULxClqR-236EOkuIp3uEdBtqir_OotEBfBWF73EnBSJp1G29w0yPkO_nF6UCRjHRt07xCtRFONGF735isyEg3sRUHzUCcZVWWpVlTZdVItVMMvUUcvkUcJAdJi2csv3Jwb6W57SWS684bGo2KbiTY2gzeoQii6rbksvjO_rqu7dqymqjmokgnYCRsHiXKytmlrLnwziIp7hxKzkzj0LIblgj2bk3DkbJc2HiF7h22TDK9vDgb9QP9bDTSPIYHdn2QVsXUeFZXmzff-gbLOy6RChodndwe3MlXBEQ2bh24YXG-2UnHJ_Mym5qoo6iOdAmig7UKwo2ltRGlgNU6nggFQ3JZgXv3qpGZ4oTdpioKpbDpEzY3D5nZXw99EjcnLCyMrS9tDpbdSLlXduMTTpIfSweboWwqzkaLleUS'

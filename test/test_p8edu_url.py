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
        assert len(code) == 356
        # raise Exception(str(code))

    def test_can_get_url(self):
        parsedContents = self.parseFile(TestFileEnum.TWEET_CART_ANNOTATED_TEST_FILE)
        url = Pico8EduUrlCompilationTarget.compileToPico8Url(parsedContents)
        print('here iam', url)
        assert url == 'https://pico-8-edu.com/?c=AHB4YQHBAWTrwd0nH188xEvMPsNL3B4kjcGfl7jkkFOKZCgPnuAB3qAom-b8FzDBA2QTqSXChwiDpNh4hpWuLjbSZ4hKC9RVELbHHRUspVn3Eo_wM5KvpBcrBwTCAYFuSJG3WXae6kC3MhDmLxEFTTWSZVWWlVlTZZUa2ZIa0UHS4lkKwhvf4jUGmrmnSAbP23iJqOgGg5254CGKIKqOS06LD63P69quLauJaieKdAJGwuZRoqycXcuaEw8tkuLQoeTONA4tu2GJYO3YNBwpy4WNZ_geYssks6OL81E-0J8QjTQXeOAEH6RVMXVCVlebN9-_Bss7LpEKGh2dHB-cyVcERDZuHbhg8YpmJx2fjMtsaqKOojrSJYgO1ioIN5bWRpQCVut4IhQMyWUF7t2rRmaKC3abqiiUwqZP2Nw8ZGZ-PfRJ3JywsDC2vrQ5WHYj5V7ZjU84SX4sHWyGsqk4Gy1Wlks='


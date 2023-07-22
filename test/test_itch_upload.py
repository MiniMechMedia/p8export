from src.ItchGameCompilationTarget import ItchGameCompilationTarget
from test.BaseTest import BaseTest
from src.FileRegistry import TestFileEnum
from src.ParsedContents import ParsedContents
import unittest
from pathlib import Path


# TODO not sure if I really want/need to test this
@unittest.skip
class TestItchUpload(BaseTest):
    def test_can_upload_to_itch(self):
        parsed: ParsedContents = self.parseFile(TestFileEnum.GAME_CART_TEST_FILE)
        parsed.metadata.game_slug = "test-game"  # TODO
        ItchGameCompilationTarget.uploadToItch(parsed, Path("tmp/html_export"))

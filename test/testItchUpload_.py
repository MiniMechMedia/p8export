from src.ItchGameCompilationTarget import ItchGameCompilationTarget
from BaseTest import BaseTest
from src.FileRegistry import TestFileEnum
from src.ParsedContents import ParsedContents


class TestItchUpload(BaseTest):
    def test_can_upload_to_itch(self):
        parsed: ParsedContents = self.parseFile(TestFileEnum.BASIC_GAME_TEMPLATE_FILE)
        parsed.metadata.game_slug = "test-game"  # TODO
        ItchGameCompilationTarget.uploadToItch(parsed)

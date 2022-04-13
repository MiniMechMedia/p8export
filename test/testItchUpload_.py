from src.ItchGameCompilationTarget import ItchGameCompilationTarget
from BaseTest import BaseTest


class TestItchUpload(BaseTest):
    def test_can_upload_to_itch(self):
        ItchGameCompilationTarget.uploadToItch(None)

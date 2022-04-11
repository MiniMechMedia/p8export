from BaseTest import BaseTest
from src.ReadmeCompilationTarget import ReadmeCompilationTarget
from src.FileRegistry import TestFileEnum


class TestReadme(BaseTest):
    def test_games_tag_not_required(self):
        testSlug = "mongo-bongo"
        gameSnippet = "this is a test snippet of Mongo Bongo"
        result: str = ReadmeCompilationTarget.addToAggregateReadmeStr(
            slug=testSlug, existingReadmeContents="", gameSnippet=gameSnippet
        )

        self.assertEqual(
            result,
            f"""<!--BEGIN GAMES-->
<!--BEGIN mongo-bongo-->
this is a test snippet of Mongo Bongo
<!--END mongo-bongo-->
""",
        )

    def test_can_add_game_description(self):
        # use the same file
        pass

    def test_can_replace_existing(self):
        result: str = ReadmeCompilationTarget.addToAggregateReadmeStr(
            slug="mongo-bongo",
            existingReadmeContents=self.getTestFileContents(
                TestFileEnum.AGGREGATE_README_BEFORE_FILE
            ),
            gameSnippet="And this is what Mongo Bongo should\nbe now",
        )
        from src.FileRegistry import TempFileEnum

        with open(
            self.getTempFilePath(TempFileEnum.AGGREGATE_README_UPDATED_AFTER), "w"
        ) as file:
            file.write(result)

        self.assertFilesEqual(
            actual=TempFileEnum.AGGREGATE_README_UPDATED_AFTER,
            expected=TestFileEnum.AGGREGATE_README_AFTER_UPDATE_FILE,
        )
        # self.assertContentsEqual(
        #     actual=result, expected=TestFileEnum.AGGREGATE_README_AFTER_FILE
        # )

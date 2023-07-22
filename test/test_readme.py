from test.BaseTest import BaseTest
from src.ReadmeCompilationTarget import ReadmeCompilationTarget
from src.FileRegistry import TestFileEnum, TempFileEnum


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
        result: str = ReadmeCompilationTarget.addToAggregateReadmeStr(
            slug="onyx-oryx",
            existingReadmeContents=self.getTestFileContents(
                TestFileEnum.AGGREGATE_README_BEFORE_FILE
            ),
            gameSnippet="Use your razor sharp horns to dig into the mountain!",
        )

        with open(
            self.getTempFilePath(TempFileEnum.AGGREGATE_GITHUB_README_ADDED_ACTUAL), "w"
        ) as file:
            file.write(result)

        self.assertFilesEqual(
            actual=TempFileEnum.AGGREGATE_GITHUB_README_ADDED_ACTUAL,
            expected=TestFileEnum.AGGREGATE_README_AFTER_ADD_FILE,
        )

    def test_can_replace_existing(self):
        result: str = ReadmeCompilationTarget.addToAggregateReadmeStr(
            slug="mongo-bongo",
            existingReadmeContents=self.getTestFileContents(
                TestFileEnum.AGGREGATE_README_BEFORE_FILE
            ),
            gameSnippet="And this is what Mongo Bongo should\nbe now",
        )

        with open(
            self.getTempFilePath(TempFileEnum.AGGREGATE_GITHUB_README_UPDATED_ACTUAL), "w"
        ) as file:
            file.write(result)

        self.assertFilesEqual(
            actual=TempFileEnum.AGGREGATE_GITHUB_README_UPDATED_ACTUAL,
            expected=TestFileEnum.AGGREGATE_README_AFTER_UPDATE_FILE,
        )
        # self.assertContentsEqual(
        #     actual=result, expected=TestFileEnum.AGGREGATE_README_AFTER_FILE
        # )

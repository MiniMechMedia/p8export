from src.ParsedContents import ParsedContents, CartType
from src.CompilationTarget import CompilationTarget
from pathlib import Path
from src.TemplateEvaluator import TemplateEvaluator
from src.FileRegistry import TemplateFileEnum

# TODO rename this since it's gonna be used for game.xml as well as submission.html
class ReadmeCompilationTarget(CompilationTarget):
    BEGIN_GAMES_TAG: str = "<!--BEGIN GAMES-->\n"

    @classmethod
    def beginGameTag(cls, slug: str):
        return f"<!--BEGIN {slug}-->\n"

    @classmethod
    def endGameTag(cls, slug: str):
        return f"<!--END {slug}-->\n"

    @classmethod
    def createIndividualReadme(
        cls, parsedContents: ParsedContents, readmeOutputPath: Path
    ) -> None:
        # templateFile: TemplateFileEnum = TemplateEvaluator.chooseTemplate(parsedContents=parsedContents)
        templateFile: TemplateFileEnum
        if parsedContents.metadata.stronglyTypedCartType == CartType.TWEET:
            templateFile = TemplateFileEnum.GAME_GITHUB_README
        else:
            templateFile = TemplateFileEnum.GAME_GITHUB_README

        TemplateEvaluator.evaluateTemplateToFile(
            parsedContents=parsedContents,
            template=templateFile,
            outputFile=readmeOutputPath,
        )

    @classmethod
    def addToAggregateReadme(
        cls, parsedContents: ParsedContents, readmeOutputPath: Path
    ) -> None:
        snippet: str = TemplateEvaluator.evaluateTemplateToString(
            parsedContents=parsedContents, template=TemplateFileEnum.AGGREGATE_GITHUB_README
        )

        if not readmeOutputPath.exists():
            readmeOutputPath.write_text(f"\n{cls.BEGIN_GAMES_TAG}\n")

        existingReadmeContents: str = readmeOutputPath.read_text()
        newContents: str = cls.addToAggregateReadmeStr(
            slug=parsedContents.metadata.correctedGameSlug,
            existingReadmeContents=existingReadmeContents,
            gameSnippet=snippet,
        )

        readmeOutputPath.write_text(newContents)

    @classmethod
    def addToAggregateReadmeStr(
        cls, slug: str, existingReadmeContents: str, gameSnippet: str
    ) -> str:

        preamble: str
        games: str
        splitContents = existingReadmeContents.split(cls.BEGIN_GAMES_TAG, 1)
        if len(splitContents) == 1:
            preamble, games = "", existingReadmeContents
        else:
            # Should be exactly 2
            preamble, games = splitContents

        # beginTag: str = f"<!--BEGIN {slug}-->"
        # endTag: str = f"<!--END {slug}-->"
        beginTag: str = cls.beginGameTag(slug)
        endTag: str = cls.endGameTag(slug)

        if beginTag in games:
            preThisGame: str
            postThisGameInclusive: str
            postThisGameExclusive: str

            preThisGame, postThisGameInclusive = games.split(beginTag)
            _, postThisGameExclusive = postThisGameInclusive.split(endTag)

            games = (
                f"{preThisGame}{beginTag}{gameSnippet}\n{endTag}{postThisGameExclusive}"
            )
        else:
            games = f"{beginTag}{gameSnippet}\n{endTag}{games}"

        return f"{preamble}{cls.BEGIN_GAMES_TAG}{games}"

from src.ParsedContents import ParsedContents, CartType
from src.CompilationTarget import CompilationTarget
from pathlib import Path
from src.TemplateEvaluator import TemplateEvaluator
from src.FileRegistry import TemplateFileEnum

# TODO rename this since it's gonna be used for game.xml as well as submission.html
class ReadmeCompilationTarget(CompilationTarget):
    @classmethod
    def createIndividualReadme(
        cls, parsedContents: ParsedContents, readmeOutputPath: Path
    ) -> None:
        # templateFile: TemplateFileEnum = TemplateEvaluator.chooseTemplate(parsedContents=parsedContents)
        templateFile: TemplateFileEnum
        if parsedContents.metadata.stronglyTypedCartType == CartType.TWEET:
            templateFile = TemplateFileEnum.README_GAME_MD
        else:
            templateFile = TemplateFileEnum.README_GAME_MD

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
            parsedContents=parsedContents, template=TemplateFileEnum.AGGREGATE_README_MD
        )

        beginGamesTag = "<!--BEGIN GAMES-->"

        if not readmeOutputPath.exists():
            readmeOutputPath.write_text(f"\n{beginGamesTag}\n")

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
        beginGamesTag = "<!--BEGIN GAMES-->"

        preamble: str
        games: str
        preamble, games = existingReadmeContents.split(beginGamesTag)

        beginTag: str = f"<!--BEGIN {slug}-->"
        endTag: str = f"<!--END {slug}-->"

        if beginTag in games:
            preThisGame: str
            postThisGameInclusive: str
            postThisGameExclusive: str

            preThisGame, postThisGameInclusive = games.split(beginTag)
            _, postThisGameExclusive = postThisGameInclusive.split(endTag)

            games = f"{preThisGame}{beginTag}\n{gameSnippet}\n{endTag}"
        else:
            games = f"{beginTag}\n{gameSnippet}\n{endTag}\n{games}"

        return f"{preamble}{beginGamesTag}\n{games}"

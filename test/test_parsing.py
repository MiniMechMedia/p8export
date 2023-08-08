from test.BaseTest import BaseTest
from src.FileRegistry import TestFileEnum
from src.pico8fileparser import Pico8FileParser
from src.ParsedContents import ParsedContents, Metadata, ControlEnum
from textwrap import dedent


# class TestMe: pass
class TestParsing(BaseTest):
    # def test_parsing(self):
    #     parsed: ParsedContents = Pico8FileParser.parse(
    #         self.getTestFilePath(TestFileEnum.BASIC_GAME_TEMPLATE_FILE)
    #     )

    def test_parsing_metadata(self):
        # contents: str = self.getTestFileContents(TestFileEnum.BASIC_GAME_TEMPLATE_FILE)
        # rawYaml: str = Pico8FileParser.parseRawYamlFromFileContents(contents)
        # parsedYaml: dict = Pico8FileParser.parseYamlFromRawYaml(rawYaml)
        # metadata: MetaData = Pico8FileParser.parseMetadata(parsedYaml)
        parsed: ParsedContents = self.parseFile(TestFileEnum.GAME_CART_TEST_FILE)

        firstJam: Metadata.JamInfo = parsed.metadata.jam_info[0]
        self.assertEqual(firstJam.jam_name, "TriJam")
        self.assertEqual(firstJam.jam_number, -1)

        secondJam: Metadata.JamInfo = parsed.metadata.jam_info[1]
        self.assertEqual(secondJam.jam_name, "MiniJam")
        self.assertEqual(secondJam.jam_number, None)

        firstControl: Metadata.Control = parsed.metadata.controls[0]
        self.assertEqual(firstControl.inputs, [ControlEnum.ARROW_KEYS])
        secondControl: Metadata.Control = parsed.metadata.controls[1]
        self.assertEqual(secondControl.inputs, [ControlEnum.X, ControlEnum.Z])

    def test_parsing_sourcecode(self):
        parsed: ParsedContents = self.parseFile(TestFileEnum.TWEET_CART_TEST_FILE)

        self.assertEqual(parsed.sourceCodeP8sciiCharCount, 277)

    def test_minify_sourcecode_indentation(self):
        unminified = dedent('''\
        for i=1,100do
            if x>1then
                print('hi')
            end
        end
        '''
        )
        minified_expected = dedent('''\
        for i=1,100do
        if x>1then
        print('hi')
        end
        end
        ''')
        minified_actual = Pico8FileParser.minifySourceCode(unminified)
        self.assertEqual(minified_expected, minified_actual)

    def test_minifying_sourcecode_comments(self):
        # parsed: ParsedContents = self.parseFile(TestFileEnum.TWEET_CART_ANNOTATED_TEST_FILE)
        unminified = dedent(
            """\
        if(4>2)--[[
        ]]print('hello')--[[
        ]]print('ok')
        """
        )
        minified_expected = dedent(
            """\
        if(4>2)print('hello')print('ok')
        """
        )
        minified_actual = Pico8FileParser.minifySourceCode(unminified)
        self.assertEqual(minified_expected, minified_actual)

    def test_stripping_newlines(self):
        unminified = dedent(
            r"""
        i=0--
        c={}--
        k=128--
        """.removeprefix(
                "\n"
            )
        )
        minified_expected = "i=0c={}k=128"
        minified_actual = Pico8FileParser.minifySourceCode(unminified)
        self.assertEqual(minified_expected, minified_actual)

    def test_stripping_comments(self):
        unminified = dedent(
            r"""
        -- set i to 0
        i=0
        -- set c to empty collection
        -- this will be used for particles
        c={}--
        k=128
        --somestuff
        """.removeprefix(
                "\n"
            )
        )
        minified_expected = "i=0\nc={}k=128\n"
        minified_actual = Pico8FileParser.minifySourceCode(unminified)
        self.assertEqual(minified_expected, minified_actual)

    def test_clarifying_sourcecode_variables(self):
        unclarified = dedent(
            """\
        rnd_=rnd
        xpos_,ypos_=cos(ang_),sin(ang_)
        randval_g=rnd_()
        """
        )
        clarified_expected = dedent(
            """\
        rnd=rnd
        xpos,ypos=cos(ang),sin(ang)
        randval=rnd()
        """
        )

        clarified_actual = Pico8FileParser.clarifySourceCode(unclarified)
        self.assertEqual(clarified_expected, clarified_actual)

    def test_minifying_sourcecode_variables(self):
        # Ok so there are 2 ways to do it
        # One is you convert the vars to their readable form
        unminified = dedent(
            """\
        rnd_=rnd
        xpos_,ypos_=cos(ang_),sin(ang_)
        randval_g=rnd_()
        """
        )

        # xpos_
        # ypos_
        # v_vx
        # w_vy
        # _xpos
        # _vy
        # w_vy
        # xpos_
        # vy_w
        # randval_g

        minified_expected = dedent(
            """\
        r=rnd
        x,y=cos(a),sin(a)
        g=r()
        """
        )

        minified_actual = Pico8FileParser.minifySourceCode(unminified)
        self.assertEqual(minified_expected, minified_actual)

    def test_tweet_cart_minify_total(self):
        parsed: ParsedContents = self.parseFile(
            TestFileEnum.TWEET_CART_ANNOTATED_TEST_FILE
        )
        expected_minified = dedent(
            """\
            c={}i=0k=128f=fillp::_::if(i%k<1)flip()cls()i=0
            f(░)line(i,9,i,70,5)f()line(i,k,i,k-@i,15)
            c[i]=c[i]or{x=-k,y=0,v=0,w=0,r=rnd,o=_ENV}
            _ENV=c[i]pset(x,y,15)w+=.1g=r(8)x+=v
            y+=w
            if(y>128)poke(x,@x+1)x,y,v,w=60+g,g/5,0,0
            if(y>9and y<70and g<2)v=cos(g)/2w=sin(g)/2
            _ENV=o
            i+=1goto _
            """
        ).strip()

        expected_clarified = dedent(
            """\
            c={}
            i=0
            -- We use this value a lot, so this will save us some chars
            k128=128
            f=fillp
            ::_::
            if(i%k128<1)then
                flip()
                cls()
            i=0
            end
            f(░)
            line(i,9,i,70,5)
            f()
            line(i,k128,i,k128-@i,15)
            c[i]=c[i]or{
                xpos=-k128,
                ypos=0,
                vx=0,
                vy=0,
                r=rnd,
                oldenv=_ENV
            }
            
            _ENV=c[i]
            pset(xpos,ypos,15)
            vy+=.1
            g=r(8)
            xpos+=vx
            ypos+=vy
            if(ypos>128)then
                poke(xpos,@xpos+1)
                xpos,ypos,vx,vy=60+g,g/5,0,0
            end
            if(ypos>9and ypos<70and g<2)then
                vx=cos(g)/2
                vy=sin(g)/2
            end
            _ENV=oldenv
            i+=1
            goto _"""
        )
        # raise Exception(TestMe.__module__)
        # raise Exception(
        #     'expected: ' +
        #     str(len(expected_minified)) + '\nactual\n' +
        #     str(len(parsed.minifiedSourceCode)) + "\n" + parsed.minifiedSourceCode
        # )
        # self.assertEqual(len(parsed.minifiedSourceCode), len(expected_minified))
        open('/Users/nathandunn/Projects/p8export3/p8export-fresh/result.txt', 'w').write(parsed.clarifiedSourceCode)
        open('/Users/nathandunn/Projects/p8export3/p8export-fresh/result2.txt', 'w').write(expected_clarified)
        self.assertEqual(parsed.minifiedSourceCode, expected_minified)
        self.assertEqual(parsed.clarifiedSourceCode, expected_clarified)

        # expected_clarified =


    def test_tweet_cart_clarified_variables(self):
        parsed: ParsedContents = self.parseFile(
            TestFileEnum.TWEET_CART_ANNOTATED_TEST_FILE
        )
        unclarified = dedent(
            """\
        r=rnd
        xpos_,ypos_=cos(ang_),sin(ang_)
        randval_g=r()
        """
        )

        clarified_expected = dedent(
            """\
        r=rnd
        xpos,ypos=cos(ang),sin(ang)
        randval=r()
        """
        )

        clarified_actual = Pico8FileParser.clarifySourceCode(clarified_expected)
        self.assertEqual(clarified_actual, clarified_expected)

    def test_clarify_stripping_newline_comments(self):
        unclarified = dedent(
            """\
        -- set i to 0
        i=0
        -- set c to empty collection
        -- this will be used for particles
        c={}--
        k=128
        --somestuff
        """
        )
        clarified_expected = dedent(
            """\
        -- set i to 0
        i=0
        -- set c to empty collection
        -- this will be used for particles
        c={}
        k=128
        --somestuff
        """
        )

        clarified_actual = Pico8FileParser.clarifySourceCode(unclarified)
        self.assertEqual(clarified_expected, clarified_actual)

    def test_clarifying_conditionals(self):
        unclarified = dedent(
            """\
        if(4>2)--[[then
            ]]print('ok')
        --end
        """
        )

        clarified_expected = dedent(
            """\
        if(4>2)then
            print('ok')
        end
        """
        )
        clarified_actual = Pico8FileParser.clarifySourceCode(unclarified)
        self.assertEqual(clarified_expected, clarified_actual)

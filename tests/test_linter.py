import ast
import sys
import textwrap

import pytest

from flake8_flask_openapi_docstring.linter import FlaskOpenAPIDocStringLinter

IS_PY37 = sys.version_info.major == 3 and sys.version_info.minor == 7


@pytest.mark.parametrize(
    "code",
    [
        pytest.param(
            textwrap.dedent(
                """
                @route("/hello")
                def hello():
                    pass
                """
            ),
            id="Missing docstring",
        ),
        pytest.param(
            textwrap.dedent(
                """
                @route("/hello")
                def hello():
                    '''
                    no-op docstring
                    '''
                    pass
                """
            ),
            id="Docstring without OpenAPI fragment",
        ),
        pytest.param(
            textwrap.dedent(
                """
                @route("/hello")
                def hello():
                    '''
                    no-op docstring
                    ---
                    '''
                    pass
                """
            ),
            id="Docstring with empty YAML fragment",
        ),
        pytest.param(
            textwrap.dedent(
                """
                @route("/hello")
                def hello():
                    '''
                    ---
                    '''
                    pass
                """
            ),
            id="Empty YAML fragment only",
        ),
    ],
)
def test_linter_positive(code: str) -> None:
    """
    GIVEN a function
        AND the function is decorated with @route
        AND the function has a docstring without an OpenAPI fragment
    WHEN the linter is run
    THEN the linter returns an error
    """
    # GIVEN
    tree = ast.parse(code)
    checker = FlaskOpenAPIDocStringLinter(tree)

    # WHEN
    actual = list(checker.run())

    # THEN
    expected = [
        FlaskOpenAPIDocStringLinter.error(
            2 if IS_PY37 else 3, 0, "FO100", "Missing OpenAPI fragment in docstring"
        )
    ]

    assert actual == expected


@pytest.mark.parametrize(
    "code",
    [
        pytest.param(
            textwrap.dedent(
                """
                @route("/hello")
                def hello():
                    '''
                    ---
                    get:
                        responses:
                            200:
                    '''
                    pass
                """
            ),
            id="Decorated with @route",
        ),
        pytest.param(
            textwrap.dedent(
                """
                @app.route("/hello")
                def hello():
                    '''
                    ---
                    get:
                        responses:
                            200:
                    '''
                    pass
                """
            ),
            id="Decorated with @<module>.route",
        ),
    ],
)
def test_linter_negative(code: str) -> None:
    """
    GIVEN a function
        AND the function is decorated with @route
        AND the function has a docstring with an OpenAPI fragment
    WHEN the linter is run
    THEN the linter returns no errors
    """
    # GIVEN
    tree = ast.parse(code)
    checker = FlaskOpenAPIDocStringLinter(tree)

    # WHEN
    actual = list(checker.run())

    # THEN
    assert len(actual) == 0


# @pytest.mark.parametrize("lineno", range(2))
# @pytest.mark.parametrize("offset", range(2))
# @pytest.mark.parametrize("code, message", [["U100", "my message"]])
# def test_linter_error(lineno: int, offset: int, code: str, message: str) -> None:
#     actual = FlaskOpenAPIDocStringLinter.error(lineno, offset, code, message)

#     assert actual == (lineno, offset, f"{code} {message}", FlaskOpenAPIDocStringLinter)

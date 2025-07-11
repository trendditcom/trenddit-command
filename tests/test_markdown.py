# Copyright 2024 and beyond, Trenddit. All Rights Reserved.
# https://www.trenddit.com/
# This code is Apache-2.0 licensed. Please see the LICENSE file in our repository for the full license text.
# You may use this code under the terms of the Apache-2.0 license.
# This code is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.

from pathlib import Path
from unittest.mock import MagicMock, mock_open, patch

import pytest

from trenddit_command.markdown import (count_tokens, diff, extract_variables,
                              file_select_paginate, intent_select_paginate,
                              list_files, merge_docs, parse_markdown_sections,
                              split_text_by_tokens,
                              update_markdown_with_response)


@pytest.fixture
def mock_config():
    return {
        "split": {"model": "gpt-3.5-turbo", "context-ratio": 0.8},
        "model-context": {"gpt-3.5-turbo": 4096},
    }


@patch("trenddit_command.markdown.configure.load_config")
def test_split_text_by_tokens(mock_load_config, mock_config, tmp_path):
    mock_load_config.return_value = mock_config

    test_file = tmp_path / "test.txt"
    test_file.write_text("This is a test file with some content.")

    with patch(
        "builtins.open",
        new_callable=mock_open,
        read_data="This is a test file with some content.",
    ):
        result = split_text_by_tokens(str(test_file))

    assert result == 1  # Assuming the content fits in one chunk


def test_extract_variables():
    template = "Hello {{name}}, welcome to {{location}}!"
    variables = extract_variables(template)
    assert set(variables) == {"name", "location"}


@pytest.fixture
def mock_directory(tmp_path):
    d = tmp_path / "test_dir"
    d.mkdir()
    (d / "file1.txt").touch()
    (d / "file2.py").touch()
    (d / "subdir").mkdir()
    (d / "subdir" / "file3.md").touch()
    return d


def test_list_files(mock_directory):
    files, total_pages = list_files(str(mock_directory), page=1, files_per_page=10)
    assert len(files) == 3
    assert total_pages == 1
    assert set(files) == {"file1.txt", "file2.py", str(Path("subdir") / "file3.md")}


def test_count_tokens(tmp_path):
    test_file = tmp_path / "test.txt"
    test_file.write_text("This is a test file.")

    result = count_tokens(str(test_file))
    assert result == 6  # Corrected assertion based on actual tokenization


@patch("trenddit_command.markdown.Console")
@patch("trenddit_command.markdown.Prompt.ask")
def test_intent_select_paginate(mock_ask, mock_console):
    sections = [("Intent 1", "Content 1"), ("Intent 2", "Content 2")]
    mock_ask.side_effect = ["1", "q"]

    result = intent_select_paginate(sections)
    assert result == ("Intent 1", "Content 1")

    result = intent_select_paginate(sections)
    assert result is None


@patch("trenddit_command.markdown.Console")
@patch("trenddit_command.markdown.Prompt.ask")
@patch("trenddit_command.markdown.list_files")
def test_file_select_paginate(mock_list_files, mock_ask, mock_console, mock_directory):
    mock_list_files.return_value = (["file1.txt", "file2.py"], 1)
    mock_ask.side_effect = ["1", "q"]

    result = file_select_paginate(str(mock_directory))
    assert result == str(Path(mock_directory) / "file1.txt")

    result = file_select_paginate(str(mock_directory))
    assert result is None


def test_merge_docs(tmp_path):
    source_file = tmp_path / "source.md"
    source_file.write_text("# Section 1\nContent 1\n# Section 2\nContent 2")

    expanded_file = tmp_path / "source expanded.md"
    expanded_file.write_text("# Section 1\n[merge here]\n# Section 2\n[merge here]")

    merge_docs(str(tmp_path / "source"))

    merged_file = tmp_path / "source merged.md"
    assert merged_file.exists()
    content = merged_file.read_text()
    assert "# Section 1\nContent 1\n# Section 2\nContent 2" in content


def test_diff():
    content1 = "This is a test."
    content2 = "This is a different test."
    difference = diff(content1, content2)
    assert 0 < difference < 100


def test_parse_markdown_sections():
    content = (
        "# Section 1\n\nPrompt: Test prompt 1\n# Section 2\n\nPrompt: Test prompt 2"
    )
    sections = parse_markdown_sections(content)
    assert sections == [("Section 1", "Test prompt 1"), ("Section 2", "Test prompt 2")]


def test_update_markdown_with_response(tmp_path):
    markdown_file = tmp_path / "test.md"
    markdown_file.write_text("# Title\n\nPrompt: Test prompt\n\nContent")

    update_markdown_with_response(str(markdown_file), "Title", "response.md")

    updated_content = markdown_file.read_text()
    assert "![[response.md]]" in updated_content


if __name__ == "__main__":
    pytest.main()

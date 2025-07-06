# Copyright 2024 and beyond, Trenddit. All Rights Reserved.
# https://www.trenddit.com/
# This code is Apache-2.0 licensed. Please see the LICENSE file in our repository for the full license text.
# You may use this code under the terms of the Apache-2.0 license.
# This code is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.

from pathlib import Path
from unittest.mock import MagicMock, call, mock_open, patch

import pytest
from click.testing import CliRunner

from trenddit_command.cli import (ask, audit, cli, config, gather, id, init, intents,
                         merge, refer, run, split, test, trends, validate,
                         vision)


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture
def mock_config():
    return {
        "run": {
            "lookup-folder": "../trenddit_command-vault/Code",
            "save-folder": "../trenddit_command-vault/../../Apps",
        },
        "provider-model-mapping": {"provider1": ["model1", "model2"]},
        "test": {
            "ask": "test prompt",
            "vision": "vision prompt",
            "image-path": "../trenddit_command-vault/Images/hackathon.jpg",
        },
        "ask": {
            "provider": "mock_provider",
            "prompts-folder": "../trenddit_command-vault/Prompts",
        },
        "refer-section": {
            "provider": "mock_provider",
            "lookup-folder": "../trenddit_command-vault/Raw",
        },
        "intents": {
            "provider": "mock_provider",
            "lookup-folder": "../trenddit_command-vault/Intents",
            "save-folder": "../trenddit_command-vault/Embeds",
        },
        "merge": {
            "lookup-folder": "../trenddit_command-vault/Posts",
            "dest-suffix": "expanded",
            "merge-suffix": "merged",
            "placeholder": "[merge here]",
            "prompt-prefix": "> Prompt:",
        },
        "validate": {
            "provider": "mock_provider",
            "lookup-folder": "../trenddit_command-vault/Intents",
            "save-folder": "../trenddit_command-vault/Embeds",
            "validate-prompt": "Validate this",
        },
        "vision": {
            "provider": "mock_provider",
            "model": "vision_model",
            "lookup-folder": "../trenddit_command-vault/Gather/images",
            "system": "System prompt",
            "save": True,
            "save-folder": "../trenddit_command-vault/Vision",
        },
        "vision-models": ["vision_model"],
    }


@pytest.fixture
def mock_provider_instance():
    instance = MagicMock()
    instance.ask.return_value = "../trenddit_command-vault/Posts/response.md"
    instance.stream_response.return_value = iter(["Mock ", "response"])
    instance.stream_vision_response.return_value = iter(["Vision ", "response"])
    instance.get_model_info.return_value = "Mock model info"
    return instance


@patch("trenddit_command.cli.configure.load_config")
@patch("trenddit_command.cli.utils.get_provider_instance")
@patch("trenddit_command.cli.markdown.file_select_paginate")
@patch("trenddit_command.cli.code.process_markdown_file")
def test_run(
    mock_process_markdown,
    mock_file_select,
    mock_get_provider,
    mock_load_config,
    runner,
    mock_config,
    mock_provider_instance,
):
    mock_load_config.return_value = mock_config
    mock_get_provider.return_value = mock_provider_instance
    mock_file_select.return_value = "../trenddit_command-vault/Code/selected_file.md"

    result = runner.invoke(run)
    assert result.exit_code == 0
    mock_file_select.assert_called_once_with("../trenddit_command-vault/Code")
    mock_process_markdown.assert_called_once_with(
        "../trenddit_command-vault/Code/selected_file.md",
        app_folder="../trenddit_command-vault/../../Apps",
    )


@patch("trenddit_command.cli.configure.load_config")
@patch("trenddit_command.cli.configure.save_config")
@patch("trenddit_command.cli.utils.get_provider_instance")
@patch("trenddit_command.cli.metrics.save_test_summary")
def test_test(
    mock_save_summary,
    mock_get_provider,
    mock_save_config,
    mock_load_config,
    runner,
    mock_config,
    mock_provider_instance,
):
    mock_load_config.return_value = mock_config
    mock_get_provider.return_value = mock_provider_instance
    mock_config["ask"]["model"] = "test_model"

    result = runner.invoke(test, ["ask"])
    assert result.exit_code == 0
    mock_get_provider.assert_called()
    mock_provider_instance.stream_response.assert_called()
    mock_save_summary.assert_called()


@patch("trenddit_command.cli.configure.load_config")
@patch("trenddit_command.cli.utils.get_provider_instance")
@patch("trenddit_command.cli.markdown.parse_markdown_sections")
@patch("trenddit_command.cli.markdown.diff")
def test_validate(
    mock_diff,
    mock_parse,
    mock_get_provider,
    mock_load_config,
    runner,
    mock_config,
    mock_provider_instance,
):
    mock_load_config.return_value = mock_config
    mock_get_provider.return_value = mock_provider_instance
    mock_parse.return_value = [("Intent1", "Prompt1")]
    mock_diff.return_value = 10.5

    with patch("builtins.open", mock_open(read_data=b"Mock content")), patch(
        "os.path.exists", return_value=True
    ), patch("trenddit_command.cli.click.prompt", return_value=1):
        result = runner.invoke(validate, ["-d", "../trenddit_command-vault/Intents/test_doc.md"])
        assert result.exit_code == 0
        mock_provider_instance.ask.assert_called_once()
        mock_diff.assert_called_once()


@patch("trenddit_command.cli.configure.load_config")
@patch("trenddit_command.cli.utils.get_provider_instance")
@patch("trenddit_command.cli.markdown.file_select_paginate")
@patch("trenddit_command.cli.markdown.parse_markdown_sections")
@patch("trenddit_command.cli.markdown.intent_select_paginate")
@patch("trenddit_command.cli.click.confirm")
@patch("trenddit_command.cli.markdown.update_markdown_with_response")
def test_intents_existing_response(
    mock_update,
    mock_confirm,
    mock_intent_select,
    mock_parse,
    mock_file_select,
    mock_get_provider,
    mock_load_config,
    runner,
    mock_config,
    mock_provider_instance,
):
    mock_load_config.return_value = mock_config
    mock_get_provider.return_value = mock_provider_instance
    mock_file_select.return_value = "../trenddit_command-vault/Intents/intents.md"
    mock_parse.return_value = [("Intent1", "Prompt1")]
    mock_intent_select.return_value = ("Intent1", "Prompt1")
    mock_confirm.return_value = False

    with patch("builtins.open", mock_open(read_data=b"Mock content")), patch(
        "os.path.exists", return_value=True
    ):
        result = runner.invoke(intents)
        assert result.exit_code == 0
        mock_provider_instance.ask.assert_not_called()
        assert (
            "Operation cancelled. Existing file will not be replaced." in result.output
        )


@patch("trenddit_command.cli.configure.load_config")
@patch("trenddit_command.cli.utils.get_provider_instance")
@patch("trenddit_command.cli.markdown.parse_markdown_sections")
@patch("trenddit_command.cli.markdown.diff")
def test_validate_response_file_not_found(
    mock_diff,
    mock_parse,
    mock_get_provider,
    mock_load_config,
    runner,
    mock_config,
    mock_provider_instance,
):
    mock_load_config.return_value = mock_config
    mock_get_provider.return_value = mock_provider_instance
    mock_parse.return_value = [("Intent1", "Prompt1")]

    with patch("builtins.open", mock_open(read_data="Mock content")), patch(
        "os.path.exists", side_effect=[True, False]
    ), patch("trenddit_command.cli.click.prompt", return_value=1):
        result = runner.invoke(validate, ["-d", "../trenddit_command-vault/Intents/test_doc.md"])
        assert result.exit_code == 1  # The command is exiting with code 1
    mock_provider_instance.ask.assert_not_called()


@patch("trenddit_command.cli.configure.load_config")
@patch("trenddit_command.cli.utils.get_provider_instance")
@patch("trenddit_command.cli.markdown.file_select_paginate")
@patch("trenddit_command.model_vision.images.resize_image")
@patch("trenddit_command.model_vision.images.display_image")
@patch("trenddit_command.model_vision.requests.get")
@patch("trenddit_command.cli.configure.has_vision_capability", return_value=True)
def test_vision_with_url(
    mock_has_vision,
    mock_requests_get,
    mock_display,
    mock_resize,
    mock_file_select,
    mock_get_provider,
    mock_load_config,
    runner,
    mock_config,
    mock_provider_instance,
):
    mock_load_config.return_value = mock_config
    mock_get_provider.return_value = mock_provider_instance
    mock_resize.return_value = b"resized_image_data"
    mock_requests_get.return_value.content = b"image_data"
    mock_requests_get.return_value.headers = {"content-type": "image/jpeg"}
    mock_requests_get.return_value.status_code = 200

    with patch(
        "trenddit_command.model_vision.tempfile.NamedTemporaryFile"
    ) as mock_temp_file, patch("trenddit_command.cli.os.unlink"), patch(
        "trenddit_command.cli.shutil.copyfileobj"
    ), patch(
        "builtins.open", mock_open()
    ):
        mock_temp_file.return_value.__enter__.return_value.name = "/tmp/temp_image.jpg"
        result = runner.invoke(
            vision, ["-u", "https://example.com/image.jpg", "Test prompt"]
        )
        assert result.exit_code == 0
    mock_provider_instance.stream_vision_response.assert_called_once()
    mock_requests_get.assert_called_with("https://example.com/image.jpg", stream=True)


@patch("trenddit_command.cli.configure.load_config")
@patch("trenddit_command.cli.utils.get_provider_instance")
@patch("trenddit_command.cli.markdown.file_select_paginate")
def test_refer_no_file_selected(
    mock_file_select,
    mock_get_provider,
    mock_load_config,
    runner,
    mock_config,
    mock_provider_instance,
):
    mock_load_config.return_value = mock_config
    mock_get_provider.return_value = mock_provider_instance
    mock_file_select.return_value = None

    result = runner.invoke(refer, ["section"])
    assert result.exit_code == 0
    assert "No file selected. Exiting." in result.output


@patch("trenddit_command.cli.configure.load_config")
@patch("trenddit_command.cli.utils.get_provider_instance")
@patch("trenddit_command.cli.markdown.file_select_paginate")
@patch("trenddit_command.cli.markdown.parse_markdown_sections")
@patch("trenddit_command.cli.markdown.intent_select_paginate")
def test_intents_no_intent_selected(
    mock_intent_select,
    mock_parse,
    mock_file_select,
    mock_get_provider,
    mock_load_config,
    runner,
    mock_config,
    mock_provider_instance,
):
    mock_load_config.return_value = mock_config
    mock_get_provider.return_value = mock_provider_instance
    mock_file_select.return_value = "../trenddit_command-vault/Intents/intents.md"
    mock_parse.return_value = [("Intent1", "Prompt1")]
    mock_intent_select.return_value = None

    with patch("builtins.open", mock_open(read_data="Mock content")):
        result = runner.invoke(intents)
        assert result.exit_code == 0
        assert "No intent selected. Exiting." in result.output


@patch("trenddit_command.cli.configure.load_config")
@patch("trenddit_command.cli.markdown.merge_docs")
def test_merge_file_not_found(mock_merge, mock_load_config, runner, mock_config):
    mock_load_config.return_value = mock_config
    mock_merge.side_effect = FileNotFoundError("File not found")

    result = runner.invoke(merge, ["non_existent_file.md"])
    assert result.exit_code != 0
    assert "File not found" in str(result.exception)


@patch("trenddit_command.cli.configure.load_config")
@patch("trenddit_command.cli.utils.get_provider_instance")
def test_id_default_section(
    mock_get_provider, mock_load_config, runner, mock_config, mock_provider_instance
):
    mock_load_config.return_value = mock_config
    mock_get_provider.return_value = mock_provider_instance

    result = runner.invoke(id)
    assert result.exit_code == 0
    mock_provider_instance.get_model_info.assert_called_once()
    mock_provider_instance.set_model_config.assert_called_with("ask")


@patch("trenddit_command.cli.configure.edit_config")
def test_config(mock_edit_config, runner):
    result = runner.invoke(config, ["key1", "key2", "value"])
    assert result.exit_code == 0
    mock_edit_config.assert_called_once_with(["key1", "key2"], "value")


@patch("trenddit_command.cli.gather_utils.article")
def test_gather(mock_article, runner):
    result = runner.invoke(gather, ["article", "https://example.com"])
    assert result.exit_code == 0
    mock_article.assert_called_once_with("https://example.com")


@patch("trenddit_command.cli.gather_utils.article")
def test_gather_invalid_type(mock_article, runner):
    result = runner.invoke(gather, ["invalid_type", "https://example.com"])
    assert result.exit_code == 0
    assert "Invalid type: invalid_type" in result.output
    mock_article.assert_not_called()


@patch("trenddit_command.cli.markdown.split_text_by_tokens")
def test_split(mock_split, runner):
    result = runner.invoke(split, ["../trenddit_command-vault/Raw/file.txt"])
    assert result.exit_code == 0
    mock_split.assert_called_once_with("../trenddit_command-vault/Raw/file.txt")


@patch("trenddit_command.cli.metrics.read_yaml_files")
@patch("trenddit_command.cli.metrics.process_data")
@patch("trenddit_command.cli.metrics.display_trends")
def test_trends(mock_display, mock_process, mock_read, runner):
    mock_read.return_value = {"mock": "data"}
    mock_process.return_value = {"processed": "data"}

    result = runner.invoke(trends, ["--days", "5"])
    assert result.exit_code == 0
    mock_read.assert_called_once()
    mock_process.assert_called_once_with({"mock": "data"}, 5)
    mock_display.assert_called_once_with({"processed": "data"})


if __name__ == "__main__":
    pytest.main([__file__])

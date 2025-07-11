# Copyright 2024 and beyond, Trenddit. All Rights Reserved.
# https://www.trenddit.com/
# This code is Apache-2.0 licensed. Please see the LICENSE file in our repository for the full license text.
# You may use this code under the terms of the Apache-2.0 license.
# This code is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.

from unittest.mock import Mock, mock_open, patch

import pytest

from trenddit_command.gather import article, article_scrape


@pytest.fixture
def mock_progress():
    return Mock()


@pytest.fixture
def mock_task_id():
    return Mock()


@pytest.fixture
def mock_config():
    return {
        "gather": {
            "user-agent": "TestAgent",
            "user-website": "test.com",
            "user-email": "test@example.com",
            "save-folder": "/test/folder",
        }
    }


@patch("trenddit_command.gather.RobotExclusionRulesParser")
def test_article_scrape_robots_disallowed(mock_rerp, mock_progress, mock_task_id):
    mock_rerp.return_value.is_allowed.return_value = False

    result = article_scrape(
        "http://example.com",
        mock_progress,
        mock_task_id,
        "/test/folder",
        "TestUserAgent",
    )

    assert result is None
    mock_progress.update.assert_called_with(
        mock_task_id, description="Scraping not allowed", completed=100
    )


@patch("trenddit_command.gather.requests.Session")
@patch("trenddit_command.gather.RobotExclusionRulesParser")
def test_article_scrape_request_exception(
    mock_rerp, mock_session, mock_progress, mock_task_id
):
    mock_rerp.return_value.is_allowed.return_value = True
    mock_session.return_value.get.side_effect = Exception("Connection error")

    with pytest.raises(Exception):
        article_scrape(
            "http://example.com",
            mock_progress,
            mock_task_id,
            "/test/folder",
            "TestUserAgent",
        )


@patch("trenddit_command.gather.configure.load_config")
@patch("trenddit_command.gather.article_scrape")
def test_article_function_failure(mock_article_scrape, mock_load_config, mock_config):
    mock_load_config.return_value = mock_config
    mock_article_scrape.return_value = None

    result = article("http://example.com")

    assert result is None


@patch("trenddit_command.gather.requests.Session")
@patch("trenddit_command.gather.RobotExclusionRulesParser")
@patch("trenddit_command.gather.BeautifulSoup")
@patch("trenddit_command.gather.Document")
@patch("trenddit_command.gather.html2text.HTML2Text")
@patch("trenddit_command.gather.os.path.exists")
@patch("trenddit_command.gather.os.makedirs")
@patch("builtins.open", new_callable=mock_open)
def test_article_scrape_no_title(
    mock_open,
    mock_makedirs,
    mock_exists,
    mock_html2text,
    mock_document,
    mock_bs,
    mock_rerp,
    mock_session,
    mock_progress,
    mock_task_id,
):
    mock_exists.return_value = False
    mock_rerp.return_value.is_allowed.return_value = True

    mock_response = Mock()
    mock_response.text = "<html><body><p>Content</p></body></html>"
    mock_session.return_value.get.return_value = mock_response

    mock_document.return_value.summary.return_value = "<div><p>Content</p></div>"

    mock_soup = Mock()
    mock_soup.find_all.return_value = []
    mock_soup.find.return_value = None  # No title found
    mock_bs.return_value = mock_soup

    mock_html2text_instance = Mock()
    mock_html2text_instance.handle.return_value = "Content"
    mock_html2text.return_value = mock_html2text_instance

    result = article_scrape(
        "http://example.com/page",
        mock_progress,
        mock_task_id,
        "/test/folder",
        "TestUserAgent",
    )

    assert result == "/test/folder/page.md"
    mock_open.assert_called_with("/test/folder/page.md", "w", encoding="utf-8")
    mock_open().write.assert_called_once_with("Content")

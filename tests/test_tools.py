"""
Unit tests for src/tools/tools.py

These tests mock external dependencies (Tavily API, HTTP requests)
so they run fast, free, and without any API keys.
"""

from unittest.mock import patch, MagicMock


# ---------------------------------------------------------------------------
# web_search tests
# ---------------------------------------------------------------------------


class TestWebSearch:
    """Tests for the web_search tool."""

    @patch("src.tools.tools.tavily")
    def test_web_search_returns_formatted_results(self, mock_tavily):
        """web_search should format Tavily results into a readable string."""
        # Arrange — fake Tavily response
        mock_tavily.search.return_value = {
            "results": [
                {
                    "title": "AI in 2026",
                    "url": "https://example.com/ai",
                    "content": "Artificial intelligence is transforming industries worldwide with new breakthroughs.",
                },
                {
                    "title": "LLM Advances",
                    "url": "https://example.com/llm",
                    "content": "Large language models continue to improve at reasoning tasks.",
                },
            ]
        }

        # Act — import here so the mock is already in place
        from src.tools.tools import web_search

        result = web_search.invoke("AI trends 2026")

        # Assert
        assert "AI in 2026" in result
        assert "https://example.com/ai" in result
        assert "LLM Advances" in result
        assert "----" in result  # separator between results
        mock_tavily.search.assert_called_once_with(query="AI trends 2026", max_results=5)

    @patch("src.tools.tools.tavily")
    def test_web_search_handles_empty_results(self, mock_tavily):
        """web_search should handle empty results gracefully."""
        mock_tavily.search.return_value = {"results": []}

        from src.tools.tools import web_search

        result = web_search.invoke("nonexistent topic xyz123")

        assert result == ""  # no results = empty join


# ---------------------------------------------------------------------------
# scrape_url tests
# ---------------------------------------------------------------------------


class TestScrapeUrl:
    """Tests for the scrape_url tool."""

    @patch("src.tools.tools.trafilatura")
    @patch("src.tools.tools.requests")
    def test_scrape_url_extracts_content_via_trafilatura(self, mock_requests, mock_trafilatura):
        """scrape_url should use trafilatura as primary strategy."""
        # Arrange
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "<html><body><p>Long article content here</p></body></html>"
        mock_response.raise_for_status = MagicMock()
        mock_requests.get.return_value = mock_response
        mock_requests.exceptions = __import__("requests").exceptions

        # trafilatura returns good content
        mock_trafilatura.extract.return_value = "A" * 300  # > 200 chars threshold

        from src.tools.tools import scrape_url

        result = scrape_url.invoke("https://example.com/article")

        assert len(result) > 0
        mock_trafilatura.extract.assert_called_once()

    @patch("src.tools.tools.requests")
    def test_scrape_url_handles_timeout(self, mock_requests):
        """scrape_url should return friendly message on timeout."""
        import requests as real_requests

        mock_requests.get.side_effect = real_requests.exceptions.Timeout("Connection timed out")
        mock_requests.exceptions = real_requests.exceptions

        from src.tools.tools import scrape_url

        result = scrape_url.invoke("https://slow-site.com")

        assert "timed out" in result.lower()

    @patch("src.tools.tools.requests")
    def test_scrape_url_handles_http_error(self, mock_requests):
        """scrape_url should return friendly message on HTTP errors."""
        import requests as real_requests

        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = real_requests.exceptions.HTTPError("404 Not Found")
        mock_requests.get.return_value = mock_response
        mock_requests.exceptions = real_requests.exceptions

        from src.tools.tools import scrape_url

        result = scrape_url.invoke("https://example.com/missing")

        assert "http error" in result.lower() or "404" in result

    @patch("src.tools.tools.requests")
    def test_scrape_url_handles_generic_exception(self, mock_requests):
        """scrape_url should catch unexpected errors gracefully."""
        import requests as real_requests

        mock_requests.get.side_effect = ConnectionError("DNS resolution failed")
        mock_requests.exceptions = real_requests.exceptions

        from src.tools.tools import scrape_url

        result = scrape_url.invoke("https://invalid-domain.xyz")

        assert "could not scrape" in result.lower()

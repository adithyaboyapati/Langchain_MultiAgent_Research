"""
Unit tests for src/agents/agents.py

These tests verify agent construction and chain definitions
WITHOUT making any real LLM API calls.
"""

from unittest.mock import patch, MagicMock


# ---------------------------------------------------------------------------
# Agent construction tests
# ---------------------------------------------------------------------------


class TestGetLlm:
    """Tests for the get_llm() factory function."""

    def test_get_llm_uses_env_vars(self):
        """get_llm should pass env-var values to ChatOpenAI."""
        mock_llm = MagicMock()

        with patch.dict("os.environ", {
            "LLM_MODEL": "test-model",
            "OPENAI_API_KEY": "test-key",
            "LLM_BASE_URL": "https://test.api.com",
        }):
            with patch("langchain_openai.ChatOpenAI", return_value=mock_llm) as mock_chat_openai:
                # Reload the module so it picks up the patched ChatOpenAI
                import importlib
                import src.agents.agents as agents_mod
                importlib.reload(agents_mod)

                llm = agents_mod.get_llm()

                mock_chat_openai.assert_called()
                call_kwargs = mock_chat_openai.call_args[1]
                assert call_kwargs["model"] == "test-model"
                assert call_kwargs["api_key"] == "test-key"
                assert call_kwargs["base_url"] == "https://test.api.com"


class TestBuildAgents:
    """Tests for build_search_agent and build_reader_agent."""

    @patch("src.agents.agents.create_agent")
    def test_build_search_agent_passes_correct_tools(self, mock_create_agent):
        """build_search_agent should pass web_search tool to create_agent."""
        mock_create_agent.return_value = MagicMock()

        from src.agents.agents import build_search_agent, web_search

        agent = build_search_agent()

        mock_create_agent.assert_called_once()
        call_kwargs = mock_create_agent.call_args[1]
        assert web_search in call_kwargs["tools"]

    @patch("src.agents.agents.create_agent")
    def test_build_reader_agent_passes_correct_tools(self, mock_create_agent):
        """build_reader_agent should pass scrape_url tool to create_agent."""
        mock_create_agent.return_value = MagicMock()

        from src.agents.agents import build_reader_agent, scrape_url

        agent = build_reader_agent()

        mock_create_agent.assert_called_once()
        call_kwargs = mock_create_agent.call_args[1]
        assert scrape_url in call_kwargs["tools"]


# ---------------------------------------------------------------------------
# Chain definition tests
# ---------------------------------------------------------------------------


class TestChains:
    """Tests for writer_chain and critic_chain."""

    def test_writer_prompt_has_required_variables(self):
        """writer_prompt should accept 'topic' and 'research' variables."""
        from src.agents.agents import writer_prompt

        input_vars = writer_prompt.input_variables
        assert "topic" in input_vars
        assert "research" in input_vars

    def test_critic_prompt_has_required_variables(self):
        """critic_prompt should accept 'report' variable."""
        from src.agents.agents import critic_prompt

        input_vars = critic_prompt.input_variables
        assert "report" in input_vars

    def test_writer_chain_is_runnable(self):
        """writer_chain should be a LangChain Runnable (has .invoke method)."""
        from src.agents.agents import writer_chain

        assert hasattr(writer_chain, "invoke")

    def test_critic_chain_is_runnable(self):
        """critic_chain should be a LangChain Runnable (has .invoke method)."""
        from src.agents.agents import critic_chain

        assert hasattr(critic_chain, "invoke")

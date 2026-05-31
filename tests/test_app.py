"""
Smoke tests for the Streamlit app.

These tests verify the app module structure without actually
starting the Streamlit server.
"""


class TestAppModule:
    """Basic smoke tests for app.py."""

    def test_app_file_exists(self):
        """The main app.py file should exist and be importable as text."""
        from pathlib import Path

        app_path = Path(__file__).parent.parent / "app.py"
        assert app_path.exists(), "app.py not found in project root"

    def test_app_contains_page_config(self):
        """app.py should configure the Streamlit page."""
        from pathlib import Path

        app_path = Path(__file__).parent.parent / "app.py"
        content = app_path.read_text()

        assert "set_page_config" in content, "app.py should call st.set_page_config()"
        assert "Multi-Agent Research Assistant" in content, "app.py should set a page title"

    def test_app_imports_agents(self):
        """app.py should import the required agent functions."""
        from pathlib import Path

        app_path = Path(__file__).parent.parent / "app.py"
        content = app_path.read_text()

        assert "build_search_agent" in content
        assert "build_reader_agent" in content
        assert "writer_chain" in content
        assert "critic_chain" in content

    def test_requirements_file_exists(self):
        """requirements.txt should exist in the project root."""
        from pathlib import Path

        req_path = Path(__file__).parent.parent / "requirements.txt"
        assert req_path.exists(), "requirements.txt not found"

    def test_dockerfile_exists(self):
        """Dockerfile should exist in the project root."""
        from pathlib import Path

        dockerfile_path = Path(__file__).parent.parent / "Dockerfile"
        assert dockerfile_path.exists(), "Dockerfile not found"

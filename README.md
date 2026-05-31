# LangChain Multi-Agent Research System

A powerful multi-agent research system built with LangChain that autonomously researches topics, gathers information, writes comprehensive reports, and evaluates their quality using AI-powered agents.

<p align="center">
  <strong>🔬 Research Automation • 🤖 Multi-Agent Orchestration • 📝 Intelligent Report Generation</strong>
</p>

---

## 🌟 Features

- **Multi-Agent Architecture**: Specialized agents for searching, reading, writing, and critiquing
- **Automated Web Research**: Intelligent web search with Tavily API
- **Smart Content Extraction**: Advanced web scraping with multiple fallback strategies
- **AI-Powered Report Generation**: Automatically generates structured research reports
- **Quality Evaluation**: Built-in critic agent for report validation and scoring
- **Interactive UI**: Streamlit-based user interface for easy interaction
- **Pipeline Orchestration**: Seamless coordination of multiple agents
- **CI/CD Pipeline**: GitHub Actions workflows for automated testing, linting, and Docker builds
- **Docker Support**: Containerized deployment with health checks
- **Comprehensive Testing**: Unit tests with pytest and coverage reporting
- **Code Quality**: Ruff linting and formatting for consistent code standards

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────┐
│           Streamlit UI (app.py)                     │
│      Multi-Agent Research Assistant Interface       │
└──────────────────┬──────────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────────┐
│      Research Pipeline (pipeline.py)                │
│        Orchestrates multi-agent workflow            │
└──────────────────┬──────────────────────────────────┘
                   │
    ┌──────────────┼──────────────┐
    │              │              │
┌───▼───┐    ┌────▼─────┐   ┌───▼────┐
│Search │    │   Reader  │   │ Writer │
│Agent  │    │   Agent   │   │ Chain  │
└───┬───┘    └────┬─────┘   └───┬────┘
    │             │             │
    │  ┌──────────▼─────────┐   │
    └─▶│  Tools Layer       │◀──┘
       │                    │
       │ • web_search      │
       │ • scrape_url      │
       │                    │
       └────────┬───────────┘
                │
            ┌───▼────────┐
            │ Critic     │
            │ Chain      │
            └────────────┘
```

### Agent Responsibilities

- **Search Agent**: Discovers relevant information across the web using Tavily
- **Reader Agent**: Extracts clean, readable content from URLs
- **Writer Chain**: Composes structured, professional research reports
- **Critic Chain**: Evaluates reports and provides improvement suggestions

---

## 🛠️ Technologies Used

| Technology | Purpose |
|-----------|---------|
| **LangChain** | Multi-agent orchestration and chain management |
| **OpenAI GPT-4o-mini** | Language model for agents and chains |
| **Streamlit** | Interactive web UI |
| **Tavily API** | Web search and information retrieval |
| **BeautifulSoup4** | HTML parsing and content extraction |
| **Trafilatura** | Web content extraction |
| **Readability-lxml** | Article content extraction |
| **Python-dotenv** | Environment configuration management |
| **Rich** | Terminal output formatting |
| **Pytest** | Testing framework with coverage reporting |
| **Ruff** | Fast Python linter and formatter |
| **Docker** | Container image building and deployment |
| **GitHub Actions** | CI/CD pipeline automation |

---

## 📋 Prerequisites

- Python 3.11 or higher
- OpenAI API Key
- Tavily API Key

---

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/LangChain-Multi-Agent-Research-System.git
cd LangChain-Multi-Agent-Research-System
```

### 2. Create Environment (Conda)

```bash
conda create -n langagent python=3.11 -y
conda activate langagent
```

Or with venv:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```bash
OPENAI_API_KEY=your_openai_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

Get your keys from:
- [OpenAI API](https://platform.openai.com/api-keys)
- [Tavily API](https://tavily.com)

---

## 💡 Usage

### Run with Streamlit UI (Recommended)

```bash
streamlit run app.py
```

Then open `http://localhost:8501` in your browser.

### Run as a Script

```bash
python main.py
```

Edit the `topic` variable in `main.py` to research different topics.

### Run with Docker

```bash
docker build -t research-agent:latest .
docker run -p 8501:8501 \
  -e OPENAI_API_KEY=your_key \
  -e TAVILY_API_KEY=your_key \
  research-agent:latest
```

Then open `http://localhost:8501` in your browser.

### Run Tests

```bash
# Run all tests with coverage
pytest tests/ --cov=src --cov-report=term-missing

# Run specific test file
pytest tests/test_agents.py -v

# Run with verbose output
pytest tests/ -v
```

### Code Quality Checks

```bash
# Lint code
ruff check .

# Format code
ruff format .

# Check formatting without applying changes
ruff format --check .
```

---

## 📁 Project Structure

```
.
├── app.py                      # Streamlit web interface
├── main.py                     # CLI entry point
├── requirements.txt            # Python dependencies
├── requirements-dev.txt        # Development dependencies (pytest, ruff)
├── pyproject.toml             # Project configuration (pytest, ruff, coverage)
├── Dockerfile                 # Container image configuration
├── .dockerignore              # Files to exclude from Docker build
├── .github/
│   └── workflows/
│       └── ci.yml             # GitHub Actions CI/CD pipeline
├── README.md                  # This file
├── LICENSE                    # License file
├── demo.excalidraw           # Architecture diagram
├── .env                       # Environment variables (not in repo)
│
├── src/
│   ├── __init__.py
│   ├── agents/
│   │   ├── __init__.py
│   │   └── agents.py          # Search, Reader, Writer, Critic agents
│   ├── tools/
│   │   ├── __init__.py
│   │   └── tools.py           # web_search, scrape_url tools
│   └── pipelines/
│       ├── __init__.py
│       └── pipeline.py        # Main research orchestration
│
└── tests/
    ├── __init__.py
    ├── test_agents.py         # Agent unit tests
    ├── test_tools.py          # Tool unit tests
    └── test_app.py            # Application integration tests
```

---

## 🔄 CI/CD Pipeline

The project includes a comprehensive GitHub Actions workflow (`ci.yml`) that automatically:

1. **Lint & Format Check** 🔍
   - Runs ruff linter to catch code issues
   - Verifies code formatting consistency
   - Fails the pipeline if violations are found

2. **Unit Tests** 🧪
   - Runs all tests in the `tests/` directory
   - Generates coverage reports
   - Only runs if linting passes

3. **Docker Build** 🐳
   - Builds the Docker image for deployment
   - Verifies the container builds successfully
   - Only runs if all tests pass

The pipeline runs automatically on:
- Every push to `main` branch
- Every pull request to `main` branch
- Path filtering ensures it only runs when relevant code changes

---

## 🔄 Workflow

1. **User Input**: Enter a research topic via UI or script
2. **Search Phase**: Search agent queries the web using Tavily
3. **Reading Phase**: Reader agent extracts content from relevant URLs
4. **Writing Phase**: Writer chain synthesizes findings into a structured report
5. **Review Phase**: Critic chain evaluates the report and provides scores
6. **Output**: Display final report with feedback and scores

---

## 📊 Example Output

The system generates reports with:
- Comprehensive introduction and background
- Key findings with detailed explanations
- Well-sourced conclusions
- Structured sections and proper formatting
- Quality scores from 1-10

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Built with [LangChain](https://langchain.com/)
- Search powered by [Tavily](https://tavily.com)
- UI built with [Streamlit](https://streamlit.io/)
- Inspired by agentic AI research patterns

---

## 📧 Support

For support, open an issue on GitHub or contact the maintainers.

**Happy Researching! 🚀**
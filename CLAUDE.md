# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Trenddit-Command** is a Python CLI tool that provides unified access to 15+ LLMs from 7 providers through a command-line interface. It integrates with markdown workflows and tools like VS Code and Obsidian.

## Development Environment Setup

### Dependencies & Package Management
- **Poetry** for dependency management: `poetry install`
- **Python 3.12+** required
- **Virtual environment**: `poetry shell` or `poetry run <command>`

### Essential Commands

#### Development Setup
```bash
# Initial setup
poetry install                    # Install all dependencies
poetry shell                     # Activate virtual environment

# Alternative: run commands without shell activation
poetry run <command>             # Run any command in poetry environment
```

#### Testing
```bash
# Run test suite
poetry run pytest                # Run all tests
poetry run pytest -v            # Verbose output
poetry run pytest --cov         # Run with coverage report
poetry run pytest tests/test_cli.py  # Run specific test file

# Application-level testing
poetry run tc test ask     # Test all providers/models
poetry run tc test vision  # Test vision models
```

#### Code Quality
```bash
# Formatting and linting
poetry run black .              # Format code
poetry run isort .              # Sort imports
poetry run pylint src/          # Lint code
```

#### Build & Distribution
```bash
# Build package
poetry build                    # Creates dist/ directory

# Local installation for testing
pip install -e .               # Install in development mode
```

## Project Architecture

### Core Design Patterns
- **Provider Pattern**: Abstract `Provider` base class with concrete implementations for each LLM provider
- **Configuration-Driven**: YAML-based configuration system (`trenddit-command.yml`)
- **Command Pattern**: CLI commands implemented using Click framework
- **Factory Pattern**: Provider factory in `utils.py` for creating provider instances

### Key Modules Structure
```
src/trenddit_command/
├── cli.py              # Main CLI entry point (Click-based)
├── provider.py         # Abstract base class for all providers
├── utils.py            # Provider factory and utility functions
├── configure.py        # Configuration management
├── model_text.py       # Text model processing
├── model_vision.py     # Vision model processing
├── providers/          # Provider implementations
│   ├── claude.py       # Anthropic Claude
│   ├── openai.py       # OpenAI GPT models
│   ├── gemini.py       # Google Gemini
│   ├── groq.py         # Groq API
│   ├── ollama.py       # Local Ollama models
│   ├── bedrock.py      # AWS Bedrock
│   └── perplexity.py   # Perplexity API
└── features/           # Feature modules
    ├── gather.py       # Web scraping
    ├── images.py       # Image generation
    ├── markdown.py     # Markdown processing
    ├── auditor.py      # Usage analytics
    └── ...
```

### Configuration System
- **Main config**: `trenddit-command.yml` in project root
- **Scaffold config**: `src/trenddit_command/scaffold/trenddit-command.yml` (default template)
- **Environment variables**: API keys stored in `~/.zshrc` or environment

#### Critical Configuration Sections
```yaml
# Model mappings (friendly names to actual model IDs)
model-mapping:
  sonnet: claude-3-5-sonnet-20240620
  gpt4o: gpt-4o
  # ...

# Provider-model associations
provider-model-mapping:
  claude: [sonnet, opus, haiku]
  openai: [gpt4o, gpt4mini, dalle3]
  # ...

# Command configurations
ask:
  provider: claude
  model: sonnet
  max-tokens: 4000
  # ...
```

## Development Guidelines

### Code Style & Principles
- **Test-Driven Development**: Write tests before implementing features
- **SOLID Principles**: Single Responsibility, Open/Closed, Liskov Substitution, Interface Segregation, Dependency Inversion
- **DRY Principles**: Reduce redundancy, improve maintainability
- **No placeholders**: Code working features, not mocks or prototypes

### Adding New Providers
1. Create provider class in `src/trenddit_command/` inheriting from `Provider`
2. Implement required methods: `get_completion()`, `get_completion_streaming()`
3. Add provider to `provider-model-mapping` in configuration
4. Add model mappings to `model-mapping` section
5. Update provider factory in `utils.py`
6. Add tests in `tests/test_<provider>.py`

### Adding New Commands
1. Add command function in `cli.py` using Click decorators
2. Add command configuration section in `trenddit-command.yml`
3. Implement command logic following existing patterns
4. Add comprehensive tests
5. Update documentation

## Testing Strategy

### Test Structure
```
tests/
├── test_cli.py          # CLI command testing
├── test_provider.py     # Provider base class
├── test_configure.py    # Configuration testing
├── test_<provider>.py   # Individual provider tests
└── fixtures/           # Test fixtures and data
```

### Test Categories
- **Unit Tests**: Individual module functionality
- **Integration Tests**: Provider API interactions
- **CLI Tests**: Command-line interface behavior
- **Configuration Tests**: YAML config validation

### Running Specific Tests
```bash
# Test specific provider
poetry run pytest tests/test_claude.py

# Test with pattern matching
poetry run pytest -k "test_claude"

# Test with coverage for specific module
poetry run pytest --cov=src/trenddit_command/claude.py tests/test_claude.py
```

## Configuration Management

### Environment Variables Required
```bash
# Add to ~/.zshrc or environment
export ANTHROPIC_API_KEY=your_key_here
export OPENAI_API_KEY=your_key_here
export GROQ_API_KEY=your_key_here
export GEMINI_API_KEY=your_key_here
export PERPLEXITY_KEY=your_key_here
# AWS credentials for Bedrock (optional)
export AWS_ACCESS_KEY_ID=your_key_here
export AWS_SECRET_ACCESS_KEY=your_key_here
```

### Configuration Commands
```bash
# View current configuration
poetry run tc id

# Change model/provider
poetry run tc config ask model sonnet
poetry run tc config ask provider claude

# Initialize configuration in new directory
poetry run tc init
```

## Entry Points & CLI Commands

### Main Entry Points (from pyproject.toml)
- `tc` - Main CLI
- `ask` - Quick prompting
- `refer` - Content referencing
- `image` - Image generation

### Command Categories
1. **Core Commands**: `ask`, `image`, `refer`, `intents`
2. **Configuration**: `id`, `config`, `init`
3. **Content Management**: `gather`, `merge`, `split`
4. **Analysis**: `audit`, `test`, `trends`, `validate`
5. **Execution**: `run`, `vision`

## Common Development Workflows

### Adding a New LLM Provider
1. Create provider module: `src/trenddit_command/new_provider.py`
2. Implement Provider interface
3. Add to configuration mappings
4. Write comprehensive tests
5. Update documentation

### Debugging Provider Issues
1. Check API key configuration
2. Test provider directly: `poetry run tc test ask`
3. Check model mappings in configuration
4. Review provider-specific error handling

### Performance Testing
```bash
# Test all providers/models
poetry run tc test ask
poetry run tc test vision

# View performance trends
poetry run tc trends --days 7
```

## Error Handling Patterns

### Provider Error Handling
- Use try/catch blocks for API calls
- Implement retry logic for transient failures
- Provide meaningful error messages
- Log errors for debugging

### Configuration Validation
- Validate YAML structure on load
- Check required fields are present
- Validate model-provider combinations
- Provide clear error messages for misconfigurations

## Documentation & Content Structure

### Scaffold System
The project uses a scaffold system for organizing generated content:
- `Prompts/` - Template prompts
- `Intents/` - Intent-based workflows
- `Code/` - Generated applications
- `Gather/` - Web scraped content
- `Images/` - Generated images
- `Embeds/` - Generated content embeds
- `Metrics/` - Performance data

### Markdown Integration
- Supports markdown-first workflows
- Integrates with VS Code and Obsidian
- Processes markdown with frontmatter
- Supports embedded code execution

## Performance Considerations

### Streaming Support
- All providers support streaming responses
- Uses Rich library for terminal formatting
- Implements proper async handling

### Context Management
- Model context limits defined in configuration
- Automatic content chunking for large inputs
- Smart context preservation across interactions

## Security & Privacy

### API Key Management
- Never commit API keys to repository
- Use environment variables for keys
- Support for local models (Ollama) for privacy
- Configurable provider selection

### Content Handling
- User controls data flow and storage
- Support for local-only workflows
- Audit trail of all operations
- Configurable content saving
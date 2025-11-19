# Cursor Rules for Adventure Agent

This directory contains comprehensive cursor rules for the Adventure Agent project. These rules help maintain consistency and guide development patterns.

## Rule Files

1. **01-project-overview.mdc** - Project architecture, key components, and entry points
2. **02-code-style.mdc** - Python code style, naming conventions, and import organization
3. **03-agent-patterns.mdc** - Agent development patterns and best practices
4. **04-langgraph-patterns.mdc** - LangGraph-specific patterns for graph construction and routing
5. **05-state-management.mdc** - State schema patterns and state access/update patterns
6. **06-tools-patterns.mdc** - Tool definition and usage patterns
7. **07-testing-patterns.mdc** - Testing structure, async testing, and mocking patterns
8. **08-configuration.mdc** - Environment variables and configuration management
9. **09-structured-output.mdc** - Pydantic models and structured LLM output patterns
10. **10-error-handling.mdc** - Error handling patterns for nodes, tools, and retry policies
11. **11-development-workflow.mdc** - Development setup, commands, and workflow

## Quick Reference

### Key Technologies
- **LangGraph**: Multi-agent orchestration
- **LangChain**: LLM integrations and tools
- **Pydantic**: Structured output and validation
- **OpenAI**: Default LLM provider
- **uv**: Package management
- **Ruff**: Linting and formatting
- **MyPy**: Type checking
- **Pytest**: Testing framework

### Common Commands
```bash
# Development
./run.sh dev              # Start dev server
./run.sh test             # Run tests
./run.sh lint             # Run linting
./run.sh typecheck        # Run type checking

# Setup
uv venv                   # Create virtual environment
uv pip install -e .       # Install dependencies
```

### Key Patterns
- All agents follow consistent initialization and method patterns
- Graph nodes are async functions returning Dict[str, Any]
- State uses TypedDict for type safety
- Tools use @tool decorator and return JSON strings
- Error handling accumulates errors in state.errors list
- Structured output uses Pydantic models with with_structured_output()

## Usage

These rules are automatically loaded by Cursor when working in this repository. They provide context-aware suggestions and help maintain consistency across the codebase.


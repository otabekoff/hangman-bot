# Contributing to Hangman Bot

First off, thank you for considering contributing to Hangman Bot! It's people like you that make this project better for everyone.

## Code of Conduct

This project and everyone participating in it is governed by our [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code. Please report unacceptable behavior to the project maintainers.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the existing issues to avoid duplicates. When you create a bug report, include as many details as possible:

* **Use a clear and descriptive title**
* **Describe the exact steps to reproduce the problem**
* **Provide specific examples** (screenshots, code snippets, etc.)
* **Describe the behavior you observed and what you expected**
* **Include details about your configuration and environment**

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, include:

* **Use a clear and descriptive title**
* **Provide a detailed description of the proposed enhancement**
* **Explain why this enhancement would be useful**
* **List any examples of similar features in other projects**

### Adding New Languages

To add support for a new language:

1. Add translations to the `TRANSLATIONS` dictionary in `hangman-bot.py`
2. Create a keyboard layout (if the language requires special characters)
3. Create a CSV file `words-{language_code}.csv` with word database
4. Update the language selection buttons in the code
5. Update README.md to reflect the new language support

**CSV Format for Words:**
```csv
word,category
EXAMPLE,Animals
TEST,Food
```

### Pull Requests

The process for submitting pull requests:

1. **Fork the repository** and create your branch from `main`
2. **Follow the coding style** of the project (PEP 8 for Python)
3. **Update documentation** if you're adding/changing features
4. **Test your changes thoroughly**
5. **Write clear commit messages**
6. **Open a Pull Request** with a clear description of changes

#### Pull Request Guidelines:

* Keep pull requests focused on a single feature or fix
* Include relevant issue numbers in the PR description
* Update tests if applicable
* Ensure your code passes all existing tests
* Add comments to complex logic
* Update CHANGELOG.md under "Unreleased" section

## Development Setup

1. **Clone your fork:**
   ```bash
   git clone https://github.com/YOUR-USERNAME/hangman-bot.git
   cd hangman-bot
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Create `.env` file:**
   ```
   BOT_TOKEN=your_bot_token_here
   ```

4. **Test your changes:**
   ```bash
   python hangman-bot.py
   ```

## Coding Standards

* **Python Style**: Follow PEP 8 guidelines
* **Naming Conventions**:
  - Use `snake_case` for functions and variables
  - Use `PascalCase` for class names
  - Use `UPPER_CASE` for constants
* **Comments**: Write clear, concise comments for complex logic
* **Async/Await**: Use async patterns consistently throughout
* **Error Handling**: Include proper try-except blocks where appropriate

## Testing

Before submitting your pull request:

1. Test the bot with all three languages (EN, RU, UZ)
2. Verify that all keyboard layouts work correctly
3. Test game flow: start, play, win, lose scenarios
4. Verify message cleanup at game end
5. Test with different word categories

## Documentation

When adding new features:

* Update README.md with usage instructions
* Add comments to your code
* Update CHANGELOG.md
* Update TODOs.md if introducing new ideas for future work

## Project Structure

```
hangman-bot/
├── hangman-bot.py          # Main bot application
├── words-en.csv            # English word database
├── words-ru.csv            # Russian word database
├── words-uz.csv            # Uzbek word database
├── images/                 # Hangman progression images
├── .env                    # Environment variables (not in repo)
├── requirements.txt        # Python dependencies
└── README.md              # Project documentation
```

## Questions?

If you have questions about contributing, feel free to:

* Open an issue with the "question" label
* Reach out to the maintainers
* Check existing issues and pull requests

## Recognition

Contributors will be recognized in:

* README.md acknowledgments section
* CHANGELOG.md for their contributions
* GitHub's contributors page

Thank you for contributing to Hangman Bot! 🎮🎉

---

© 2025 Otabek Sadiridinov
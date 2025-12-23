# Contributing to PSG Diaspora Dataset

Thank you for your interest in contributing! This project aims to analyze the relationship between Île-de-France demographics and football talent production.

## Ways to Contribute

### 1. Data Improvements

- **Add missing players**: If you know professional footballers born in Île-de-France (1980-2006) who are not in the dataset, please open an issue with:
  - Player name
  - Date of birth
  - Birthplace (city/commune)
  - Source (Wikipedia, Transfermarkt, etc.)

- **Correct errors**: If you spot incorrect data (wrong birthplace, nationality, etc.), open an issue with the correction and source.

### 2. Code Contributions

- **Bug fixes**: Found a bug? Open an issue or submit a PR.
- **New collectors**: Want to add a new data source? See `src/collectors/` for examples.
- **Analysis improvements**: Better statistical methods, new visualizations, etc.

### 3. Documentation

- **Translations**: Help translate documentation to French or other languages.
- **Methodology review**: Suggest improvements to our research methodology.

## Development Setup

```bash
# Clone the repo
git clone https://github.com/ldiaby/psg-diaspora-dataset.git
cd psg-diaspora-dataset

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run tests
pytest tests/
```

## Code Style

- Python code follows PEP 8
- Use type hints where possible
- Document functions with docstrings
- Keep commits atomic and well-described

## Pull Request Process

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/my-feature`)
3. Make your changes
4. Run tests (`pytest tests/`)
5. Commit with a clear message
6. Push and open a PR

## Ethical Guidelines

When contributing, please remember:

- **Privacy**: Don't add personal information beyond what's publicly available
- **Accuracy**: Always cite sources for data
- **Respect**: This is about understanding patterns, not categorizing individuals
- **Transparency**: Document limitations and uncertainties

## Questions?

Open an issue or contact the maintainer.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

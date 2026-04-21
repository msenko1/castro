# The Castro Project 🏳️‍🌈

## Authors

Grace Brown

Anton de La Fuente

Taiga Ikedo

Lorena Martin

Rob Podesva

Michael Senko

Yin Lin Tan

Jonathan Wu Wong

---

## Project Description

This is a sociolinguistic fieldwork project focusing on language, sexuality, and place identity in San Francisco.

---

## Project Structure

```
downeast/
├── pyproject.toml     # Project configuration and dependencies (managed by uv)
├── uv.lock            # Locked dependency versions for reproducibility
├── README.md          # Project documentation (this file)
├── data/              # Directory for raw and processed data
├── documents/         # Directory for written reports, references, and/or papers
├── scripts/           # Directory for scripts, functions, or modules
├── analysis/          # Directory for analysis scripts and notebooks
├── outputs/           # Directory for results, figures, and tables
```

---

## Getting Started

### Requirements

* Python (managed via uv)
* uv (Python package manager)

---

### Installation

Clone the repository and set up the environment:

```
git clone https://github.com/YOUR_USERNAME/downeast.git
cd downeast
uv sync
```

This will install all required dependencies in a local virtual environment.

---

### Run Analysis

To run the main script:

```
uv run python scripts/main.py
```

---

## Reproducibility

This project uses:

* `pyproject.toml` to declare dependencies
* `uv.lock` to pin exact versions

Together, these ensure that anyone can recreate the exact computational environment.

---

## Contributing

Contributions are welcome.

---

## License

This project is licensed under the MIT License.

---

## Acknowledgements

Thank you to all!

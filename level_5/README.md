# level_5

A TensorImgPipeline project.

## Description

Tutorial Level 5

## Installation

```bash
# Install dependencies
pip install tensorimgpipeline

# Link this project to the main pipeline system
tipi add .
```

## Usage

```bash
# Run the pipeline
tipi run level_5

# Validate the pipeline configuration
tipi validate level_5

# Inspect the pipeline components
tipi inspect level_5
```

## Project Structure

```
level_5/
├── level_5/           # Main package
│   ├── __init__.py          # Registers permanences and processes
│   ├── permanences.py       # Permanence definitions
│   └── processes.py         # Process definitions
├── configs/                 # Configuration files
│   └── pipeline_config.toml # Main pipeline configuration
├── pyproject.toml          # Project metadata and dependencies
├── README.md               # This file
└── .gitignore             # Git ignore rules
```

## Permanences

- **ConfigPermanence**: Stores configuration parameters
- **DataPermanence**: Stores data throughout the pipeline

## Processes

- **LoadDataProcess**: Loads data from the data directory
- **ProcessDataProcess**: Processes the loaded data

## Configuration

Edit `configs/pipeline_config.toml` to configure permanences and processes.

## Development

```bash
# Install in development mode
uv sync

# Run tests (if you add them)
pytest tests/
```

## License

MIT
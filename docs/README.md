# Documentation for streamlit-notify

This directory contains the documentation for the streamlit-notify package.

## Building the documentation

### Requirements

To build the documentation, you'll need to install the dependencies:

```bash
pip install -e ..
pip install -r requirements.txt
```

### Building

From this directory, run:

```bash
make html
```

The generated documentation will be in the `build/html` directory.

### Viewing

To view the documentation, open `build/html/index.html` in your browser.

## Documentation Structure

- `source/`: Contains the source files for the documentation
  - `conf.py`: Configuration file for Sphinx
  - `index.rst`: Main index file
  - `api/`: API documentation
  - `_static/`: Static files (CSS, images, etc.)
  - `_templates/`: Custom templates

## Read the Docs

This documentation is set up to be built automatically on Read the Docs when changes are pushed to the repository.

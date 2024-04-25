# Miaul: Markdown In-browser Automatic Loader

Miaul is a tool that enables you to watch a Markdown file and view it in HTML format in your browser with hot reload functionality.

## Installation

1. Clone the Miaul repository:

```bash
$ git clone https://github.com/eduardosilva/miaul \
    cd miaul
```

2. Install the required dependencies:

```bash
pip install -r requirements.txt
```
## Usage

To use Miaul, simply run the miaul.py script with the path to your Markdown file as an argument. You can also specify the verbosity level of logging output using the `-v` or `--verbose` option.

Example:

```bash
$ python miaul.py <markdown file path>

miaul is running...

  /\_/\
 ( o.o )
  > ^ <

```

After the execution you can open your browser to access the file using `http://localhost:8000/<markdown file name>`

You can also run Miaul using Docker:

```bash
docker run -t \
    --name miaul --rm \
    -p 8000:8000 \
    -p 8765:8765 \
    -v $(pwd):/docs \
    eduardoloursilva/github-miaul python /app/miaul.py /docs/README.md
```


### Options

```bash
$ python miaul.py -h

  /\_/\
 ( o.o )
  > ^ <

usage: miaul.py [-h] [-v] markdown_file

Miaul: Markdown In-browser Automatic Loader

positional arguments:
  markdown_file  Path to the Markdown file

options:
  -h, --help     show this help message and exit
  -v, --verbose  Increase output verbosity
```

## Features

* Automatically converts Markdown to HTML.
* Provides hot reload functionally, updating the broser whenever the Markdown file is modified.
* Supports customization logging verbosity for debugging purposies

## Development

If you'd like to contribute to Miaul or customize it for your own needs, feel free to fork the repository and submit pull requests with your changes.

# iscc-cli  - Command Line Tool

[![Linux Build Status](https://img.shields.io/travis/iscc/iscc-cli.svg?label=Linux)](https://travis-ci.org/iscc/iscc-cli)
[![Windows Build Status](https://img.shields.io/appveyor/ci/titusz/iscc-cli.svg?label=Windows)](https://ci.appveyor.com/project/titusz/iscc-cli)
[![Version](https://img.shields.io/pypi/v/iscc-cli.svg)](https://pypi.python.org/pypi/iscc-cli/)

> A command line tool that creates **ISCC Codes** for digital media files based on the [reference implementation](<https://github.com/iscc/iscc-specs>).

## Table of Contents

- [Background](#background)
- [Install](#install)
- [Usage](#usage)
- [Maintainers](#maintainers)
- [Contributing](#contributing)
- [License](#license)

## Background

The **International Standard Content Code** is a proposal for an [open standard](https://en.wikipedia.org/wiki/Open_standard) for decentralized content identification. **ISCC Codes** are generated algorithmically **from the content itself** and offer many powerful features like content similarity clustering and partial integrity checks. If you want to learn more about the **ISCC** please check out https://iscc.codes.

This tool offers an easy way to generate ISCC codes from the command line. It supports content extraction via [Apache Tika](https://tika.apache.org/) and uses the [ISCC reference implementation](https://github.com/iscc/iscc-specs).

**Supported File Types**: doc, docx, epub, html, jpg, odt, pdf, png, rtf, txt, xml

## Requirements

| NOTE: Requires JAVA to be installed and on your path! |
| --- |

**iscc-cli** is tested on Linux and Windows with Python 3.5/3.6/3.7 but should also work on macOS.

This tool depends on [tika-python](<https://github.com/chrismattmann/tika-python>).  [Tika](<https://tika.apache.org/>)  is used for extracting metadata and content from media files before generating ISCC Codes. On first execution of the `iscc` command line tool it will automatically download and launch the Java Tika Server in the background (this may take some time). Consecutive runs will access the existing Tika instance. You may explicitly pre-launch the Tika server with `$ iscc init`

## Install

The ISCC command line tool is published with the package name `iscc-cli` on the [Python Package Index](https://pypi.python.org/pypi/iscc-cli) and can be installed with pip:

```console
$ pip3 install iscc-cli
```

## Usage

### Getting Help

Show help overview by calling `iscc` without any arguments:

```console
$ iscc
Usage: iscc [OPTIONS] COMMAND [ARGS]...

Options:
  --version  Show the version and exit.
  --help     Show this message and exit.

Commands:
  gen*   Generate ISCC Code for FILE.
  batch  Create ISCC Codes for all files in PATH.
  info   Show information about environment.
  init   Inititalize and check Tika server.
  sim    Estimate Similarity of ISCC Codes A & B.
```

Get help for a specific command by entering `iscc <command>`:

```console
$ iscc gen
Usage: iscc gen [OPTIONS] FILE

  Generate ISCC Code for FILE.

Options:
  -g, --guess       Guess title (first line of text).
  -t, --title TEXT  Title for Meta-ID creation.
  -e, --extra TEXT  Extra text for Meta-ID creation.
  -v, --verbose     Enables verbose mode.
  -h, --help        Show this message and exit.
```

### Generating ISCC Codes

The `gen` command generates an ISCC Code for a single file:

```console
$ iscc gen tests/demo.jpg
ISCC:CCTcjug7rM3Da-CYDfTq7Qc7Fre-CDYkLqqmQJaQk-CRAPu5NwQgAhv
```

The `gen` command is default so you can skip it and simply do `$ iscc tests/demo.jpg` 

To get a more detailed result use the `-v` (`--verbose`) option:

```console
$ iscc -v tests/demo.jpg
ISCC:CCTcjug7rM3Da-CYDfTq7Qc7Fre-CDYkLqqmQJaQk-CRAPu5NwQgAhv
Norm Title: concentrated cat
Tophash:    7a8d0c513142c45f417e761355bf71f11ad61d783cd8958ffc0712d00224a4d0
Filepath:   tests/demo.jpg
GMT:        image
```

See `iscc batch` for help on how to generate ISCC codes for multiple files at once.


### Similarity of ISCC Codes

The `sim` command computes estimated similarity of two ISCC Codes:

```console
$ iscc sim CCUcKwdQc1jUM CCjMmrCsKWu1D
Estimated Similarity of Meta-ID: 87.50 %
```

You may also compare full four-component ISCC Codes.


## Maintainers

[@titusz](https://github.com/titusz)

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

You may also want join our developer chat on Telegram at <https://t.me/iscc_dev>.

## Change Log

### [0.4.0] - 2019-06-03

- Added support for html, odt, txt, xml
- Added optional guessing of title (first line of text)
- Added new info command
- Fixed wrong detection of identical Instance-ID

### [0.3.0] - 2019-06-01

- Add `sim` command similarity comparison of ISCC Codes

### [0.2.0] - 2019-05-31

- Add support for doc, docx and rtf documents
- Update to ISCC 1.0.4 (fixes whitespace bug)


### [0.1.0] - 2019-05-31

- Basic ISCC Code creation
- Supported file types: jpg, png, pdf, epub

## License

MIT © 2019 Titusz Pan


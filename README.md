# iscc-cli  - Command Line Tool

[![Linux Build Status](https://img.shields.io/travis/iscc/iscc-cli.svg?label=Linux)](https://travis-ci.org/iscc/iscc-cli)
[![Windows Build Status](https://img.shields.io/appveyor/ci/titusz/iscc-cli.svg?label=Windows)](https://ci.appveyor.com/project/titusz/iscc-cli)

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

## Requirements

| NOTE: Requires JAVA to be installed and on your path! |
| --- |

**iscc-cli** is tested on Linux and Windows with Python 3.5/3.6/3.7.

This tool depends on [tika-python](<https://github.com/chrismattmann/tika-python>).  [Tika](<https://tika.apache.org/>)  is used for extracting metadata and content from media files before generating ISCC Codes. On first execution of the `iscc` command line tool it will automatically download and launch the Java Tika Server in the background (this may take some time). Consecutive runs will access the existing Tika instance. You may explicitly pre-launch the Tika server with `$ iscc init`

## Install

The ISCC command line tool is published with the package name `iscc-cli` on the [Python Package Index](https://pypi.python.org/pypi/iscc-cli) and can be installed with pip:

```console
$ pip3 install iscc-cli
```

## Usage

Show help by calling `iscc` without any arguments:

```console
$ iscc
Usage: iscc [OPTIONS] COMMAND [ARGS]...

Options:
  --version  Show the version and exit.
  --help     Show this message and exit.

Commands:
  gen*   Generate ISCC Code for a single media file.
  batch  Generate ISCC Codes for multiple files.
  init   Inititalize and check Tika server.
```

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

Get help for a specific command:

```console
$ iscc batch --help
Usage: iscc batch [OPTIONS] PATH

  Batch create ISCC Codes.

  Generates ISCC Codes for all media files in <PATH>.

Options:
  -r, --recursive  Recurse into subdirectories.
  --help           Show this message and exit.

```

## Maintainers

[@titusz](https://github.com/titusz)

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

MIT © 2019 Titusz Pan


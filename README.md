# iscc-cli  - Command Line Tool

[![Linux Build Status](https://img.shields.io/travis/iscc/iscc-cli.svg?label=Linux)](https://travis-ci.org/iscc/iscc-cli)
[![Windows Build Status](https://img.shields.io/appveyor/ci/titusz/iscc-cli.svg?label=Windows)](https://ci.appveyor.com/project/titusz/iscc-cli)
[![Version](https://img.shields.io/pypi/v/iscc-cli.svg)](https://pypi.python.org/pypi/iscc-cli/)
[![Downloads](https://pepy.tech/badge/iscc-cli)](https://pepy.tech/project/iscc-cli)

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


### Supported Media File Types

#### Text

doc, docx, epub, html, odt, pdf, rtf, txt, xml, ibooks, md, xls, mobi ...


#### Image

gif, jpg, png, tif, bmp, psd, eps ...

**Note**: EPS (postscript) support requires [Ghostscript](https://www.ghostscript.com/download.html) to be installed on your system and available on your PATH. (Make sure you can run `gs` from your command line.)


#### Audio

aif, mp3, ogg, wav ...


**Note**: Support for the Audio-ID is experimentel and not yet part of the [specification](https://iscc.codes/specification/)


#### Video

3gp, 3g2, asf, avi, flv, gif, mpg, mp4, mkv, mov, ogv, webm, wmv ...


**Note**: Support for the Video-ID is experimentel and not yet part of the [specification](https://iscc.codes/specification/)

## Requirements

| NOTE: Requires JAVA to be installed and on your path! |
| --- |

**iscc-cli** is tested on Linux and Windows with Python 3.6/3.7/3.8 but should also work on macOS.

This tool depends on [tika-python](https://github.com/chrismattmann/tika-python).  [Tika](https://tika.apache.org/) is used for extracting metadata and content from media files before generating ISCC Codes. On first execution of the `iscc` command line tool it will automatically download and launch the Java Tika Server in the background (this may take some time). Consecutive runs will access the existing Tika instance. You may explicitly pre-launch the Tika server with `$ iscc init`

## Install

The ISCC command line tool is published with the package name `iscc-cli` on the [Python Package Index](https://pypi.python.org/pypi/iscc-cli) and can be installed with pip:

```console
$ pip3 install iscc-cli
```

Self-contained Windows binary executables are available for download at:
<https://github.com/iscc/iscc-cli/releases/>

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
  dump   Dump Tika extraction results for PATH (file or url path).
  info   Show information about environment.
  init   Inititalize and check environment.
  sim    Estimate Similarity of ISCC Codes A & B.
  test   Test conformance with latest reference data.
  web    Generate ISCC Code from URL.
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

#### For local files

The `gen` command generates an ISCC Code for a single file:

```console
$ iscc gen tests/image/demo.jpg
ISCC:CC1GG3hSxtbWU-CYDfTq7Qc7Fre-CDYkLqqmQJaQk-CRAPu5NwQgAhv
```

The `gen` command is default so you can skip it and simply do `$ iscc tests/demo.jpg`

To get a more detailed result use the `-v` (`--verbose`) option:

```console
$ iscc -v tests/image/demo.jpg
ISCC:CC1GG3hSxtbWU-CYDfTq7Qc7Fre-CDYkLqqmQJaQk-CRAPu5NwQgAhv
Norm Title: concentrated cat
Tophash:    7a8d0c513142c45f417e761355bf71f11ad61d783cd8958ffc0712d00224a4d0
Filepath:   tests/image/demo.jpg
GMT:        image
```

See `iscc batch` for help on how to generate ISCC codes for multiple files at once.

#### For web urls

The `web` command allows you to create ISCC codes from URLs:

```console
$ iscc web https://iscc.foundation/news/images/lib-arch-ottawa.jpg
ISCC:CCbUCUSqQpyJo-CYaHPGcucqwe3-CDt4nQptEGP6M-CRestDoG7xZFy
```

YouTube URLs will be auto-detected to create ISCC Video-IDs:

```console
$ iscc web -v https://www.youtube.com/watch?v=yJY-aLoEqDo
Norm Title: anokato kali spiral sessions
Tophash:    312554214e3d17e8aafc0d0bc54382b5b4c1b2ce0fa20d7bde1ff12aa34e911b
Filepath:   https://www.youtube.com/watch?v=yJY-aLoEqDo
GMT:        video
```

### Similarity of ISCC Codes

The `sim` command computes estimated similarity of two ISCC Codes:

```console
$ iscc sim CCUcKwdQc1jUM CCjMmrCsKWu1D
Estimated Similarity of Meta-ID: 87.50 %
```

You may also compare full four-component ISCC Codes.

### Using from your python code

While this package is not built to be used as a library, some of the high level commands to generate ISCC Codes are exposed as vanilla python functions:

```python
from iscc_cli import lib
from pprint import pprint

pprint(lib.iscc_from_url("https://iscc.foundation/news/images/lib-arch-ottawa.jpg"))

{'gmt': 'image',
 'iscc': 'CCbUCUSqQpyJo-CYaHPGcucqwe3-CDt4nQptEGP6M-CRestDoG7xZFy',
 'norm_title': 'library and archives canada ottawa',
 'tophash': 'e264cc07209bfaecc291f97c7f8765229ce4c1d36ac6901c477e05b2422eea3e'}
```

## Maintainers

[@titusz](https://github.com/titusz)

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

You may also want join our developer chat on Telegram at <https://t.me/iscc_dev>.

## Change Log

### [0.9.7] - 2020-05-01
- Add support for flac and opus audio formats
- Update dependencies

### [0.9.6] - 2020-04-24
- Support urls with dump command
- Updated tika 1.24 and fpcalc 1.50
- Use filename for meta-id as last resort
- Switch to signed audio fingerprint (breaking change)
- Bugfixes and stability improvements

### [0.9.5] - 2020-03-02
- Support mobi7
- Support mobi print replica
- Support mobi with web command

### [0.9.4] - 2020-03-02
- Add experimental support for mobi files

### [0.9.3] - 2020-02-18
- Add support for XHTML
- Fix error on unsupported media types

### [0.9.2] - 2020-01-30
- Add support for bmp, psd, xls, xlsx
- Add tika server live testing
- Fix error with title guess on image files

### [0.9.1] - 2020-01-05
- Fix issue with APP_DIR creation

### [0.9.0] - 2020-01-05
- Add experimental support for Video-ID
- Add special handling of YouTube URLs
- Add support for more Media Types (try & error)
- Add support for Python 3.8
- Remove support for Python 3.5

### [0.8.2] - 2019-12-22
- Add new `test` command for confromance testing
- Add support for .md (Markdown) files
- Update to ISCC v1.0.5
- Update to Apache Tika 1.23
- Fix issue with non-conformant Meta-ID

### [0.8.1] - 2019-12-13
- Add support for tif files
- Add support for eps files
- Set application directory to non-roaming path

### [0.8.0] - 2019-11-23
- Add new `dump` command (dumps extraction results)
- Add support for iBooks files
- Fix error with tika 1.22 dependency
- Store tika server in non-volatile storage

### [0.7.0] - 2019-09-12
- Expose commands as python API
- Fix title guessing bug

### [0.6.0] - 2019-06-11

- Added new `web` command (creates ISCC Codes for URLs)

### [0.5.0] - 2019-06-06

- Added experimental support for aif, mp3, ogg, wav
- More verbose batch output
- Fix batch output default Meta-ID

### [0.4.0] - 2019-06-03

- Added support for html, odt, txt, xml, gif
- Added optional guessing of title (first line of text)
- Added new `info` command
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

MIT © 2019-2020 Titusz Pan


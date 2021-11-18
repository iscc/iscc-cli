# iscc-cli  - Command Line Tool

[![Linux/Windows/macOS Tests](https://github.com/iscc/iscc-cli/workflows/Tests/badge.svg)](https://github.com/iscc/iscc-cli/actions?query=workflow%3ATests)
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

This tool offers an easy way to generate ISCC codes from the command line. It supports content extraction and uses the [ISCC reference implementation](https://github.com/iscc/iscc-specs).


### Supported Media File Types

3g2, 3gp, aif, aif, asf, avi, azw, azw3, azw4, bmp, doc, docx, drc, eps, epub, f4v, flac, flv, gif, h264, html, ibooks, jpeg, jpg, json, m1v, m4v, markdown, md, mkv, mobi, mov, mp3, mp4, mpeg, mpg, odt, ogg, ogg, ogv, opus, pdf, p
ng, pptx, prc, psd, rm, rtf, swf, tif, txt, vob, wav, wav, webm, wmv, xhtml, xls, xlsx, xml

## Requirements

| NOTE: Requires JAVA to be installed and on your path if you need support for text extraction! |
| --- |

**iscc-cli** is tested on Linux, Windows, and macOS with Python 3.6/3.7/3.8.

This tool depends on [tika-python](https://github.com/chrismattmann/tika-python).  [Tika](https://tika.apache.org/) is used for extracting text from documents before generating ISCC Codes. On first execution of the `iscc` command line tool it will automatically download and launch the Java Tika Server in the background (this may take some time). Consecutive runs will access the existing Tika instance. You may explicitly pre-launch the Tika server and install content extraction dependencies with `$ iscc init`

## Install

The ISCC command line tool is published with the package name `iscc-cli` on the [Python Package Index](https://pypi.python.org/pypi/iscc-cli) and can be installed with pip:

```console
$ pip3 install iscc-cli
$ iscc init
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
  --version          Show the version and exit.
  -d, --debug        Show debug output
  -g, --granular     Extract granular features
  -p, --preview      Extract asset preview
  -s, --store        Store ISCC in local index
  -u, --unpack       Unpack ISCC into components
  -st, --store_text  Store extracted text
  --help             Show this message and exit.

Commands:
  gen*     Generate ISCC Code for FILE.
  batch    Create ISCC Codes for all files in PATH.
  db       Manage ISCC database
  detect   Detect mediatype of file.
  dump     Dump Tika extraction results for PATH (file or url path).
  explain  Explain details of an ISCC code.
  info     Show information about environment.
  init     Inititalize and check environment.
  sim      Estimate Similarity of ISCC Codes A & B.
  test     Test conformance with latest reference data.
  web      Generate ISCC Code from URL.
```

Get help for a specific command by entering `iscc <command>`:

```console
$ iscc gen
Usage: iscc gen [OPTIONS] FILE

  Generate ISCC Code for FILE.

Options:
  -t, --title TEXT  Title for Meta-Code.
  -e, --extra TEXT  Extra text for Meta-Code.
  -h, --help        Show this message and exit.
```

### Generating ISCC Codes

#### For local files

The `gen` command generates an ISCC Code for a single file:

```console
$ iscc gen tests/image/demo.jpg
{
  "version": "0-0-0",
  "iscc": "KED6D635YTR5XNF6YNBTBHR4T2HGP3HKVFO7TYUP2BKVFG724W63HVI",
  "title": "Concentrated Cat",
  "filename": "demo.jpg",
  "filesize": 35393,
  "mediatype": "image/jpeg",
  "tophash": "ec87e69e73dfaf886200f90d4ba03d2f8593367543393dea8c3aa5f06422087a",
  "metahash": "9ce5052a03004657d8657167f53812718e9426d85b4cdd5106ef3d87412e6f64",
  "datahash": "55529bfae5bdb3d530c52f44d13ccd6a7c710f63620dc2db1c43c5592ae2dc97",
  "gmt": "image",
  "width": 200,
  "height": 133
}
```

The `gen` command is default so you can skip it and simply do `$ iscc tests/demo.jpg`

To get debug output use the `-d` (`--debug`) option:

```console
$ iscc -d tests/image/demo.jpg
2021-11-18 10:27:49.537 | INFO     | iscc_cli.cli:cli:69 - Debug messages activated!
2021-11-18 10:27:49.539 | DEBUG    | codetiming._timer:stop:61 - instance code creation took 0.0007s
2021-11-18 10:27:49.542 | DEBUG    | codetiming._timer:stop:61 - data code creation took 0.0019s
2021-11-18 10:27:49.560 | DEBUG    | codetiming._timer:stop:61 - content code image creation took 0.0148s
{
  "version": "0-0-0",
  "iscc": "KED6D635YTR5XNF6YNBTBHR4T2HGP3HKVFO7TYUP2BKVFG724W63HVI",
  "title": "Concentrated Cat",
  "filename": "demo.jpg",
  "filesize": 35393,
  "mediatype": "image/jpeg",
  "tophash": "ec87e69e73dfaf886200f90d4ba03d2f8593367543393dea8c3aa5f06422087a",
  "metahash": "9ce5052a03004657d8657167f53812718e9426d85b4cdd5106ef3d87412e6f64",
  "datahash": "55529bfae5bdb3d530c52f44d13ccd6a7c710f63620dc2db1c43c5592ae2dc97",
  "gmt": "image",
  "width": 200,
  "height": 133
}
```

See `iscc batch` for help on how to generate ISCC codes for multiple files at once.

#### For web urls

The `web` command allows you to create ISCC codes from URLs:

```console
$ iscc web https://iscc.foundation/news/images/lib-arch-ottawa.jpg
{
  "version": "0-0-0",
  "iscc": "KEDYT2F222OCBGQRQBD7M4HPDLUZJZAA2JO4DE76UQWNVH76MP2AK2Q",
  "title": "Library and Archives Canada, Ottawa",
  "filename": "lib-arch-ottawajpg",
  "filesize": 643177,
  "mediatype": "image/jpeg",
  "tophash": "ff5c5a115da98a89ae51cdada1c0747a0e802b3670227aefe7b18a60da984b21",
  "metahash": "4458bd689ff47d679d783e9536bcd31b261ffcb7b006a91d5194e4d520013641",
  "datahash": "2cda9ffe63f4056a72c035a8bac2286d66fcbc90d507451fe323eeb3488dcaf9",
  "gmt": "image",
  "width": 1199,
  "height": 901
}
```

### Similarity of ISCC Codes

The `sim` command computes estimated similarity of two ISCC Codes:

```console
$ iscc sim EAASS3POFKWX7KDJ EAASS2POFKWX7KDJ
Estimated Similarity of Meta-ID: 78.00 % (56 of 64 bits match)
{
  "cdist": 1
}
```

You may also compare full four-component ISCC Codes.
```console
$ iscc sim KADV5PDFXBL7HGBXFFW64KVNP6UGTUZC2CJTDBKMFYTTZPLQQVX22FI KAD3M6R7CS3367D3FFU64KVNP6UGSGETKMSM36EQI37B2Y4KEBSQLPI
Estimated Similarity of Meta-ID: 78.00 % (56 of 64 bits match)
{
  "mdist": 29,
  "cdist": 1,
  "ddist": 38,
  "imatch": false
}
```


## Maintainers

[@titusz](https://github.com/titusz)

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

You may also want join our developer chat on Telegram at <https://t.me/iscc_dev>.

## Change Log

## [1.1.0] - Unreleased
- Complete rewrite based on ISCC v1.1

### [0.9.12] - 2021-07-16
- Update to custom mediatype detection (without Tika requirement)
- Update dependencies

### [0.9.11] - 2020-06-12
- Update dependencies
- Remove support for creating ISCC codes from youtube urls

### [0.9.10] - 2020-05-19
- Fixed issue with mime-type detection
- Changed wording of similarity output
- Added CSV-compatible output for batch command
- Added debug option for batch command
- Updated dependencies

### [0.9.9] - 2020-05-18
- Fixed issue with tika & macOS
- Added macOS ci testing
- Updated dependencies

### [0.9.8] - 2020-05-13
- Updated Content-ID-Audio for robustness against transcoding (breaking change)
- Changed similarity calculation to match with web demo
- Fixed bug in mime-type detection
- Updated dependencies

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

MIT © 2019-2021 Titusz Pan


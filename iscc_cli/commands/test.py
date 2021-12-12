# -*- coding: utf-8 -*-
import io
import sys
import click
from click.exceptions import Exit
import requests
from iscc_core.conformance import selftest
import iscc
from loguru import logger as log

TEST_DATA_URL = "https://raw.githubusercontent.com/iscc/iscc-specs/version-1.1/tests/"


@click.command()
def test():
    """Test conformance with latest reference data."""
    log.remove()
    log.add(sys.stdout)
    log.info("Running iscc-core confromance tests")
    passed = selftest()
    if passed:
        log.info("iscc-core conformance tests passed")
    else:
        log.error("iscc-core conformance tests failed")
        raise Exit(1)

    log.info("Running iscc-sdk tests")
    test_data = requests.get(TEST_DATA_URL + "test_data.json").json()
    passed = True
    for funcname, tests in test_data.items():
        for testname, testdata in tests.items():
            if not testname.startswith("test_"):
                continue
            func = getattr(iscc, funcname)
            args = testdata["inputs"]
            if isinstance(args[0], str) and args[0].startswith("file"):
                r = requests.get(TEST_DATA_URL + args[0])
                args[0] = io.BytesIO(r.content)

            if funcname in ["data_chunks"]:
                testdata["outputs"] = [
                    bytes.fromhex(i.split(":")[1]) for i in testdata["outputs"]
                ]
                result = list(func(*args))
            else:
                result = func(*args)
            expected = testdata["outputs"]
            try:
                assert result == expected, "%s %s " % (funcname, args)
            except AssertionError:
                passed = False
                log.warning("FAILED %s" % testname)
                log.warning("Result %s != Expected %s" % (result, expected))
            else:
                log.info("PASSED %s" % testname)
    if passed:
        log.info("iscc-sdk tests passed")
    else:
        log.error("iscc-sdk tests failed")
        raise Exit(1)

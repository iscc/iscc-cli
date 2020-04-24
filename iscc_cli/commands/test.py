# -*- coding: utf-8 -*-
import io
import click
import requests
import iscc
from iscc_cli import const


@click.command()
def test():
    """Test conformance with latest reference data."""
    click.echo("Running confromance tests.\n")
    test_data = requests.get(const.TEST_DATA_URL + "test_data.json").json()
    for funcname, tests in test_data.items():
        if not tests["required"]:
            continue
        for testname, testdata in tests.items():
            if not testname.startswith("test_"):
                continue
            func = getattr(iscc, funcname)
            args = testdata["inputs"]
            if isinstance(args[0], str) and args[0].startswith("file"):
                r = requests.get(const.TEST_DATA_URL + args[0])
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
                click.echo("FAILED %s" % testname)
                click.echo("Result %s != Expected %s" % (result, expected))
            else:
                click.echo("PASSED %s" % testname)

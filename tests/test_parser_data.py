from parser_data import DataParser
import io
from contextlib import redirect_stdout


def test_default_parser():
    with io.StringIO() as buf, redirect_stdout(buf):
        with DataParser('zips/zip_for_test.zip') as data_parser:
            data_parser.parse(file=buf)
            with open('tests/parsed_files/output.txt', 'r') as f:
                assert f.read() == buf.getvalue()


def test_bad_situation():
    with io.StringIO() as buf, redirect_stdout(buf):
        with DataParser('zips/zip_for_test.zip',
                        file_names=['example_data_bad_status.txt', 'entity_mapping.tsv']) as data_parser:
            data_parser.parse(file=buf)
            print(buf.getvalue())
            assert "\n" == buf.getvalue()


def test_bad_entity_code():
    with io.StringIO() as buf, redirect_stdout(buf):
        with DataParser('zips/zip_for_test.zip',
                        file_names=['example_data_bad_code.txt', 'entity_mapping.tsv']) as data_parser:
            data_parser.parse(file=buf)
            print(buf.getvalue())
            assert "\n" == buf.getvalue()

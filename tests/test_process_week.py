import os
import pytest
import json

from pprint import pprint


@pytest.fixture
def week_transformer():
    from process_week import WeekTransformer
    return WeekTransformer()


def test_transform_row(week_transformer):

    with open(os.path.join(os.path.dirname(__file__), 'amo_json_2020_40.json')) as test_file:
        data = json.loads(test_file.read())

    source_row = [row for row in data if row['id'] == 26890448][0]

    result_row = week_transformer.transform_row(source_row)

    pprint(result_row)

    breakpoint()

    assert True

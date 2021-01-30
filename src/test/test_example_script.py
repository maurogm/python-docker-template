from src.main.example_script import load_parquet_dataset
from pandas.testing import assert_frame_equal

import pandas as pd


class Test_example:
    def test_load_parquet_dataset(self):
        expected = pd.DataFrame(
            {"serie": ["The Wire", "Treme", "The Deuce"], "year": [2002, 2010, 2017]}
        )

        actual = load_parquet_dataset("data")

        assert_frame_equal(expected, actual)
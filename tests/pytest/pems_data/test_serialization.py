import pandas as pd
import pyarrow as pa
import pytest

from pems_data.serialization import arrow_bytes_to_df, df_to_arrow_bytes


@pytest.fixture
def arrow_bytes(df):
    # convert df to actual arrow bytes for testing
    table = pa.Table.from_pandas(df, preserve_index=False)
    sink = pa.BufferOutputStream()
    with pa.ipc.RecordBatchStreamWriter(sink, table.schema) as writer:
        writer.write_table(table)
    return sink.getvalue().to_pybytes()


def test_arrow_bytes_to_df_with_valid_data(arrow_bytes, df):
    result = arrow_bytes_to_df(arrow_bytes)
    pd.testing.assert_frame_equal(result, df)


def test_arrow_bytes_to_df_with_none():
    result = arrow_bytes_to_df(None)
    pd.testing.assert_frame_equal(result, pd.DataFrame())


def test_arrow_bytes_to_df_with_empty_bytes():
    result = arrow_bytes_to_df(b"")
    pd.testing.assert_frame_equal(result, pd.DataFrame())


def test_df_to_arrow_bytes_serialization(df):
    result = df_to_arrow_bytes(df)

    # convert back to DataFrame to verify data integrity
    reconstructed_df = arrow_bytes_to_df(result)
    pd.testing.assert_frame_equal(reconstructed_df, df)


def test_df_to_arrow_bytes_empty_df():
    empty_df = pd.DataFrame()
    result = df_to_arrow_bytes(empty_df)

    # verify we can deserialize empty DataFrame
    reconstructed_df = arrow_bytes_to_df(result)
    pd.testing.assert_frame_equal(reconstructed_df, empty_df)


def test_df_to_arrow_bytes_preserves_dtypes(df):
    result = df_to_arrow_bytes(df)
    reconstructed_df = arrow_bytes_to_df(result)

    assert df.dtypes.equals(reconstructed_df.dtypes)

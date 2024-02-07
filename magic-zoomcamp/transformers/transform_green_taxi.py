import re

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(data, *args, **kwargs):
    """
    Template code for a transformer block.

    Add more parameters to this function if this block has multiple parent blocks.
    There should be one parameter for each output variable from each parent block.

    Args:
        data: The output from the upstream parent block
        args: The output from any additional upstream blocks (if applicable)

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    # Specify your transformation logic here
    data = data[data.passenger_count > 0]
    data = data[data.trip_distance > 0]
    data['lpep_pickup_date'] = data['lpep_pickup_datetime'].dt.date
    data.columns = data.columns.map(lambda x: re.sub('(?!^)([A-Z]+)', r'_\1', x).lower())

    return data


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """

    assert 'vendor_id' in output.columns, 'vendor_id not found'
    assert output[(output['passenger_count'] <= 0)].empty, 'Found invalid passenger count'
    assert output[(output['trip_distance'] <= 0)].empty, 'Found invalid trip distance'
    assert output is not None, 'The output is undefined'

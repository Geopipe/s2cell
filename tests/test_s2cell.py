import csv
import pathlib
import re

import pytest
import s2cell


@pytest.mark.parametrize('lat, lon, level, expected', [
    (0, 0, 0, 1152921504606846976),
    (0, 0, 30, 1152921504606846977),
    (45, 45, 30, 4635422624767557889),
    (-45, -45, 30, 13811321448941993727),
    (90, -180, 30, 5764607523034234881),
    (12.3456789, 12.3456789, 30, 1226158516923251567),
])
def test_lat_lon_to_cell_id(lat, lon, level, expected):
    cell_id = s2cell.lat_lon_to_cell_id(lat, lon, level=level)
    assert cell_id == expected

def test_invalid_lat_lon_to_cell_id():
    # Invalid level
    with pytest.raises(ValueError, match=re.escape('S2 level must be integer >= 0 and <= 30')):
        s2cell.lat_lon_to_cell_id(0, 0, level=-1)

    with pytest.raises(ValueError, match=re.escape('S2 level must be integer >= 0 and <= 30')):
        s2cell.lat_lon_to_cell_id(0, 0, level=31)

    with pytest.raises(ValueError, match=re.escape('S2 level must be integer >= 0 and <= 30')):
        s2cell.lat_lon_to_cell_id(0, 0, level='a')

def test_lat_lon_to_cell_id_compat():
    # Check against generated S2 tests
    encode_file = pathlib.Path(__file__).parent / 's2_encode_corpus.csv'
    with encode_file.open() as f:
        for row in csv.DictReader(f):
            assert s2cell.lat_lon_to_cell_id(
                float(row['lat']), float(row['lon']), int(row['level'])
            ) == int(row['cell_id'])

@pytest.mark.parametrize('lat, lon, level, expected', [
    (0, 0, 0, '1'),
    (0, 0, 30, '1000000000000001'),
    (45, 45, 30, '4054545155144101'),
    (-45, -45, 30, 'bfababaeaaebbeff'),
    (90, -180, 30, '5000000000000001'),
    (12.3456789, 12.3456789, 30, '110430acb787bb6f'),
])
def test_lat_lon_to_token(lat, lon, level, expected):
    cell_id = s2cell.lat_lon_to_token(lat, lon, level=level)
    assert cell_id == expected

def test_invalid_lat_lon_to_token():
    # Invalid level
    with pytest.raises(ValueError, match=re.escape('S2 level must be integer >= 0 and <= 30')):
        s2cell.lat_lon_to_token(0, 0, level=-1)

    with pytest.raises(ValueError, match=re.escape('S2 level must be integer >= 0 and <= 30')):
        s2cell.lat_lon_to_token(0, 0, level=31)

    with pytest.raises(ValueError, match=re.escape('S2 level must be integer >= 0 and <= 30')):
        s2cell.lat_lon_to_token(0, 0, level='a')

def test_lat_lon_to_token_compat():
    # Check against generated S2 tests
    encode_file = pathlib.Path(__file__).parent / 's2_encode_corpus.csv'
    with encode_file.open() as f:
        for row in csv.DictReader(f):
            assert s2cell.lat_lon_to_token(
                float(row['lat']), float(row['lon']), int(row['level'])
            ) == row['token']

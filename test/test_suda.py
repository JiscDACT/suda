import random
import pandas as pd
import pytest
from suda import suda, find_msu


@pytest.fixture
def data():
    persons = [
        {'gender': 'female', 'region': 'urban', 'education': 'secondary incomplete', 'labourstatus': 'employed'},
        {'gender': 'female', 'region': 'urban', 'education': 'secondary incomplete', 'labourstatus': 'employed'},
        {'gender': 'female', 'region': 'urban', 'education': 'primary incomplete', 'labourstatus': 'non-LF'},
        {'gender': 'male', 'region': 'urban', 'education': 'secondary complete', 'labourstatus': 'employed'},
        {'gender': 'female', 'region': 'rural', 'education': 'secondary complete', 'labourstatus': 'unemployed'},
        {'gender': 'male', 'region': 'urban', 'education': 'secondary complete', 'labourstatus': 'employed'},
        {'gender': 'female', 'region': 'urban', 'education': 'primary complete', 'labourstatus': 'non-LF'},
        {'gender': 'male', 'region': 'urban', 'education': 'post-secondary', 'labourstatus': 'unemployed'},
        {'gender': 'female', 'region': 'urban', 'education': 'secondary incomplete', 'labourstatus': 'non-LF'},
        {'gender': 'female', 'region': 'urban', 'education': 'secondary incomplete', 'labourstatus': 'non-LF'},
        {'gender': 'female', 'region': 'urban', 'education': 'secondary complete', 'labourstatus': 'non-LF'}
    ]
    return pd.DataFrame(persons)


@pytest.fixture
def large_data():
    return pd.read_csv('test_data.csv')


# def test_performance(large_data):
#     suda(large_data, 4)


def test_msu(data):
    groups = [['gender', 'region']]
    aggregations = {'msu': 'min', 'suda': 'sum', 'fK': 'min', 'fM': 'sum'}
    for column in data.columns:
        aggregations[column] = 'max'
    results = find_msu(data, groups=groups, aggregations=aggregations, att=4)
    results = results.fillna(0)

    assert (results.loc[0].msu == 0)
    assert (results.loc[1].msu == 0)
    assert (results.loc[2].msu == 0)
    assert(results.loc[3].msu == 0)
    assert (results.loc[4].msu == 2)
    assert (results.loc[5].msu == 0)
    assert (results.loc[6].msu == 0)
    assert(results.loc[7].msu == 0)
    assert (results.loc[8].msu == 0)
    assert (results.loc[9].msu == 0)
    assert (results.loc[10].msu == 0)


def test_suda(data):
    results = suda(data, max_msu=3)
    print(results)
    assert (results.loc[0].msu == 0)
    assert (results.loc[1].msu == 0)
    assert (results.loc[2].msu == 1)
    assert(results.loc[3].msu == 0)
    assert (results.loc[4].msu == 1)
    assert (results.loc[5].msu == 0)
    assert (results.loc[6].msu == 1)
    assert(results.loc[7].msu == 1)
    assert (results.loc[8].msu == 0)
    assert (results.loc[9].msu == 0)
    assert (results.loc[10].msu == 2)

    assert (results.loc[0].suda == 0)
    assert (results.loc[1].suda == 0)
    assert (results.loc[2].suda == 15)
    assert(results.loc[3].suda == 0)
    assert (results.loc[4].suda == 20)
    assert (results.loc[5].suda == 0)
    assert (results.loc[6].suda == 15)
    assert(results.loc[7].suda == 20)
    assert (results.loc[8].suda == 0)
    assert (results.loc[9].suda == 0)
    assert (results.loc[10].suda == 5)


def test_suda_with_columns(data):
    results = suda(data, max_msu=2, columns=['gender', 'region', 'education'])
    # check we get back columns we didn't include in SUDA calcs
    assert(results.loc[0].labourstatus == 'employed')
    assert (results.loc[0].msu == 0)
    assert (results.loc[1].msu == 0)
    assert (results.loc[2].msu == 1)
    assert(results.loc[3].msu == 0)
    assert (results.loc[4].msu == 1)
    assert (results.loc[5].msu == 0)
    assert (results.loc[6].msu == 1)
    assert(results.loc[7].msu == 1)
    assert (results.loc[8].msu == 0)
    assert (results.loc[9].msu == 0)
    assert (results.loc[10].msu == 0)

    assert (results.loc[0].suda == 0)
    assert (results.loc[1].suda == 0)
    assert (results.loc[2].suda == 4)
    assert(results.loc[3].suda == 0)
    assert (results.loc[4].suda == 4)
    assert (results.loc[5].suda == 0)
    assert (results.loc[6].suda == 4)
    assert(results.loc[7].suda == 4)
    assert (results.loc[8].suda == 0)
    assert (results.loc[9].suda == 0)
    assert (results.loc[10].suda == 0)


def test_suda_no_uniques():
    persons = [
        {'gender': 'female', 'region': 'urban', 'education': 'secondary incomplete', 'labourstatus': 'employed'},
        {'gender': 'female', 'region': 'urban', 'education': 'secondary incomplete', 'labourstatus': 'employed'},        {'gender': 'female', 'region': 'urban', 'education': 'secondary incomplete', 'labourstatus': 'employed'},
        {'gender': 'female', 'region': 'urban', 'education': 'secondary incomplete', 'labourstatus': 'employed'},
        {'gender': 'female', 'region': 'urban', 'education': 'secondary incomplete', 'labourstatus': 'employed'},
        {'gender': 'female', 'region': 'urban', 'education': 'secondary incomplete', 'labourstatus': 'employed'},
        {'gender': 'female', 'region': 'urban', 'education': 'secondary incomplete', 'labourstatus': 'employed'},
        {'gender': 'female', 'region': 'urban', 'education': 'secondary incomplete', 'labourstatus': 'employed'},
        {'gender': 'female', 'region': 'urban', 'education': 'secondary incomplete', 'labourstatus': 'employed'},
        {'gender': 'female', 'region': 'urban', 'education': 'secondary incomplete', 'labourstatus': 'employed'}
    ]
    df = pd.DataFrame(persons)
    results = suda(df, max_msu=3)
    assert(results.equals(df))
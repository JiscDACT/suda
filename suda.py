import pandas as pd
from math import factorial
from itertools import combinations


def find_msu(dataframe, groups, aggregations, att):
    """
    Find and score each Minimal Sample Unique (MSU) within the dataframe
    for the specified groups
    :param dataframe: the complete dataframe of data to score
    :param groups: an array of arrays for each group of columns to test for uniqueness
    :param aggregations: an array of aggregation methods to use for the results
    :param att: the total number of attributes (QIDs) in the dataset
    :return:
    """
    df_copy = dataframe.copy()
    # 'nple' as we may be testing a group that's a single, a tuple, triple etc
    for nple in groups:
        nple = list(nple)
        cols = nple.copy()

        # Calculate the unique value counts (fK)
        cols.append('fK')
        value_counts = df_copy[nple].value_counts()
        df_value_counts = pd.DataFrame(value_counts)
        df_value_counts = df_value_counts.reset_index()

        # Change the column names
        df_value_counts.columns = cols

        # Add values for fM, MSU and SUDA
        df_value_counts['fM'] = 0
        df_value_counts['suda'] = 0
        df_value_counts.loc[df_value_counts['fK'] == 1, 'fM'] = 1
        df_value_counts.loc[df_value_counts['fK'] == 1, 'msu'] = len(nple)
        df_value_counts.loc[df_value_counts['fK'] == 1, 'suda'] = factorial(att - len(nple))

        # Merge the results into the dataframe
        df_update = pd.merge(df_copy, df_value_counts, on=nple, how='left')
        dataframe = pd.concat([dataframe, df_update]).groupby(level=0) \
            .agg(aggregations)
    return dataframe


def suda(dataframe, max_msu, dis=0.1, columns=None):
    """
    Special Uniqueness Detection Algorithm (SUDA)
    :param dataframe:
    :param max_msu:
    :param dis:
    :param columns: the set of columns to apply SUDA to. Defaults to None (all columns)
    :return:
    """

    # Get the set of columns
    if columns is None:
        columns = dataframe.columns

    att = len(columns)

    # Construct the aggregation array
    aggregations = {'msu': 'min', 'suda': 'sum', 'fK': 'min', 'fM': 'sum'}
    for column in dataframe.columns:
        aggregations[column] = 'max'

    results = []
    for i in range(1, max_msu+1):
        groups = list(combinations(columns, i))
        results.append(find_msu(dataframe, groups, aggregations, att))

    dataframe = pd.concat(results).groupby(level=0).agg(aggregations)
    dataframe['dis-suda'] = 0
    dis_value = dis / dataframe.suda.sum()
    dataframe.loc[dataframe['suda'] > 0, 'dis-suda'] = dataframe.suda * dis_value

    dataframe = dataframe.fillna(0)
    return dataframe


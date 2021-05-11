import pandas as pd
from math import factorial
from itertools import combinations
import argparse
import os
import logging


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


def main():
    argparser = argparse.ArgumentParser(description='Special Uniques Detection Algorithm (SUDA) for Python.')
    argparser.add_argument('input_path', metavar='<input>', type=str, nargs=1, default='input.csv',
                           help='The name of the CSV data file to process')
    argparser.add_argument('output_path', metavar='<output>', type=str, nargs='?', default='output.csv',
                           help='The output file name')
    argparser.add_argument('m', metavar='<m>', type=float, nargs='?', default=0.8,
                           help='The largest minimum sample uniqueness (MSU) to test for.')
    argparser.add_argument('columns', metavar='<columns>', type=str, nargs='?', default=None,
                           help='The column to apply the algorithm to. Defaults to all columns.')
    argparser.add_argument('d', metavar='<d>', type=float, nargs='?', default=0.1,
                           help='The file-level disclosure intrusion score (DIS)')
    args = argparser.parse_args()

    # Defaults
    input_path = vars(args)['input_path'][0]
    output_path = vars(args)['output_path']
    columns = vars(args)['columns']
    param_m = vars(args)['m']
    param_dis = vars(args)['d']

    if isinstance(columns, str):
        columns = [columns]

    if not os.path.exists(input_path):
        logging.error('Input data file does not exist')
        exit()
    else:
        logging.info("Input data file: " + input_path)

    logging.info("Output file: " + output_path)

    # Load the dataset
    input_data = pd.read_csv(input_path)

    # Apply the perturbation
    output_data = suda(dataframe=input_data, max_msu=param_m, dis=param_dis, columns=columns)

    # Write the output
    output_data.to_csv(output_path, encoding='UTF-8', index=False)


if __name__ == "__main__":
    main()

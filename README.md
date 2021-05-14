# suda
Sample uniqueness scoring in Python

This is a Python library for computing sample uniques scoring using
the Special Uniques Detection Algorithm (SUDA).

The algorithm looks for rows in a dataset which are unique with
respect to a number of category fields and scores them according
to risk. 

The smaller the number of fields for which a row is unique, the 
higher the score. So a row which has a unique value for a single 
field will score highly.

The more combinations by which a row is unique the higher the score.
So a row which is unique in multiple ways will score highly.

## Usage

### Python

Call the suda() method with the dataframe to score, the maximum MSU to
test for, the DIS score for the file (defaults to 0.1) and the 
columns to use for scoring (defaults to all columns).

For example, calling:

`results = suda(data, max_msu=2)`

Will score the 'data' dataframe and find MSUs of up to two fields.
If the dataframe contained fields 'gender', 'age', 'education' and 'employment'
then the algorithm will look for rows that are unique for
all combinations of one and two fields (gender, age, education, employment,
gender & age, gender & education, gender & employment, age & education, age & employment,
education & employment.)

The output may look like:

| id| msu | suda | fK  | fM  | gender | region | education            | employment  | dis-suda |
|---| --- | ---  |---  | --- | ---    | ---    | ---                  | ---         | ---      |
| 0 | 0.0 |  0.0 | 2.0 | 0.0 | female | urban  | secondary incomplete |    employed | 0.000000 |
| 1 | 0.0 |  0.0 | 2.0 | 0.0 | female | urban  | secondary incomplete |    employed | 0.000000 |
| 2 | 1.0 | 12.0 | 1.0 | 4.0 | female | urban  | primary incomplete   |      non-LF | 0.020690 |
| 3 | 0.0 |  0.0 | 2.0 | 0.0 | male   | urban  | secondary complete   |    employed | 0.000000 |
| 4 | 1.0 | 16.0 | 1.0 | 6.0 | female | rural  | secondary complete   |  unemployed | 0.027586 |
| 5 | 0.0 |  0.0 | 2.0 | 0.0 | male   | urban  | secondary complete   |    employed | 0.000000 |

`fK` is the minimum frequency of the row - 
if this is >1 then there are no sample unique values for the row.

`fM` is the number of MSUs found for the row.

`msu` is the Minimum Sample Unique for the row - that is, the smallest number of 
fields where the row is unique.

`suda` is the SUDA calculated score, adding together the individual MSU scores 
(each MSU score is the factorial of the number of attributes in the dataset minus the MSU.)

`dis-suda` is the file-level risk score (DIS) divided by the total SUDA scores, multiplied
by SUDA for the row. In other words, the total risk distributed by the rows.

### Command line

Use the command line function to supply a CSV file for the input, a path to output
the resulting CSV, the minimum MSU, the columns to include, and the file-level risk (DIS).

## References

Elliot, M. J., Manning, A. M., & Ford, R. W. (2002). A Computational Algorithm for Handling the Special Uniques Problem. International Journal of Uncertainty, Fuzziness and Knowledge Based System , 10 (5), 493-509.

Elliot, M. J., Manning, A., Mayes, K., Gurd, J., & Bane, M. (2005). SUDA: A Program for Detecting Special Uniques. Joint UNECE/Eurostat Work Session on Statistical Data Confidentiality. Geneva.

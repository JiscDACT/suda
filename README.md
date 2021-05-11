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

## References

Elliot, M. J., Manning, A. M., & Ford, R. W. (2002). A Computational Algorithm for Handling the Special Uniques Problem. International Journal of Uncertainty, Fuzziness and Knowledge Based System , 10 (5), 493-509.

Elliot, M. J., Manning, A., Mayes, K., Gurd, J., & Bane, M. (2005). SUDA: A Program for Detecting Special Uniques. Joint UNECE/Eurostat Work Session on Statistical Data Confidentiality. Geneva.


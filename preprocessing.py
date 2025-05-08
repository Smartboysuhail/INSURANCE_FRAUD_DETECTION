import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import RandomOverSampler

class Preprocessor:
    """
        This class shall  be used to clean and transform the data before training.

        """

    def __init__(self, log_file, log_writer):
        """Initialize the preprocessor with logging configuration."""
        self.log_file = log_file
        self.log_writer = log_writer

    def remove_unwanted_spaces(self, data):
        """
                        Method Name: remove_unwanted_spaces
                        Description: This method removes the unwanted spaces from a pandas dataframe.
                        Output: A pandas DataFrame after removing the spaces.
                        On Failure: Raise Exception
                """
        self.data = data
        try:
            self.df_without_spaces = self.data.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
            return self.df_without_spaces
        except Exception as e:
            raise Exception()

    def remove_columns(self, data, columns):
        """Remove specified columns from the dataframe."""
        try:
            data = data.drop(columns=columns, axis=1)
            return data
        except Exception as e:
            raise e

    def separate_label_feature(self, data, label_column_name):
        """
                        Method Name: separate_label_feature
                        Description: This method separates the features and a Label Coulmns.
                        Output: Returns two separate Dataframes, one containing features and the other containing Labels .
                        On Failure: Raise Exception

                """
        try:
            self.X = data.drop(labels=label_column_name, axis=1)
            self.Y = data[label_column_name]
            return self.X, self.Y
        except Exception as e:
            raise Exception()

    def is_null_present(self, data):
        """Check if null values are present in the dataframe."""
        try:
            null_present = False
            cols_with_missing_values = []
            cols = data.columns
            for col in cols:
                if data[col].isnull().sum() > 0:
                    null_present = True
                    cols_with_missing_values.append(col)
            return null_present, cols_with_missing_values
        except Exception as e:
            raise e

    def impute_missing_values(self, data, cols_with_missing_values):
        """Impute missing values in the dataframe."""
        try:
            for col in cols_with_missing_values:
                if data[col].dtype == 'object':
                    data[col] = data[col].fillna(data[col].mode()[0])
                else:
                    data[col] = data[col].fillna(data[col].mean())
            return data
        except Exception as e:
            raise e

    def scale_numerical_columns(self, data):
        """Scale numerical columns in the dataframe."""
        try:
            scaler = StandardScaler()
            data = pd.DataFrame(scaler.fit_transform(data), columns=data.columns)
            return data
        except Exception as e:
            raise e

    def encode_categorical_columns(self, data):
        """Encode all categorical columns in the dataframe."""
        try:
            for column in data.columns:
                if data[column].dtype == 'object':
                    # If only two unique values, map yes/no
                    uniques = data[column].dropna().unique()
                    if set(uniques).issubset({'Y', 'N', 'YES', 'NO', 'Yes', 'No', 'yes', 'no'}):
                        data[column] = data[column].replace({'Y': 1, 'N': 0, 'YES': 1, 'NO': 0, 'Yes': 1, 'No': 0, 'yes': 1, 'no': 0})
                    else:
                        # Otherwise, use label encoding
                        data[column] = pd.factorize(data[column])[0]
            return data
        except Exception as e:
            raise e

    def handle_imbalanced_dataset(self, x, y):
        """
        Method Name: handle_imbalanced_dataset
        Description: This method handles the imbalanced dataset to make it a balanced one.
        Output: new balanced feature and target columns
        On Failure: Raise Exception
                                     """
        try:
            self.rdsmple = RandomOverSampler()
            self.x_sampled, self.y_sampled = self.rdsmple.fit_sample(x, y)
            return self.x_sampled, self.y_sampled
        except Exception as e:
            raise Exception()

    def drop_columns_with_nan(self, data):
        """Drop columns with more than 50% NaN."""
        try:
            threshold = 0.5
            data = data.loc[:, data.isnull().mean() < threshold]
            return data
        except Exception as e:
            raise e

import sys 
from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
# we have imported this beacuseit is used to create a pipeline (like firstly we are doing onehotencoding then standardscaler etc. )

from sklearn.impute import SimpleImputer
# for mmissing values

from sklearn.pipeline import Pipeline
# To make sure that i implement pipeline

from sklearn.preprocessing import OneHotEncoder,StandardScaler
# for converting categorical features into numbers

from src.exception import CustomException
from src.logger import logging
import os

from src.utils import save_object
# we are just importing the code of making pickle file from utils.py

@dataclass
# In Python, a data class is a special kind of class used to store data — it’s like a clean 
# and automatic way to define classes whose main purpose is to hold attributes, rather than behavior.
# Python will automatically create:

# The __init__ method

# __repr__ method (useful for printing)

# __eq__ method (for comparisons)

# 🧠 Why is it useful?
# Especially in machine learning projects:

# ✅ Cleaner, less boilerplate code
# No need to write repetitive __init__ methods.

# 📦 Better organization
# Keep all configuration in dedicated classes — makes your pipeline modular and organized.

# 🔍 Readability
# It becomes obvious this class is just for storing data/config — not for logic.

# ⚙️ Maintainability
# Changing default paths or adding new config fields is easy — no need to touch constructor code.

# ⚙ Why you used it specifically in your code
# In your ML pipeline, DataIngestionConfig holds:

# train_data_path

# test_data_path

# raw_data_path

# These are inputs to your pipeline: paths where data will be saved.
# By using a dataclass, you make this config:

# Reusable

# Easy to change later

# Clear for other developers (or yourself in the future)

class DataTransformationConfig:
    preprocessor_obj_file_path = os.path.join('artifacts',"preprocessor.pkl")
    # to store data in some kind of pickle file

class DataTransformation:
# this is the input that we will be giving over here
    def __init__(self):
        self.data_transformation_config=DataTransformationConfig()
    # self.data_transformation_config is inialized to DataTransfromationConfig(). This will be the first parameter in DataTransfromationConfig

    def get_data_transformer_object(self):

# This function is just to create all my pickle files, uh, which will basically be responsible in doing converting
# your categorical features into numerical or, sorry, categorical into numerical.
# If you want to probably perform standard scalar and all and all.

# basically we have divided the dataset into numerical and categorical features in EDA previously
# Now now we are doing some feature engineering or transforming numerical and categorical data
        try:
            numerical_columns = ["writing_score", "reading_score"]
            categorical_columns = [
                "gender",
                "race_ethnicity",
                "parental_level_of_education",
                "lunch",
                "test_preparation_course",
            ]

            num_pipeline= Pipeline(
                steps=[
                ("imputer",SimpleImputer(strategy="median")),
                ("scaler",StandardScaler())

                ]
            )

            # Here what we are doing is we are creating a pipiline which is doing two important things first handling missing values  with this strategy like median 
            # and second is doing standard scaling

            cat_pipeline=Pipeline(

                steps=[
                ("imputer",SimpleImputer(strategy="most_frequent")),
                ("one_hot_encoder",OneHotEncoder()),
                ("scaler",StandardScaler(with_mean=False))
                ]

            )

            # same here , creating a pipeline which will do the following things

            logging.info(f"Categorical columns: {categorical_columns}")
            logging.info(f"Numerical columns: {numerical_columns}")


            # Now to combine categorical pipeline with numerical pipeline we will be using ColumnTransformer
            preprocessor=ColumnTransformer(
                [
                ("num_pipeline",num_pipeline,numerical_columns),
                # we are giving num. pipeline and for whtat variable ? we are doing for numercial columns
                ("cat_pipelines",cat_pipeline,categorical_columns)
                # similarly for cat. pipeline 

                ]


            )

            return preprocessor
           
        except Exception as e:
            raise CustomException (e,sys)
        
    
    def initiate_data_transformation(self,train_path,test_path):
        try:

            # reading the data
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            logging.info("The train and test data completed")

            logging.info("obtaining preproccessing object")

            preprocessing_obj=self.get_data_transformer_object()
            # preprocessing means that combination of num. and cat. pipelines

            target_column_name="math_score"
            numerical_columns = ["writing_score", "reading_score"]
            
            # For train data
            input_feature_train_df = train_df.drop(columns=[target_column_name],axis=1)
            # droping target_column_name which is math score from input feature
            target_feature_train_df = train_df[target_column_name]

            # For test data
            input_feature_test_df = test_df.drop(columns=[target_column_name],axis=1)
            # droping target_column_name which is math score from input feature
            target_feature_test_df = test_df[target_column_name]

            logging.info(
                f"Applying preprocessing object on training dataframe and testing dataframe. "
            )

            # Once we have our train and test data we will take the preprocessing object and will do fit underscore transform 
            input_feature_train_arr = preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr = preprocessing_obj.transform(input_feature_test_df)

            train_arr = np.c_[
                input_feature_train_arr, np.array(target_feature_train_df)
            ]

            test_arr = np.c_[
                input_feature_test_arr, np.array(target_feature_test_df)
            ]

            logging.info(f"Saved preprocessing object.")

            # np.c_ is a convenient indexing tool provided by NumPy (numpy.c_) that allows you to concatenate arrays column-wise 
            
# 🔹 Example 1: Combine two 1D arrays into 2D (column-wise)

# import numpy as np
# a = np.array([1, 2, 3])
# b = np.array([4, 5, 6])

# result = np.c_[a, b]
# print(result)

# Output:
# [[1 4]
#  [2 5]
#  [3 6]]   

            save_object(

                file_path=self.data_transformation_config.preprocessor_obj_file_path,
                obj = preprocessing_obj

            )

            # the above func. is just used for saving the pickle file which is made using dill.dump
            # that code of making pickle file is in utils.py

            return (
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path,
            )

        except Exception as e:
            raise CustomException(e,sys)
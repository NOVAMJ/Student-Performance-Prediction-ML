## read a dataset or  
## create mongodb client 

# utils file consists of common functionalities which the entire project can use

import os
import numpy as np
import sys
import pandas as pd
from src.exception import CustomException
import dill
from sklearn.metrics import r2_score
# dill.dump an another library which helps to create a pickle file

def save_object(file_path, obj):
    try:
        dir_path = os.path.dirname(file_path)

        os.makedirs(dir_path, exist_ok=True)

        with open(file_path,"wb") as file_obj:
            dill.dump(obj, file_obj)

# we have defined the save object function over here.
# This is taking the file path and obj.
# It will basically take the file path or it will make a directory like this.

# If it already exists it is going to do it.

# Then we are going to open the file path in the right path mode.

# And we are going to do the dill dot dump.


    except Exception as e:
        raise CustomException(e,sys)
    
def evaluate_models(X_train,y_train,X_test,y_test,models,param):
    try:
        report = {}

        for i in range(len(list(models))):
            model = list(models.values())[i]
        
        # basically getting each an every model and then model.fit

            model.fit(X_train,y_train)  # Train model
            y_train_pred = model.predict(X_train)

            y_test_pred = model.predict(X_test)

            train_model_score = r2_score(y_train,y_train_pred)
            test_model_score = r2_score(y_test,y_test_pred)

            report[list(models.keys())[i]] = test_model_score

        return report

    except Exception as e:
        raise CustomException (e,sys)




    

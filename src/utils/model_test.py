'''
from src.utils.all_utils import read_yaml, create_directory, save_model, error_value, save_reports
from sklearn.model_selection import RandomizedSearchCV, train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn import linear_regression

import pytest


@pytest.fixture
def data_preparation():
    data_preprocessing()
    return split_train_test_data()


@pytest.fixture
def linear_regression_prediction(data_preparation):
    xtrain, ytrain, xtest, ytest = data_preparation
    lr = linear_regression(xtrain, ytrain)
    ypred = predict_on_test_data(lr, xtest)
    return xtest, ypred

@pytest.fixture
def k_neighbors_prediction(data_preparation):
    xtrain, ytrain, xtest, ytest = data_preparation
    knn = k_neighbours(xtrain, ytrain)
    ypred = predict_on_test_data(knn, xtest)
    return xtest, ypred

@pytest.fixture
def return_models(data_preparation):
    xtrain, ytrain, xtest, ytest = data_preparation
    lr = linear_regression(xtrain, ytrain)
    knn = k_neighbours(xtrain, ytrain)
    return [lr, knn]

'''
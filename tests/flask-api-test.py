import requests
import pandas as pd
import numpy as np
from src.utils.all_utils import read_yaml
import os

# Read the input data from the test sheet
config = read_yaml("config/config.yaml")

artifacts_dir = config["artifacts"]["artifacts_dir"]
split_data_dir = config["artifacts"]["split_data"]["split_data_dir"]
test_data_dir = config["artifacts"]["split_data"]["test_data_dir"]
test_data_file = config["artifacts"]["split_data"]["test_data_file"]

reports_dir = config["artifacts"]["reports"]["reports_dir"]
reports_file = config["artifacts"]["reports"]["reports_sheet"]

test_data_file_path = os.path.join(artifacts_dir, split_data_dir, test_data_dir, test_data_file )
output_file_path = os.path.join(artifacts_dir, reports_dir, reports_file)

input_df = pd.read_csv(filepath_or_buffer=test_data_file_path)

# Define the Flask API endpoint
endpoint = "http://127.0.0.1:5000/dem_predict"

# Create an empty list to store the predicted outputs
predicted_outputs = []

# Iterate over each row in the input CSV file
for index, row in input_df.iterrows():

    # Prepare the data as a dictionary
    data = {
        "visit": row["Visit"],
        "mr_delay": row["MR Delay"],
        "Age": row["Age"],
        "EDUC": row["EDUC"],
        "SES": row["SES"],
        "CDR": row["CDR"],
        "eTIV": row["eTIV"],
        "nWBV": row["nWBV"],
        "Gender": row["M/F_M"],
        "ASF": row["ASF"],
        "MMSE": row["MMSE"],
    }

    # Send the data to the Flask API for prediction
    response = requests.post(endpoint, data=data)

    # Extract the predicted output from the response
    predicted_output = response.text.strip()

    # Add the predicted output to the list
    predicted_outputs.append(predicted_output)

# Add the predicted outputs as a new column to the input dataframe
input_df["predicted-output"] = predicted_outputs

# Save the input dataframe with predicted outputs as a new CSV file
input_df.to_csv(path_or_buf=output_file_path, index=False)

import os
import pandas as pd

# Dynamically determine the base directory and construct the correct path to the Excel file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EXCEL_PATH = os.path.join(BASE_DIR, "assets", "Australian Shark-Incident Database Public Version.xlsx")

def load_filtered_data():
    """
    Load the data from the Excel file and filter the necessary columns.
    Returns a DataFrame with the selected columns.
    """
    # List of required columns
    required_columns = [
        "Incident.month", "Incident.year", "State", "Location", "Latitude", "Longitude",
        "Shark.common.name", "Shark.scientific.name", "Shark.length.m", "Provoked/unprovoked",
        "Victim.activity", "Shark.behaviour", "Injury.location", "Victim.gender", "Victim.age",
        "Time.of.incident"
    ]

    try:
        # Load the Excel file
        data = pd.read_excel(EXCEL_PATH)
        
        # Filter the necessary columns
        filtered_data = data[required_columns]

        return filtered_data

    except FileNotFoundError as e:
        raise FileNotFoundError(f"Excel file not found at path: {EXCEL_PATH}") from e
    except KeyError as e:
        raise KeyError(f"One or more required columns are missing in the Excel file: {required_columns}") from e

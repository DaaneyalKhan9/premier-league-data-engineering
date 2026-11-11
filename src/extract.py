
import os
import json
import requests
import pandas as pd

from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv


# API endpoint for Premier League team information
API_URL = "https://api.football-data.org/v4/competitions/PL/teams"


def fetch_teams():
    """Retrieve Premier League team data from the API."""

    # Load the API key securely from our .env file
    load_dotenv()
    api_key = os.getenv("FOOTBALL_API_KEY")

    # Stop execution if the API key is missing
    if not api_key:
        raise ValueError("FOOTBALL_API_KEY is missing")

    # Include the API key in the request headers for authentication
    headers = {"X-Auth-Token": api_key}

    # Send a GET request to retrieve data from the API
    response = requests.get(
        API_URL,
        headers=headers,
        timeout=15
    )

    # Raise an error if the API returns an unsuccessful HTTP status
    response.raise_for_status()

    # Convert the JSON response into a Python dictionary
    return response.json()


def create_dataframe(data):
    """Convert the API team records into a Pandas DataFrame."""

    # Extract the list of teams from the JSON dictionary
    teams = data["teams"]

    # Convert the list of dictionaries into rows and columns
    return pd.DataFrame(teams)


def explore_data(data, df):
    """Explore the API response and inspect the dataset."""

    # Inspect the top-level keys returned by the API
    print("\n--- API RESPONSE ---")
    print("Available keys:", list(data.keys()))

    # Display the first team record as formatted JSON
    if data["teams"]:
        print("\nFirst team:")
        print(json.dumps(data["teams"][0], indent=4))

    # Display the number of teams and DataFrame dimensions
    print("\n--- DATAFRAME OVERVIEW ---")
    print("Total teams:", len(df))
    print("Shape:", df.shape)

    # Display the available column names
    print("Columns:", df.columns.tolist())

    # Preview the first five rows of the dataset
    print("\nFirst five rows:")
    print(df.head())

    # Count missing (null) values in each column
    print("\nMissing values:")
    print(df.isnull().sum())

    # Display column data types and non-null counts
    print("\nData types:")
    df.info()


def save_raw_data(data):
    """Save the original API response as a JSON file."""

    # Define the raw data folder relative to the project root
    project_root = Path(__file__).resolve().parent.parent
    output_dir = project_root / "data" / "raw"

    # Create the folder if it doesn't already exist
    output_dir.mkdir(parents=True, exist_ok=True)

    # Generate a unique filename using the current timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"premier_league_teams_{timestamp}.json"

    # Save the original API response without modifying it
    output_path = output_dir / filename

    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

    print(f"\nRaw data saved to: {output_path}")

    return output_path


def main():
    """Run the extraction and data exploration process."""

    # Extract data from the API
    data = fetch_teams()

    # Save the original response before any transformations
    save_raw_data(data)

    # Convert the team records into a Pandas DataFrame
    teams_df = create_dataframe(data)

    # Explore the dataset
    explore_data(data, teams_df)

if __name__ == "__main__":
    main()

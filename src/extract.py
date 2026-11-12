
import os
import json
import time
import requests

from datetime import datetime, timezone
from pathlib import Path
from dotenv import load_dotenv


# ==========================================
# 1. API CONFIGURATION
# ==========================================

# Base URL for Premier League API requests
BASE_URL = "https://api.football-data.org/v4/competitions/PL"

# Datasets we want to extract
ENDPOINTS = {
    "teams": "teams",
    "matches": "matches",
    "standings": "standings",
    "scorers": "scorers",
    "competition": ""
}

# Location where raw API responses will be stored
PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"


# ==========================================
# 2. FETCH DATA FROM API
# ==========================================

def fetch_data(endpoint, api_key):
    """Retrieve JSON data from a football API endpoint."""

    # Construct the URL for the selected dataset
    url = f"{BASE_URL}/{endpoint}" if endpoint else BASE_URL

    # Authenticate the request using our API key
    headers = {
        "X-Auth-Token": api_key
    }

    # Send the HTTP GET request
    response = requests.get(
        url,
        headers=headers,
        timeout=30
    )

    # Raise an error for unsuccessful responses
    response.raise_for_status()

    # Convert the JSON response into a Python dictionary
    return response.json()


# ==========================================
# 3. SAVE RAW JSON DATA
# ==========================================

def save_raw_data(data, dataset_name):
    """Save the original API response as a JSON file."""

    # Create the raw data folder if it doesn't exist
    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

    # Generate a UTC timestamp for the filename
    timestamp = datetime.now(timezone.utc).strftime(
        "%Y%m%d_%H%M%S_%f"
    )

    # Create a filename for the selected dataset
    filename = f"premier_league_{dataset_name}_{timestamp}.json"

    # Build the complete output path
    output_path = RAW_DATA_DIR / filename

    # Save the JSON response without changing its structure
    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

    return output_path


# ==========================================
# 4. MAIN EXTRACTION PIPELINE
# ==========================================

def main():
    """Extract and save all configured football datasets."""

    # Load the API key from the .env file
    load_dotenv()
    api_key = os.getenv("FOOTBALL_API_KEY")

    # Stop the pipeline if authentication is missing
    if not api_key:
        raise ValueError("FOOTBALL_API_KEY is missing from .env")

    print("Starting Premier League data extraction...\n")

    successful = []
    failed = []

    # Loop through each configured API endpoint
    for dataset_name, endpoint in ENDPOINTS.items():

        print(f"Extracting {dataset_name}...")

        try:
            # Step 1: Retrieve the API response
            data = fetch_data(endpoint, api_key)

            # Step 2: Save the original response as JSON
            output_path = save_raw_data(data, dataset_name)

            # Step 3: Record successful extraction
            successful.append(dataset_name)

            print(f"Saved successfully: {output_path.name}\n")

        except requests.exceptions.RequestException as error:
            # Report API/network failures without stopping other datasets
            failed.append(dataset_name)
            print(f"API request failed for {dataset_name}: {error}\n")

        except OSError as error:
            # Report file-saving failures
            failed.append(dataset_name)
            print(f"Could not save {dataset_name}: {error}\n")

        # Brief pause to avoid sending requests too quickly
        time.sleep(7)

    # Display the final extraction summary
    print("\n--- EXTRACTION SUMMARY ---")
    print(f"Successful datasets: {len(successful)}")
    print(f"Failed datasets: {len(failed)}")

    if failed:
        print("Failed:", ", ".join(failed))
        raise RuntimeError("One or more datasets failed to extract")

    print("Extraction pipeline completed successfully!")


# ==========================================
# 5. SCRIPT ENTRY POINT
# ==========================================

if __name__ == "__main__":
    main()

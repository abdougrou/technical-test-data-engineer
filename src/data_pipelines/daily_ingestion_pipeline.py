import os
import csv
import requests
from datetime import datetime
from typing import Dict, List
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DailyIngestionPipeline:
    def __init__(self, base_url: str = "http://127.0.0.1:8000", data_dir = Path("data")):
        self.base_url = base_url
        self.endpoints = ["tracks", "users", "listen_history"]
        self.data_dir = data_dir
        self.setup_directories()

    def setup_directories(self):
        today = datetime.now().strftime("%Y-%m-%d")
        for endpoint in self.endpoints:
            directory = self.data_dir / endpoint / today
            directory.mkdir(parents=True, exist_ok=True)

    def fetch_data(self, endpoint: str) -> List[Dict]:
        url = f"{self.base_url}/{endpoint}"
        all_data = []
        page = 1

        while True:
            try:
                response = requests.get(url, params={"page": page, "size": 100})
                response.raise_for_status()
                data = response.json()

                if not data["items"]:
                    break
                    
                all_data.extend(data["items"])
                logging.info(f"Fetched page {page} from {endpoint}")

                page += 1

            except requests.exceptions.RequestException as e:
                logging.error(f"Error fetching data from {endpoint}: {str(e)}")
                break

        return all_data

    def save_to_csv(self, endpoint: str, data: List[Dict]):
        if not data:
            logging.warning(f"No data to save for {endpoint}")
            return

        today = datetime.now().strftime("%Y-%m-%d")
        timestamp = datetime.now().strftime("%H-%M-%S")
        filename = f"{endpoint}_{timestamp}.csv"
        filepath = self.data_dir / endpoint / today / filename

        try:
            # Get headers from the first item
            fieldnames = data[0].keys()

            with open(filepath, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                
                # Handle special case for listen_history items list
                if endpoint == "listen_history":
                    for row in data:
                        if isinstance(row["items"], list):
                            row["items"] = ",".join(map(str, row["items"]))
                        writer.writerow(row)
                else:
                    writer.writerows(data)

            logging.info(f"Saved {len(data)} records to {filepath}")
            
        except IOError as e:
            logging.error(f"Error saving data to {filepath}: {str(e)}")

    def run_pipeline(self):
        for endpoint in self.endpoints:
            logging.info(f"Starting data collection for {endpoint}")
            data = self.fetch_data(endpoint)
            if data:
                self.save_to_csv(endpoint, data)
            logging.info(f"Completed data collection for {endpoint}")

def main():
    pipeline = DailyIngestionPipeline()
    pipeline.run_pipeline()

if __name__ == "__main__":
    main()
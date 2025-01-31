from pathlib import Path
import tempfile
import shutil
from unittest.mock import patch, MagicMock
import requests
from datetime import datetime

from src.data_pipelines.daily_ingestion_pipeline import DailyIngestionPipeline

class TestDailyIngestionPipeline:
    def setup_method(self):
        # Create temporary directory for test data
        self.temp_dir = Path(tempfile.mkdtemp())
        self.pipeline = DailyIngestionPipeline(base_url="http://127.0.0.1:8000", data_dir=self.temp_dir)

    def teardown_method(self):
        # Clean up temporary directory
        shutil.rmtree(self.temp_dir)

    @patch('requests.get')
    def test_fetch_data_success(self, mock_get):
        # Test successful data fetching with pagination
        mock_responses = [
            {'items': [{'id': 1}, {'id': 2}], 'total': 4, "page": 1, "size": 2, "pages": 3},
            {'items': [{'id': 3}, {'id': 4}], 'total': 4, "page": 2, "size": 2, "pages": 3},
            {'items': [], 'total': 4, "page": 3, "size": 0, "pages": 3}
        ]
        mock_get.side_effect = [
            MagicMock(json=lambda r=response: r, status_code=200)
            for response in mock_responses
        ]

        data = self.pipeline.fetch_data('tracks')
        print(data)

        assert len(data) == 4
        assert mock_get.call_count == 3

    @patch('requests.get')
    def test_fetch_data_error_handling(self, mock_get):
        # Test error handling during data fetching
        mock_get.side_effect = requests.exceptions.RequestException()
        
        data = self.pipeline.fetch_data('tracks')
        assert data == []

    def test_directory_creation(self):
        # Test proper directory structure creation
        today = datetime.now().strftime("%Y-%m-%d")
        
        for endpoint in ['tracks', 'users', 'listen_history']:
            expected_dir = self.temp_dir / endpoint / today
            assert expected_dir.exists()

    def test_save_to_csv_special_handling(self):
        # Test special handling of listen_history items
        test_data = [{
            'user_id': 1,
            'items': [1, 2, 3],
            'created_at': '2025-01-31'
        }]
        
        self.pipeline.save_to_csv('listen_history', test_data)
        
        today = datetime.now().strftime("%Y-%m-%d")
        saved_files = list((self.temp_dir / 'listen_history' / today).glob('*.csv'))
        assert len(saved_files) == 1
        
        with open(saved_files[0]) as f:
            content = f.read()
            assert '1,2,3' in content  # Check if list was properly joined

    def test_empty_data_handling(self):
        # Test handling of empty data
        self.pipeline.save_to_csv('tracks', [])
        
        today = datetime.now().strftime("%Y-%m-%d")
        saved_files = list((self.temp_dir / 'tracks' / today).glob('*.csv'))
        assert len(saved_files) == 0
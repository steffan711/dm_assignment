import json
import logging
from collections import deque
import atexit
from data_structures import QueueDict
from event_loader import GitHubEventLoader
from event_statistics import EventStatistics
from typing import List, Dict, Optional


class Config:
    MAX_REPOSITORIES = 5
    MAX_STORED_EVENTS = 500
    MAX_EVENT_AGE_DAYS = 7


class DataManager:
    class _InnerDataManager:
        def __init__(self, file_name: str):
            self.file_name: str = file_name
            self.data: QueueDict = self._load_data()
            atexit.register(self._save_data)

        def get_events(self, repository: str) -> Optional[deque]:
            return self.data.get(repository)

        def get_statistics(self, repository: str) -> Dict[str, str]:
            """
            Calculate and return statistics for a specific repository.

            Args:
                repository (str): The name of the repository.

            Returns:
                Dict[str, str]: A dictionary of event statistics for the repository.
            """
            self._update_repository_data(repository)
            repo_data = self.get_events(repository)
            if repo_data is None:
                return {}
            return {event_type: EventStatistics.calculate_average_gap(repo_data, event_type)
                    for event_type in EventStatistics.extract_event_types(repo_data)}

        def _update_repository_data(self, repository: str) -> None:
            """
            Update the repository data with new events from GitHub.

            Args:
                repository (str): The name of the repository to update.
            """
            repo_data = self.get_events(repository)
            last_event_id = repo_data[-1]["id"] if repo_data else None

            new_events = GitHubEventLoader().fetch_events(
                repository, Config.MAX_STORED_EVENTS, Config.MAX_EVENT_AGE_DAYS, last_event_id)

            if new_events:
                self._extend_repository_data(repository, new_events)

        def _extend_repository_data(self, repository: str, new_events: List[Dict]) -> None:
            """
            Extend the repository data with new events.

            Args:
                repository (str): The name of the repository.
                new_events (List[Dict]): A list of new events to add to the repository data.
            """
            existing_repo_data = self.data.get(repository)
            if existing_repo_data is not None:
                existing_repo_data.extend(reversed(new_events))
            else:
                self.data.put(repository, deque(reversed(new_events), maxlen=Config.MAX_STORED_EVENTS))

        def _load_data(self) -> QueueDict:
            """
            Load data from a file into a QueueDict.

            Returns:
                QueueDict: A QueueDict containing the loaded data.
            """
            try:
                with open(self.file_name, 'r') as file:
                    raw_data = json.load(file)
            except (FileNotFoundError, json.JSONDecodeError) as e:
                logging.error(f"Error loading file {self.file_name}: {e}")
                return QueueDict(Config.MAX_REPOSITORIES)

            data = QueueDict(Config.MAX_REPOSITORIES)
            for repo_name, events in raw_data:
                if isinstance(events, list):
                    data.put(repo_name, deque(events, maxlen=Config.MAX_STORED_EVENTS))
                else:
                    logging.error(f"Invalid format for repository {repo_name}")

            return data

        def _save_data(self) -> None:
            """
            Save the data to a file at exit.
            """
            with open(self.file_name, 'w') as file:
                json.dump(self.data.get_serializable_list(), file)

    _instance: Optional[_InnerDataManager] = None

    def __init__(self, file_name: str = 'repository_data.json'):
        """
        Initialize the DataManager (singleton pattern). If an instance of _InnerDataManager doesn't exist,
        create one. Otherwise, update the file name of the existing instance.

        Args:
            file_name (str): The name of the file to save and load data.
        """
        if DataManager._instance is None:
            DataManager._instance = DataManager._InnerDataManager(file_name)
        else:
            DataManager._instance.file_name = file_name

    def __getattr__(self, name):
        return getattr(DataManager._instance, name)


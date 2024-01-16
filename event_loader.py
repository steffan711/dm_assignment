import logging
from datetime import datetime, timedelta
from github import Github, GithubException
from typing import Optional, List, Dict


class GitHubEventLoader:
    def __init__(self, auth_file: str = 'auth_config.txt'):
        self.auth_file: str = auth_file

    def _load_github_token(self) -> Optional[str]:
        try:
            with open(self.auth_file, 'r') as file:
                return file.read().strip()
        except FileNotFoundError:
            logging.error("Authentication configuration file not found. Continuing in anonymous mode.")
            return None

    @staticmethod
    def _convert_event_to_dict(event) -> Dict:
        return {
            "id": event.id,
            "type": event.type,
            "created_at": event.created_at.isoformat() if event.created_at else None,
        }

    def fetch_events(self, repository: str, max_events: int, max_days: int, last_event_id: Optional[str] = None) -> List[Dict]:
        """
        Fetches events for a specific GitHub repository.

        Args:
            repository (str): The name of the repository.
            max_events (int): Maximum number of events to fetch.
            max_days (int): Maximum age of events in days.
            last_event_id (Optional[str]): The ID of the last event fetched (for pagination).

        Returns:
            List[Dict]: A list of event dictionaries.
        """
        token = self._load_github_token()
        github_client = Github(token) if token else Github()

        try:
            repository = github_client.get_repo(repository)
            events = repository.get_events()

            return self._fetch_recent_events(events, max_events, max_days, last_event_id)

        except GithubException as e:
            logging.error(f"GitHub API error: {e}")
            return []

    def _fetch_recent_events(self, events, max_events: int, max_days: int, last_event_id: Optional[str]) -> List[Dict]:
        """
        Fetches recent events from a collection of GitHub events.

        Args:
            events: The collection of GitHub events.
            max_events (int): Maximum number of events to fetch.
            max_days (int): Maximum age of events in days.
            last_event_id (Optional[str]): The ID of the last event fetched (for pagination).

        Returns:
            List[Dict]: A list of recent event dictionaries.
        """
        recent_events = []
        for event in events:
            if event.id == last_event_id or len(recent_events) >= max_events:
                break

            if self._is_event_outdated(event, max_days):
                break

            recent_events.append(self._convert_event_to_dict(event))

        return recent_events

    @staticmethod
    def _is_event_outdated(event, max_days: int) -> bool:
        event_date = event.created_at
        return event_date and (datetime.utcnow() - event_date.replace(tzinfo=None)) > timedelta(days=max_days)

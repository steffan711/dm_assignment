from collections import deque
from datetime import datetime, timedelta


class EventStatistics:
    @staticmethod
    def extract_event_types(events: deque) -> set:
        """
        Extracts a set of unique event types from a deque of event dictionaries.

        Args:
            events (deque): A deque of dictionaries, each representing an event.

        Returns:
            set: A set of unique event types.
        """
        return {event['type'] for event in events if 'type' in event}

    @staticmethod
    def calculate_average_gap(events: deque, event_type: str) -> str:
        """
        Calculates the average time gap between events of a specified type.

        Args:
            events (deque): A deque of dictionaries, each representing an event.
            event_type (str): The type of event for which to calculate the average gap.

        Returns:
            str: A string representation of the average time gap. Returns "0:00:00" if no gaps are found.
        """
        timestamps = [
            datetime.fromisoformat(event['created_at']) for event in events
            if event.get('type') == event_type and event.get('created_at') is not None
        ]

        timestamps.sort()

        gaps = [
            (timestamps[i] - timestamps[i - 1]).total_seconds()
            for i in range(1, len(timestamps))
        ]

        average_gap = sum(gaps) / len(gaps) if gaps else 0
        return str(timedelta(seconds=average_gap))


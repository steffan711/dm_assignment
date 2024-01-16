from collections import deque, OrderedDict
from typing import Optional, List, Dict, Tuple


class QueueDict:
    """
    A class that implements a queue-like dictionary with a fixed capacity.
    The keys are strings, and values are deques. Oldest items are removed when capacity is exceeded.
    """
    def __init__(self, capacity: int) -> None:
        self._dict: Dict[str, deque[Dict]] = OrderedDict()
        self._capacity: int = capacity

    def put(self, key: str, value: deque) -> None:
        """
        Insert or update a deque. If the capacity is exceeded, remove the oldest deque.
        """
        if key not in self._dict:
            if len(self._dict) >= self._capacity:
                self._dict.popitem(last=False)
        self._dict[key] = value
        self._dict.move_to_end(key)

    def get(self, key: str) -> Optional[deque[Dict]]:
        """ Retrieve a deque by key. Returns None if the key is not found. """
        return self._dict.get(key, None)

    def __repr__(self) -> str:
        return repr(self._dict)

    def get_serializable_list(self) -> List[Tuple[str, List[Dict]]]:
        """
        Get a serializable list representation of the QueueDict items.
        """
        return [(key, list(value)) for key, value in self._dict.items()]

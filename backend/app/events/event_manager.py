from typing import Callable, Dict, List

class EventManager:
    """
    Simple publish/subscribe event manager.
    Other modules can subscribe to events like 'job_finished' or 'job_failed'.
    """

    def __init__(self):
        # dictionary of event_name -> list of callback functions
        self._subscribers: Dict[str, List[Callable]] = {}

    def subscribe(self, event_name: str, callback: Callable):
        """Subscribe a callback to an event"""
        if event_name not in self._subscribers:
            self._subscribers[event_name] = []
        self._subscribers[event_name].append(callback)

    def emit(self, event_name: str, **kwargs):
        """Emit an event to all subscribers"""
        if event_name in self._subscribers:
            for callback in self._subscribers[event_name]:
                callback(**kwargs)

# Create a global event manager instance
event_manager = EventManager()

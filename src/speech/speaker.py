"""Offline pyttsx3 speech wrapper."""
import queue
import threading


class Speaker:
    def __init__(self, enabled: bool, rate: int, volume: float, logger):
        self.enabled, self.logger = enabled, logger
        self.messages: queue.Queue[str | None] = queue.Queue()
        self.engine = None
        if enabled:
            try:
                import pyttsx3
                self.engine = pyttsx3.init()
                self.engine.setProperty("rate", rate)
                self.engine.setProperty("volume", volume)
                threading.Thread(target=self._worker, daemon=True).start()
            except Exception as exc:
                self.logger.warning("Speech unavailable: %s", exc)

    def _worker(self) -> None:
        while True:
            message = self.messages.get()
            if message is None:
                return
            try:
                self.engine.say(message)
                self.engine.runAndWait()
            except Exception as exc:
                self.logger.warning("Speech failed: %s", exc)

    def speak(self, message: str) -> None:
        if self.enabled and self.engine is not None:
            self.messages.put(message)

    def close(self) -> None:
        self.messages.put(None)

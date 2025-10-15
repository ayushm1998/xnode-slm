# src/metrics_store.py
import threading

class MetricsStore:
    def __init__(self):
        self._lock = threading.Lock()
        self.data = {
            "accuracy_by_intent": {},
            "agent_latency_ms": {},
            "workflow_efficiency": 0,
            "total_predictions": 0
        }

    def record(self, intent, confidence, latency_ms):
        with self._lock:
            self.data["total_predictions"] += 1
            # average accuracy per intent
            if intent not in self.data["accuracy_by_intent"]:
                self.data["accuracy_by_intent"][intent] = confidence
            else:
                old = self.data["accuracy_by_intent"][intent]
                self.data["accuracy_by_intent"][intent] = (old + confidence) / 2

            # track latency
            self.data["agent_latency_ms"][intent] = latency_ms

            # compute fake workflow efficiency (mean accuracy)
            self.data["workflow_efficiency"] = (
                sum(self.data["accuracy_by_intent"].values()) /
                len(self.data["accuracy_by_intent"])
                if self.data["accuracy_by_intent"]
                else 0
            )

    def summary(self):
        with self._lock:
            return self.data

# ✅ Persistent global instance
metrics_store = MetricsStore()

from collections import defaultdict
from datetime import timedelta


class DetectionContext:
    def __init__(self):
        self.login_events = defaultdict(list)
        self.transaction_events = defaultdict(list)

        self.last_ip = {}
        self.last_location = {}

        self.transaction_totals = defaultdict(float)
        self.transaction_counts = defaultdict(int)

        self.ato_flag = {}

    def add_event(self, event):
        user = event.get("user_id")
        if not user:
            return

        event_type = event.get("event_type")
        timestamp = event.get("timestamp")
        ip = event.get("source_ip")

        
        if event_type in ["login_failed", "login_success"]:
            if timestamp:
                self.login_events[user].append((event_type, timestamp))

       
        if event_type == "transaction":
            amount = event.get("event_data", {}).get("amount", 0)

            if timestamp:
                self.transaction_events[user].append((amount, timestamp))

            self.transaction_totals[user] += amount
            self.transaction_counts[user] += 1

        
        if ip:
            self.last_ip[user] = ip

    def get_recent_logins(self, user, window_seconds, current_time):
        if not current_time:
            return []

        return [
            e for e in self.login_events[user]
            if (current_time - e[1]) <= timedelta(seconds=window_seconds)
        ]

    def get_recent_transactions(self, user, window_seconds, current_time):
        if not current_time:
            return []

        return [
            e for e in self.transaction_events[user]
            if (current_time - e[1]) <= timedelta(seconds=window_seconds)
        ]

    def get_avg_transaction(self, user):
        count = self.transaction_counts[user]
        if count == 0:
            return 0
        return self.transaction_totals[user] / count
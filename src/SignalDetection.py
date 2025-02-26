class SignalDetection:
    def __init__(self, hits, misses, false_alarms, correct_rejections):
        self.hits = hits
        self.misses = misses
        self.false_alarms = false_alarms
        self.correct_rejections = correct_rejections

    def hit_rate(self):
        total_signals = self.hits + self.misses
        if total_signals == 0:
            return 0.0
        return self.hits / total_signals

    def false_alarm_rate(self):
        total_noises = self.false_alarms + self.correct_rejections
        if total_noises == 0:
            return 0.0
        return self.false_alarms / total_noises
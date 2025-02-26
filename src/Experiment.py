import matplotlib.pyplot as plt

class Experiment:
    def __init__(self):
        self.conditions = [] 

    def add_condition(self, sdt_obj, label=None):
        self.conditions.append((sdt_obj, label))

    def sorted_roc_points(self):
        if not self.conditions:
            raise ValueError("No conditions added to the experiment")
        false_alarm_rates = [sdt.false_alarm_rate() for sdt, _ in self.conditions]
        hit_rates = [sdt.hit_rate() for sdt, _ in self.conditions]
        sorted_pairs = sorted(zip(false_alarm_rates, hit_rates))
        false_alarm_rates, hit_rates = zip(*sorted_pairs)
        return list(false_alarm_rates), list(hit_rates)

    def compute_auc(self):
        if not self.conditions:
            raise ValueError("No conditions added to the experiment")
        false_alarm_rates, hit_rates = self.sorted_roc_points()
        auc = 0.0
        for i in range(1, len(false_alarm_rates)):
            auc += (false_alarm_rates[i] - false_alarm_rates[i-1]) * (hit_rates[i] + hit_rates[i-1]) / 2
        return auc

    def plot_roc_curve(self, show_plot=True):
        false_alarm_rates, hit_rates = self.sorted_roc_points()
        plt.plot(false_alarm_rates, hit_rates, marker='o', label='ROC Curve')
        plt.plot([0, 1], [0, 1], 'k--', label='Random Guess')
        plt.xlabel('False Alarm Rate')
        plt.ylabel('Hit Rate')
        plt.title('ROC Curve')
        plt.legend()
        if show_plot:
            plt.show()
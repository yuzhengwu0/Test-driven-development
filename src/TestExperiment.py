import unittest
from Experiment import Experiment
from SignalDetection import SignalDetection

class TestExperiment(unittest.TestCase):
    def test_add_condition(self):
        exp = Experiment()
        sdt = SignalDetection(10, 0, 0, 10)
        exp.add_condition(sdt, "Condition1")
        self.assertEqual(len(exp.conditions), 1)
        self.assertEqual(exp.conditions[0][1], "Condition1")

    def test_sorted_roc_points_empty(self):
        exp = Experiment()
        with self.assertRaises(ValueError):
            exp.sorted_roc_points()

    def test_sorted_roc_points_order(self):
        exp = Experiment()
        exp.add_condition(SignalDetection(10, 0, 10, 0))  # FAR=1.0, HR=1.0
        exp.add_condition(SignalDetection(0, 10, 0, 10))  # FAR=0.0, HR=0.0
        far, hr = exp.sorted_roc_points()
        self.assertEqual(far, [0.0, 1.0])
        self.assertEqual(hr, [0.0, 1.0])

    def test_compute_auc_two_points(self):
        exp = Experiment()
        exp.add_condition(SignalDetection(0, 10, 0, 10))  # (0,0)
        exp.add_condition(SignalDetection(10, 0, 10, 0))  # (1,1)
        self.assertAlmostEqual(exp.compute_auc(), 0.5)

    def test_compute_auc_three_points_perfect(self):
        exp = Experiment()
        exp.add_condition(SignalDetection(0, 10, 0, 10))  # (0,0)
        exp.add_condition(SignalDetection(10, 0, 0, 10))  # (0,1)
        exp.add_condition(SignalDetection(10, 0, 10, 0))  # (1,1)
        self.assertAlmostEqual(exp.compute_auc(), 1.0)

    def test_compute_auc_empty(self):
        exp = Experiment()
        with self.assertRaises(ValueError):
            exp.compute_auc()

    def test_add_condition_without_label(self):
        exp = Experiment()
        sdt = SignalDetection(5, 5, 5, 5)
        exp.add_condition(sdt)
        self.assertEqual(len(exp.conditions), 1)
        self.assertIsNone(exp.conditions[0][1])

    def test_sorted_roc_points_multiple_conditions(self):
        exp = Experiment()
        exp.add_condition(SignalDetection(8, 2, 1, 9))  # FAR=0.1, HR=0.8
        exp.add_condition(SignalDetection(5, 5, 2, 8))  # FAR=0.2, HR=0.5
        exp.add_condition(SignalDetection(2, 8, 3, 7))  # FAR=0.3, HR=0.2
        far, hr = exp.sorted_roc_points()
        self.assertEqual(far, [0.1, 0.2, 0.3])
        self.assertEqual(hr, [0.8, 0.5, 0.2])

    def test_compute_auc_multiple_points(self):
        exp = Experiment()
        exp.add_condition(SignalDetection(0, 10, 0, 10))  # (0,0)
        exp.add_condition(SignalDetection(5, 5, 2, 8))   # (0.2,0.5)
        exp.add_condition(SignalDetection(10, 0, 10, 0)) # (1,1)
        auc = exp.compute_auc()
        self.assertAlmostEqual(auc, 0.65)  # 手工计算：0.05 + 0.6 = 0.65

if __name__ == '__main__':
    unittest.main()
from math import fabs


class FindAsymptoticValues():
  def __init__(self, values):
    self.values = values
    
  def get_asymptotic_value(self, window_size):
    start = len(self.values) - window_size
    end = len(self.values)
    average1 = sum(self.values[start:end]) / window_size
    average2 = sum(self.values[start-1:end-1]) / window_size
    convergence = fabs(average1 - average2) / average1

    return convergence, average1

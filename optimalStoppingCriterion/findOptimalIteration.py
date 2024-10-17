from math import fabs


class FindOptimalIteration():
  def __init__(self, window_size, values):
    self.window_size = window_size
    self.values = values
    self.averages = [0] * (len(values) - window_size)
    self._calculate_averages()

  def get_start_of_monotonic_convergence(self):
    positive_slope_end = (self.averages[-1] - self.averages[-2]) >= 0
    for iteration in range(len(self.values) - 2, self.window_size, -1):
      index = iteration - self.window_size
      
      current_slope = self.averages[index + 1] - self.averages[index] >= 0

      if current_slope != positive_slope_end:
        return iteration
  
    print('WARNING: Could not determine start of monotonic convergence!')
    print('Your simulation may be strictly monotonically converging!')
    print('If this is the case, you can ignore this warning\n')

    return len(self.values)
  
  def get_iteration_with_highest_acceptable_error(self, average, threshold):
    for iteration in range(len(self.values) - self.window_size - 1, 0, -1):
      residual = fabs(self.averages[iteration] - average)
      residual /= average

      if residual > threshold:
        return iteration

    print('  WARNING: Could not determine iteration with highest acceptable error!')
    print(f'  Your error threshold of {threshold} may be set too high.\n')
    return len(self.values)
  
  def _calculate_averages(self):
    for iteration in range(self.window_size, len(self.values)):
      index = iteration - self.window_size
      self.averages[index] = \
        sum(self.values[iteration - i] for i in range(0, self.window_size))
      self.averages[index] /= self.window_size
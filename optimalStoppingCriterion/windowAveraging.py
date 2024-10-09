from math import fabs


class WindowAveraging():
  def __init__(self, smallest_window, largest_window, increments):
    self.smallest_window = smallest_window
    self.largest_window = largest_window
    self.increments = increments
    self.window_sizes = list()
    self._generate_window_sizes()

  def _generate_window_sizes(self):
    window_range = self.largest_window - self.smallest_window
    if not window_range % self.increments == 0:
      raise Exception(f'Cannot create window sizes between {self.smallest_window} and {self.largest_window} with increments of {self.increments}')

    for window in range(self.smallest_window, self.largest_window, self.increments):
      self.window_sizes.append(window)
    self.window_sizes.append(self.largest_window)

  def apply_window_averaging(self, convergence_tolerange, values):
    if len(values)/2 < self.window_sizes[-1]:
      raise Exception(f'Number of values must be at least twice the largest window size. {len(values)}/2 > {self.window_sizes[-1]}')
    
    has_converged = list()
    iterations_to_convergence = list()

    last_two_values = [0, 0]
    for window in self.window_sizes:
      for iteration in range(window, len(values)):
        average = sum(values[iteration - i] for i in range(0, window)) / window
        
        last_two_values[0] = last_two_values[1]
        last_two_values[1] = average

        if fabs(last_two_values[0] - last_two_values[1]) < convergence_tolerange:
          has_converged.append(True)
          iterations_to_convergence.append(iteration)
          break

    return has_converged, iterations_to_convergence, self.window_sizes
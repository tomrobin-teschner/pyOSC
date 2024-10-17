from math import fabs, floor, log10, ceil


class WindowAveraging():
  def __init__(self, smallest_window, largest_window, increments, \
    earliest_iteration_to_stop, asymptotic_average, \
    asymptotic_convergence_threshold, values):

    self.smallest_window = smallest_window
    self.largest_window = largest_window
    self.increments = increments
    self.earliest_iteration_to_stop = earliest_iteration_to_stop
    self.asymptotic_average = asymptotic_average
    self.asymptotic_convergence_threshold = asymptotic_convergence_threshold
    self.values = values

    self.window_sizes = list()
    self._generate_window_sizes()

  def _generate_window_sizes(self):

    window_range = self.largest_window - self.smallest_window
    if not window_range % self.increments == 0:
      raise Exception(f'Cannot create window sizes between {self.smallest_window} and {self.largest_window} with increments of {self.increments}')

    for window in range(self.smallest_window, self.largest_window, self.increments):
      self.window_sizes.append(window)
    self.window_sizes.append(self.largest_window)

  def determine_best_residual_threshold(self):
    has_converged = list()
    iterations_to_convergence = list()
    residual = list()

    for window in self.window_sizes:
      averages = [0] * (len(self.values) - window)
      for iteration in range(window, len(self.values)):
        index = iteration - window
        averages[index] = sum(self.values[iteration - i] for i in range(0, window))
        averages[index] /= window
      
      window_residual = [0] * (len(self.values) - window - 1)
      lowest_residual_before_optimum = 1
      lowest_residual_after_optimum = 1
      iteration_before_optimum = 0
      iteration_after_optimum = 0
      for iteration in range(window, len(self.values) - 1):
        index = iteration - window

        window_residual[index] = fabs(averages[index + 1] - averages[index])
        window_residual[index] /= fabs(averages[index])

        if iteration < self.earliest_iteration_to_stop:
          if window_residual[index] < lowest_residual_before_optimum:
            lowest_residual_before_optimum = window_residual[index]
            iteration_before_optimum = iteration
        else:
          if window_residual[index] < lowest_residual_after_optimum:
            lowest_residual_after_optimum = window_residual[index]
            iteration_after_optimum = iteration

      if lowest_residual_before_optimum < lowest_residual_after_optimum:
        has_converged.append(False)
        iterations_to_convergence.append(iteration_before_optimum)
        residual.append(self._2_sig_dig(lowest_residual_before_optimum))

      elif lowest_residual_before_optimum >= lowest_residual_after_optimum:
        has_converged.append(True)
        iterations_to_convergence.append(iteration_after_optimum)
        residual.append(self._2_sig_dig(lowest_residual_after_optimum))

    return has_converged, iterations_to_convergence, residual, self.window_sizes
      
  def _2_sig_dig(self, x, sig=1):
    exp = floor(log10(abs(x)))
    mantissa = x / 10**exp
    mantissa = ceil(mantissa * 10**sig) / 10**sig
    return format(mantissa * 10**exp, f'.{sig}e')
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

    for window_size in self.window_sizes:
      averages = [0] * (len(self.values) - window_size)
      for iteration in range(window_size, len(self.values)):
        index = iteration - window_size
        averages[index] = sum(self.values[iteration - i] for i in range(0, window_size))
        averages[index] /= window_size
      
      window_residual = [0] * (len(self.values) - window_size - 1)
      for iteration in range(window_size, len(self.values) - 1):
        index = iteration - window_size
        window_residual[index] = fabs(averages[index + 1] - averages[index])
        window_residual[index] /= fabs(averages[index])

      assert self.earliest_iteration_to_stop > window_size, \
        'optimal iteration to stop reached before largest window size. Reduce your window sizes!\n' \
        f'Largest window:            {self.window_sizes[-1]}\n' \
        f'Optimal iteration to stop: {self.earliest_iteration_to_stop}\n' \
        f'Max window size possible:  {self.earliest_iteration_to_stop}\n'
      residual_at_optimum = window_residual[self.earliest_iteration_to_stop - window_size]

      has_lower_residual_before_optimum = False
      iteration_before_optimum = 0
      residual_before_optimum = 0
      for iteration in range(0, self.earliest_iteration_to_stop - window_size):
        if window_residual[iteration] < residual_at_optimum:
          has_lower_residual_before_optimum = True
          iteration_before_optimum = iteration + window_size
          residual_before_optimum = window_residual[iteration]

      has_lower_residual_after_optimum = False
      iteration_beyond_optimum = 0
      residual_after_optimum = 0
      for iteration in range(self.earliest_iteration_to_stop - window_size, len(self.values) - window_size - 1):
        if window_residual[iteration] < residual_at_optimum:
          has_lower_residual_after_optimum = True
          iteration_beyond_optimum = iteration + window_size
          residual_after_optimum = window_residual[iteration]
        if has_lower_residual_before_optimum and has_lower_residual_after_optimum:
          if residual_after_optimum < residual_before_optimum:
            break

      if has_lower_residual_before_optimum and not has_lower_residual_after_optimum:
        has_converged.append(False)
        iterations_to_convergence.append(iteration_before_optimum)
        residual.append(self._2_sig_dig(residual_before_optimum))  
      elif has_lower_residual_before_optimum and has_lower_residual_after_optimum:
        if residual_before_optimum <= residual_after_optimum:
          has_converged.append(False)
          iterations_to_convergence.append(iteration_before_optimum)
          residual.append(self._2_sig_dig(residual_before_optimum))
        elif residual_before_optimum > residual_after_optimum:
          has_converged.append(True)
          iterations_to_convergence.append(iteration_beyond_optimum)
          residual.append(self._2_sig_dig(residual_after_optimum))
      elif not has_lower_residual_before_optimum:
        has_converged.append(True)
        iterations_to_convergence.append(self.earliest_iteration_to_stop)
        residual.append(self._2_sig_dig(residual_at_optimum))

    return has_converged, iterations_to_convergence, residual, self.window_sizes
      
  def _2_sig_dig(self, x, sig=1):
    exp = floor(log10(abs(x)))
    mantissa = x / 10**exp
    mantissa = ceil(mantissa * 10**sig) / 10**sig
    return format(mantissa * 10**exp, f'.{sig}e')
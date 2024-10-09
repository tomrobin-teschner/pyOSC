import optimalStoppingCriterion as osc


data = {
  "wing": {
    "lift": "inputs/lift-rfile.out",
    "drag": "inputs/drag-rfile.out"
  }
}

min_window_size = 20
max_window_size = 400
window_increments = 10

convergence_threshold = 0.0001


def main():
  convergence_data = dict()
  for boundary, coefficients in data.items():
    boundary_data = dict()
    for name, filename in coefficients.items():
      values = osc.fluent_file_reader(filename).get_values()
      averager = osc.window_averaging(min_window_size, max_window_size, window_increments)
      converged, iterations, window_sizes = averager.apply_window_averaging(convergence_threshold, values)

      boundary_data[name] = [converged, iterations, window_sizes]    
    convergence_data[boundary] = boundary_data

  find_stopping_criterion = osc.stopping_criterion(convergence_data)
  window_sizes = find_stopping_criterion.get_window_size()
  print(window_sizes)

  best_window_sizes = find_stopping_criterion.get_best_window_size()
  print(best_window_sizes)


if __name__ == "__main__":
  main()
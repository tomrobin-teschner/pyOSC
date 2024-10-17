import optimalStoppingCriterion as osc
from os.path import join
from os import listdir
import json
from sys import argv

# define the case. Name needs to match folder name within input/ folder
case = 'saab340'

min_window_size = 10
max_window_size = 100
window_increments = 5

asymptotic_convergence_threshold = 1e-2

def main():
  # process command line arguments (CLAs)
  cla = osc.handle_cla(argv)

  exit()
  # initialise dictionary holding convergence results
  convergence_data = dict()

  # determine boundaries and the stored coefficients on each boundary patch
  input_folder = join('input', case)
  boundaries = listdir(input_folder)
  coefficients = listdir(join(input_folder, boundaries[0]))

  # initialise coefficient plot
  coefficient_plot = osc.plot_convergence('coefficients', boundaries, coefficients)

  # walk over all boundaries and coefficients to collect data
  for boundary in boundaries:
    boundary_data = dict()
    for coefficient in coefficients:
      print(f'processing {boundary} / {coefficient}')

      # obtain filenames for coefficients
      filename = listdir(join(input_folder, boundary, coefficient))[0]
      path_and_filename = join(input_folder, boundary, coefficient, filename)

      # read values from file
      values = osc.fluent_file_reader(path_and_filename).get_values()

      # determine the averaged (asymptotic) coefficient value at the end of the simulation
      asymptotic_values = osc.find_asymptotic_values(values)
      asymptotic_convergence, asymptotic_average = \
        asymptotic_values.get_asymptotic_value(min_window_size)

      # determine the theoretically earliest iteration to reach convergence
      foi = osc.find_optimal_iteration(min_window_size, values)

      monotonic_convergence_start = foi.get_start_of_monotonic_convergence()
      coefficient_plot.add_monotonic_convergence(boundary, coefficient, \
        monotonic_convergence_start)
      
      earliest_iteration = foi.get_iteration_with_highest_acceptable_error( \
        asymptotic_average, asymptotic_convergence_threshold)
      coefficient_plot.add_earliest_stopping_iteration(boundary, coefficient, \
        earliest_iteration)
      
      # apply window averaging to determine convergence
      averager = osc.window_averaging(min_window_size, max_window_size, \
        window_increments, earliest_iteration, asymptotic_average, \
        asymptotic_convergence_threshold, values)
      
      # determine the best residual threshold and iteration to stop
      converged, iterations, threshold, window_sizes = \
        averager.determine_best_residual_threshold()

      # add data to coefficient_plot
      coefficient_plot.add_data(boundary, coefficient, values)

      # store data
      boundary_data[coefficient] = [converged, iterations, threshold, window_sizes]    
    convergence_data[boundary] = boundary_data

  find_stopping_criterion = osc.stopping_criterion(convergence_data)
  windowed_data = find_stopping_criterion.get_window_size()
  
  with open(join('output', case +'_windowed_data.json'), 'w') as f:
    json.dump(windowed_data, f, indent=4)

  # add optimal stopping point to each plot
  coefficient_plot.add_optimal_iteration(windowed_data)

  # save figures from plotting
  coefficient_plot.plot(case)

  # output results to screen
  print(f'----- Best window sizes per BC patch -----')
  for boundary in windowed_data:
    print(f'{boundary}:')
    for coefficient in windowed_data[boundary]:
      print(f'  {coefficient}:')
      print(f'    Iterations:            {windowed_data[boundary][coefficient]["iterations"]}')
      print(f'    Window size:           {windowed_data[boundary][coefficient]["window_size"]}')
      print(f'    Convergence threshold: {windowed_data[boundary][coefficient]["convergence_threshold"]}')
    print('')

if __name__ == "__main__":
  main()
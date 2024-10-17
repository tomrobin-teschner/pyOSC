import matplotlib.pyplot as plt
from os.path import join

class PlotConvergence():
  def __init__(self, name, boundaries, coefficients):
    self.name = name
    self.boundaries = boundaries
    self.coefficients = coefficients

    num_rows = len(boundaries)
    num_cols = len(coefficients)

    fig, ax = plt.subplots(len(boundaries), len(coefficients), \
      figsize=(num_cols * 5, num_rows * 5))

    plt.subplots_adjust(wspace=0.3, hspace=0.3)
    self.fig = fig
    self.ax = ax

  def add_data(self, boundary, coefficient, values):
    row = self._boundary_name_to_index(boundary)
    col = self._coefficient_name_to_index(coefficient)

    self._get_plot_handle(row, col).plot(values, color='k', linestyle='-')
    self._get_plot_handle(row, col).set_title(boundary, fontsize=16)
    self._get_plot_handle(row, col).set_ylabel(coefficient, fontsize=14)
    self._get_plot_handle(row, col).set_xlabel('Iterations', fontsize=14)
    self._get_plot_handle(row, col).tick_params(axis='both', which='major', \
      labelsize=12)

  def add_monotonic_convergence(self, boundary, coefficient, iteration):
    row = self._boundary_name_to_index(boundary)
    col = self._coefficient_name_to_index(coefficient)
    self._get_plot_handle(row, col).axvline(x=iteration, color='orange', \
          linestyle='--')
    
  def add_earliest_stopping_iteration(self, boundary, coefficient, iteration):
    row = self._boundary_name_to_index(boundary)
    col = self._coefficient_name_to_index(coefficient)
    self._get_plot_handle(row, col).axvline(x=iteration, color='green', \
          linestyle='--')


  def add_optimal_iteration(self, windowed_data):
    optimal_iteration = -1
    for boundary in windowed_data:
      for coefficient in windowed_data[boundary]:
        row = self._boundary_name_to_index(boundary)
        col = self._coefficient_name_to_index(coefficient)
        iteration = windowed_data[boundary][coefficient]['iterations']

        self._get_plot_handle(row, col).axvline(x=iteration, color='k', \
          linestyle='--')

        if iteration > optimal_iteration:
          optimal_iteration = iteration
    
    for boundary in windowed_data:
      for coefficient in windowed_data[boundary]:
        row = self._boundary_name_to_index(boundary)
        col = self._coefficient_name_to_index(coefficient)
        self._get_plot_handle(row, col).axvline(x=optimal_iteration, \
          color='b', linestyle=':')

  def plot(self, case):
    self.fig.savefig(join('output', case + '_' + self.name + '.png'))

  def _boundary_name_to_index(self, boundary):
    index = 0
    for boundary_name in self.boundaries:
      if boundary_name == boundary:
        return index
      index += 1

  def _coefficient_name_to_index(self, coefficient):
    index = 0
    for coefficient_name in self.coefficients:
      if coefficient_name == coefficient:
        return index
      index += 1

  def _get_plot_handle(self, row, col):
    if len(self.boundaries) == 1:
      return self.ax[col]
    elif len(self.coefficients) > 1:
      return self.ax[row, col]

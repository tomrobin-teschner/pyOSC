import matplotlib.pyplot as plt
from os.path import join

class PlotConvergence():
  def __init__(self, coefficients):
    self.coefficients = coefficients
    self.figures = dict()
    self.ax = dict()

    count = 1
    for coefficient in self.coefficients:
      self.figures[coefficient] = plt.figure(count)
      self.ax[coefficient] = self.figures[coefficient].add_subplot(111)
      count += 1

  def add_data(self, boundary, coefficient, values):
    self.ax[coefficient].plot(values, label=boundary)

  def plot(self):
    for coefficient in self.coefficients:
      self.ax[coefficient].set_xlabel('Iterations')
      self.ax[coefficient].set_ylabel(coefficient)
      self.ax[coefficient].legend()
      # self.ax.axvline(x=2500, color='k', linestyle='--')
      self.figures[coefficient].savefig(join('output', coefficient + '.png'))

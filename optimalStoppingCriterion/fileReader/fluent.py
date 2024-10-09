from optimalStoppingCriterion.fileReader.base import FileReader

class FluentFileReader(FileReader):
  def __init__(self, filename):
    super().__init__(filename, 0)

  def _read(self):
    with open(self.filename, 'r') as f:
      lines = f.readlines()
      for line in lines:
        if not line.startswith('"') and not line.startswith('('):
          args = line.strip().split()
          self.phi.append(float(args[1]))
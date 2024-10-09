from optimalStoppingCriterion.fileReader.base import FileReader

class FluentFileReader(FileReader):
  def __init__(self, filename):
    super().__init__(filename, 0)

  def read(self):
    with open(self.filename, 'r') as f:
      return f.read()
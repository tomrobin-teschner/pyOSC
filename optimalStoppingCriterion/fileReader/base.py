from abc import ABC, abstractmethod


class FileReader(ABC):

  def __init__(self, filename, col):
    self.filename = filename
    self.column = col
    self.phi = list()
    if not self.__file_is_readable():
      raise Exception(f'Could not read file! File is: {self.filename}')
    
    self._read()


  @abstractmethod
  def _read(self):
    pass

  def get_values(self):
    return self.phi

  def __file_is_readable(self):
    try:
      with open(self.filename, 'r') as f:
        return True
    except:
      return False
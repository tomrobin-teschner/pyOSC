


class HandleCommandLineArguments():
  def __init__(self, args):
    self.args = args
    self.case = ''
    self.min_window = 10
    self.max_window = 100
    self.increments = 5
    self.asymptotic_convergence_threshold = 0.01
    self.max_iterations = 0
    self._process_cla()

  def _process_cla(self):
    has_case = False

    if '-c' in self.args:
      has_case = True
      self.case = self.args[self.args.index('-c') + 1]
    elif '--case' in self.args:
      has_case = True
      self.case = self.args[self.args.index('--case') + 1]

    if not has_case:
      raise Exception('No case specified. Use --help to see usage.')
    
    if '-w' in self.args:
      self.min_window = int(self.args[int(self.args.index('-w') + 1)])
      self.max_window = int(self.args[int(self.args.index('-w') + 2)])
      self.increments = int(self.args[int(self.args.index('-w') + 3)])

    elif '--window' in self.args:
      self.min_window = int(self.args[int(self.args.index('--window') + 1)])
      self.max_window = int(self.args[int(self.args.index('--window') + 2)])
      self.increments = int(self.args[int(self.args.index('--window') + 3)])

    else:
      print('No window size specified. Using default window size of min_window = 10, max_window = 100, increments = 5')
      print('If you want to change these defaults, see the help message with -h or --help\n')


    if '-act' in self.args:
      self.asymptotic_convergence_threshold = float(self.args[int(self.args.index('-act') + 1)])
    elif'--asymptotic-convergence-threshold' in self.args:
      self.asymptotic_convergence_threshold = float(self.args[int(self.args.index('--asymptotic-convergence-threshold') + 1)])
    else:
      print('No asymptotic convergence threshold specified.')
      print('Using default asymptotic convergence threshold of 0.01 (1%)\n')

    if '-mi' in self.args:
      self.max_iterations = int(self.args[int(self.args.index('-mi') + 1)])
    elif '--max-iterations' in self.args:
      self.max_iterations = int(self.args[int(self.args.index('--max-iterations') + 1)])

    if '-h' in self.args or '--help' in self.args:
      self._print_help()

  def get_case(self):
    return self.case

  def get_window_sizes(self):
    return self.min_window, self.max_window, self.increments
  
  def get_asymptotic_convergence_threshold(self):
    return self.asymptotic_convergence_threshold
  
  def get_max_iterations(self):
    return self.max_iterations


  def _print_help(self):
    if '-h' in self.args or '--help' in self.args:
      print('Usage: python3 pyOSC.py -c <case>\n')
      print('  -c, --case <case>    Case to run')
      print('  -h, --help           Show this help message and exit')
      print('  -w, --window         Window size to use for convergence analysis')
      print('                       Specified as a list of integers separated by spaces')
      print('                       Use the format <smallest window> <largest window> <increments>')
      print('                       Example: -w 10 100 10. Smallest window = 10')
      print('                       largest window = 100, and window increments = 10')
      print('                       If no window size is specified, the default 10 100 5 is used')
      print('  -act, --asymptotic-convergence-threshold')
      print('                       Asymptotic convergence threshold to use for convergence analysis.')
      print('                       This value will be used to check if coefficients have converged')
      print('                       to the asymptotic value at the end of the simulation.')
      print('  -mi, --max-iteration Max number of iterations to consider in convergence analysis')

      exit()


  
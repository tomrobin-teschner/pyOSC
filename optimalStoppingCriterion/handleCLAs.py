


class HandleCommandLineArguments():
  def __init__(self, args):
    self.args = args
    self.case = ''
    self.min_window = 10
    self.max_window = 100
    self.increments = 5
    self.convergence_threshold = 0.01
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


    if '-ct' in self.args:
      self.convergence_threshold = float(self.args[int(self.args.index('-ct') + 1)])
    elif'--convergence-threshold' in self.args:
      self.convergence_threshold = float(self.args[int(self.args.index('--convergence-threshold') + 1)])
    else:
      print('No convergence threshold specified. Using default convergence threshold of 0.01 (i.e. 1%)\n')

    if '-h' in self.args or '--help' in self.args:
      self._print_help()

  def get_case(self):
    return self.case

  def get_window_sizes(self):
    return self.min_window, self.max_window, self.increments
  
  def get_convergence_threshold(self):
    return self.convergence_threshold


  def _print_help(self):
    if '-h' in self.args or '--help' in self.args:
      print('Usage: python3 pyOSC.py -c <case>\n')
      print('  -c, --case <case>  Case to run')
      print('  -h, --help         Show this help message and exit')
      print('  -w, --window       Window size to use for convergence analysis')
      print('                     Specified as a list of integers separated by spaces')
      print('                     Use the format <smallest window> <largest window> <increments>')
      print('                     Example: -w 10 100 10. Smallest window = 10')
      print('                     largest window = 100, and window increments = 10')
      print('                     If no window size is specified, the default 10 100 5 is used')
      print('  -act, --asymptotic-convergence-threshold')
      print('                     Asymptotic convergence threshold to use for convergence analysis.')
      print('                     This value will be used to check if coefficients have converged')
      print('                     to the asymptotic value at the end of the simulation.')

      exit()


  
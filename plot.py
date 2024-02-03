import sys
from time import sleep


def plot_process(queues):
   while True:
       res = queues['plot'].get()
       if res[0] == 'init':
           bars = res[1]
           print('plot_process init', flush=True)
           print(bars.tail(), flush=True)
       else:
           print('unknown resonse. should be init', res[0], flush=True)
           sys.exit(1)
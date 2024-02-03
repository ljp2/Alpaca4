import matplotlib.pyplot as plt
import matplotlib.animation as animation
from multiprocessing import Process, Queue
import numpy as np
import time


# def plot_process(queues):
#    while True:
#        res = queues['plot'].get()
#        if res[0] == 'init':
#            bars = res[1]
#            print('plot_process init', flush=True)
#            print(bars.tail(), flush=True)
#        else:
#            print('unknown resonse. should be init', res[0], flush=True)
#            sys.exit(1)
           
           
def plot_process(queues):
    q = queues['plot']
    plt.ion()
    fig, ax = plt.subplots()
    line, = ax.plot([], [], lw=2)


    data = q.get()
    bars = data[1]
    print('plot_process init', flush=True)
    print(bars.tail(), flush=True)
    
    x = bars.timestamp.values
    y = bars.close.values      
    line.set_data(x, y)
    plt.pause(0.1)


    while True:
        data = q.get()
        bars = data[1]
        x = bars.timestamp.values
        y = bars.close.values
        line.set_data(x, y)
        plt.pause(0.1)


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
           
           

# Create a queue
q = Queue()

# Function to put data into the queue
def put_data_into_queue(q):
    for i in range(100):
        q.put(np.random.rand(10))
        time.sleep(0.1)

# Create a new process that will put data into the queue
p = Process(target=put_data_into_queue, args=(q,))
p.start()

# Create a figure and an axis
fig, ax = plt.subplots()

# Initialize a line object which will be updated
line, = ax.plot([], [], lw=2)

# Initialization function
def init():
    line.set_data([], [])
    return line,

# Animation function. This is called sequentially
def animate(i):
    if not q.empty():
        y = q.get()
        x = np.arange(len(y))
        line.set_data(x, y)
    return line,

# Call the animator
ani = animation.FuncAnimation(fig, animate, init_func=init, frames=100, interval=100, blit=True)

plt.show()
import multiprocessing

def analysis_process(queues):
    bars_queue:multiprocessing.Queue = queues["bars"]
    info_queue:multiprocessing.Queue = queues["info"]
    i = 0
    while True:
        bar = bars_queue.get()
        print(bar)
        # info_queue.put(bar)

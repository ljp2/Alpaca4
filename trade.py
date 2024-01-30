import pandas as pd
from multiprocessing import Process, Queue

from bars import bars_process


if __name__ == "__main__":
    queues = {
        "init_bars": Queue(),
        "bars": Queue(),
        "plot": Queue(),
        "info": Queue(),    
    }

    # ui_process = multiprocessing.Process(target=labels_main, args=(queues,))
    # streaming = multiprocessing.Process(target=get_bars_process, args=(queues,))
    # analysis = multiprocessing.Process(target=analysis_process, args=(queues,))

    try:
        get_bars_process = Process(target=bars_process, args=(queues,))
        get_bars_process.start()
        get_bars_process.join()

        bars = queues['init_bars'].get()
        print(bars)
        print(type(bars))


    except KeyboardInterrupt:
        # Handle Ctrl+C gracefully by terminating both processes
        get_bars_process.terminate()

import sys
import numpy as np
import pandas as pd
from multiprocessing import Process, Queue

from moving_averages import weighted_moving_average_last

from bars import bars_process
from analysis import analysis_process

def main():
    queues = {
        "bars": Queue(),
        "plot": Queue(),
        "info": Queue(),    
    }

    try:
        do_analysis_process = Process(target=analysis_process, args=(queues,), daemon=True) 
        do_analysis_process.start()
        get_bars_process = Process(target=bars_process, args=(queues,), daemon=True)  
        get_bars_process.start()

        get_bars_process.join()
        do_analysis_process.join()
       
    except KeyboardInterrupt:
        # Handle Ctrl+C gracefully by terminating processes
        get_bars_process.terminate()
        do_analysis_process.terminate()
        sys.exit(0)

if __name__ == "__main__":
    main()
    
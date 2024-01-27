
import multiprocessing
import pandas as pd
from datetime import datetime, timedelta
from time import sleep

from alpaca.data.historical.crypto import CryptoHistoricalDataClient
from alpaca.data.requests import CryptoLatestBarRequest

from UI.widget_info import labels_main
from analysis import analysis_process
from stream import get_bars_process



if __name__ == "__main__":
    queues = {
        "bars": multiprocessing.Queue(),
        "plot": multiprocessing.Queue(),
        "info": multiprocessing.Queue(),    
    }

    ui_process = multiprocessing.Process(target=labels_main, args=(queues,))
    streaming = multiprocessing.Process(target=get_bars_process, args=(queues,))
    analysis = multiprocessing.Process(target=analysis_process, args=(queues,))

    try:
        # Start the UI process
        # ui_process.start()
        
        # Start the streaming process
        streaming.start()

        # Start the analysis process
        analysis.start()

        # Wait for both processes to finish
        # ui_process.join()
        streaming.join()
        analysis.join()

    except KeyboardInterrupt:
        # Handle Ctrl+C gracefully by terminating both processes
        streaming.terminate()
        analysis.terminate()
        streaming.join()
        analysis.join()

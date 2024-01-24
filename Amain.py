import sys
import multiprocessing
import time

from alpaca.data.live import CryptoDataStream

from keys import paper_apikey, paper_secretkey
apikey = paper_apikey
secretkey = paper_secretkey

# from UI.widget_plots import main
from UI.widget_info import labels_main


def streaming_process(queues):
    print("Streaming process started")
    crypto_stream = CryptoDataStream(apikey, secretkey)
    bars_queue = queues["bars"]

    async def bar_data_handler(data):
        print("Got bar data")
        bars_queue.put(data)

    async def updated_bar_data_handler(data):
        # quote data will arrive here
        print("\nUpdated bar data")
        bars_queue.put(data)
        
    crypto_stream.subscribe_bars(bar_data_handler, "BTC/USD")
    crypto_stream.subscribe_updated_bars(updated_bar_data_handler, "BTC/USD")
    crypto_stream.run()


def analysis_process(queues):
    bars_queue:multiprocessing.Queue = queues["bars"]
    info_queue:multiprocessing.Queue = queues["info"]
    i = 0
    while True:
        bar = bars_queue.get()
        print(bar)
        info_queue.put(bar)


if __name__ == "__main__":
    # Create multiprocessing.Queues for communication between processes
    queues = {
        "bars": multiprocessing.Queue(),
        "plot": multiprocessing.Queue(),
        "info": multiprocessing.Queue(),    
    }

    # Create multiprocessing.Process objects for streaming and analysis
    ui_process = multiprocessing.Process(target=labels_main, args=(queues,))
    streaming = multiprocessing.Process(target=streaming_process, args=(queues,))
    analysis = multiprocessing.Process(target=analysis_process, args=(queues,))

    try:
        # Start the UI process
        ui_process.start()
        
        # Start the streaming process
        streaming.start()

        # Start the analysis process
        analysis.start()

        # Wait for both processes to finish
        ui_process.join()
        streaming.join()
        analysis.join()

    except KeyboardInterrupt:
        # Handle Ctrl+C gracefully by terminating both processes
        streaming.terminate()
        analysis.terminate()
        streaming.join()
        analysis.join()


    print("Main process finished")


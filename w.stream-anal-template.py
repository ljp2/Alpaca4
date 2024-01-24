import sys
import multiprocessing
import time
import queue  # Import the queue module


# from UI.widget_plots import main
from UI.widget_info import labels_main


def streaming_process(data_queue):
    # Placeholder for your streaming logic (e.g., using WebSocket)
    print("Streaming process started")

    # Example: Replace this with your streaming logic
    for data_item in range(5):
        time.sleep(1)  # Simulating streaming activity
        data_queue.put("GOT" + str(data_item))

    print("Streaming process finished")

def analysis_process(data_queue):
    # Placeholder for your analysis logic
    print("Analysis process started")

    # Example: Replace this with your analysis logic
    while True:
        try:
            data_item = data_queue.get(timeout=1)
            print("Analysis process received data:", data_item)
            # Replace this with your analysis logic using the data_item
        except queue.Empty:
            # No more data in the queue, exit the loop
            break

    print("Analysis process finished")

if __name__ == "__main__":
    # Create multiprocessing.Queue for communication between processes
    data_queue = multiprocessing.Queue()

    # Create multiprocessing.Process objects for streaming and analysis
    ui_process = multiprocessing.Process(target=labels_main, args=(data_queue,))
    streaming = multiprocessing.Process(target=streaming_process, args=(data_queue,))
    analysis = multiprocessing.Process(target=analysis_process, args=(data_queue,))

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


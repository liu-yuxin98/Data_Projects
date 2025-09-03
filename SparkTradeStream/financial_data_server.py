# financial_server.py
from financial_data_generator import start_financial_data_stream
import time

if __name__ == "__main__":
    print("🚀 Launching Financial Data Server (Standalone Mode)")
    
    # Start the data stream server on port 9999
    data_thread = start_financial_data_stream(port=9999, interval=1.0)
    
    print("✅ Server started, waiting for clients...")
    print("Press Ctrl+C to stop.\n")

    try:
        # Keep main thread alive so background thread continues running
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        print("\n🛑 Server shutting down...")
        data_thread.join()
        print("✅ Server shutdown complete.")

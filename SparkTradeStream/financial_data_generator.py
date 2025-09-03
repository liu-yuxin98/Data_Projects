# =============================================================================
# FINANCIAL DATA STREAMER (DEBUG VERSION)
# =============================================================================
import random
import uuid
import json
import socket
import threading
import time
from datetime import datetime

class FinancialDataGenerator:
    """Generates realistic financial transactions."""
    def __init__(self):
        self.symbols = ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA',
                        'NVDA', 'META', 'NFLX', 'BABA', 'AMD',
                        'UBER', 'SPOT', 'ZOOM', 'SQ', 'PYPL']
        self.exchanges = ['NYSE', 'NASDAQ', 'CBOE', 'AMEX']
        self.currencies = ['USD', 'EUR', 'GBP', 'JPY', 'CAD']
        self.transaction_types = ['BUY', 'SELL', 'TRANSFER']
        self.customer_segments = ['RETAIL', 'INSTITUTIONAL', 'VIP']
        self.price_ranges = {
            'AAPL': (150, 200), 'GOOGL': (2500, 3000), 'MSFT': (300, 400),
            'AMZN': (3000, 4000), 'TSLA': (200, 800), 'NVDA': (400, 600),
            'META': (200, 350), 'NFLX': (350, 500), 'BABA': (80, 150),
            'AMD': (80, 120), 'UBER': (30, 60), 'SPOT': (100, 200),
            'ZOOM': (100, 200), 'SQ': (60, 120), 'PYPL': (60, 100)
        }

    def generate_transaction(self):
        symbol = random.choice(self.symbols)
        transaction_type = random.choice(self.transaction_types)
        min_price, max_price = self.price_ranges.get(symbol, (50, 200))
        price = round(random.uniform(min_price, max_price), 2)

        segment = random.choice(self.customer_segments)
        if segment == 'INSTITUTIONAL':
            quantity = random.randint(1000, 10000)
        elif segment == 'VIP':
            quantity = random.randint(100, 1000)
        else:
            quantity = random.randint(1, 100)

        volatility = random.uniform(0.95, 1.05)
        price = round(price * volatility, 2)
        total_amount = round(price * quantity, 2)

        return {
            'transaction_id': str(uuid.uuid4()),
            'timestamp': datetime.now().isoformat(),
            'account_id': f'ACC_{random.randint(10000, 99999)}',
            'transaction_type': transaction_type,
            'symbol': symbol,
            'quantity': quantity,
            'price': price,
            'total_amount': total_amount,
            'currency': random.choice(self.currencies),
            'exchange': random.choice(self.exchanges),
            'customer_segment': segment
        }

def start_financial_data_stream(port=9999, interval=1.0):
    """Start the financial data TCP server with debug logging."""
    generator = FinancialDataGenerator()

    def stream_data():
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        try:
            print(f"[DEBUG] Attempting to bind server to 127.0.0.1:{port}...")
            server_socket.bind(('127.0.0.1', port))
            server_socket.listen(1)
            print(f"📡 Financial data server listening on 127.0.0.1:{port}")
            print("⏳ Waiting for client to connect...")

            conn, addr = server_socket.accept()
            print(f"✅ Client connected from {addr}")

            transaction_count = 0
            while True:
                transaction = generator.generate_transaction()
                message = json.dumps(transaction) + '\n'
                conn.sendall(message.encode('utf-8'))

                transaction_count += 1
                if transaction_count % 10 == 0:
                    print(f"📈 Sent {transaction_count} transactions")

                time.sleep(interval)

        except Exception as e:
            print(f"⚠️ Server thread error: {e}")
        finally:
            print("[DEBUG] Closing server socket...")
            server_socket.close()

    thread = threading.Thread(target=stream_data, daemon=False)
    thread.start()
    time.sleep(1)  # Allow thread to start
    print("[DEBUG] Server thread started")
    return thread


import os, threading, time, subprocess
from tui import TUI


class ThreadBridge:
    """Thread-safe communication between backend and Terminal UI."""

    def __init__(self):
        """Initialize the thread bridge with a data dictionary and a lock."""
        self.data = {
            "quit_flag": False,
            'test_value_1': 0,
            'test_value_2': 0,
            'test_value_3': 0,
        }
        self.lock = threading.Lock()
    
    def update_data(self, key, value):
        """Thread-safe data update"""
        with self.lock: self.data[key] = value
    
    def get_data(self, key):
        """Thread-safe read"""
        with self.lock: return self.data.get(key)
    
    def get_all_data(self):
        """Thread-safe all data read"""
        with self.lock: return self.data.copy()

if __name__ == "__main__":

    # Create a terminal UI thread.
    thread_bridge = ThreadBridge()
    tui_thread = threading.Thread(target=TUI, args=(thread_bridge,))
    tui_thread.daemon = True
    tui_thread.start()

    # While the quit flag is not set...
    while thread_bridge.get_data('quit_flag') is False:
        
        # Do work.
        thread_bridge.update_data('test_value_1', thread_bridge.get_data('test_value_1') + 1)
        time.sleep(1)  # Simulate some processing time.

    # Clear the terminal screen before exiting.
    time.sleep(0.5)
    subprocess.run('clear' if os.name == 'posix' else 'cls', shell=True)
    
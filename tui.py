import time
from blessed import Terminal

class TUI:

    def __init__(self, thread_bridge) -> None:

        # Create a terminal instance.
        self.terminal = Terminal()

        # Reference to the thread bridge for communication.
        self.thread_bridge = thread_bridge

        # A flag used so when we go back a page, we know to rerender the FULL main page.
        self.render_main = True

        # Create a blessed terminal environment in fullscreen with the cursor hidden.
        with self.terminal.fullscreen(), self.terminal.hidden_cursor():
            self.page_main()

    def _draw_frame(self, header_text: str, footer_text: str) -> None:

        # Move cursor to 0,0 and clear the terminal.
        print(self.terminal.home + self.terminal.clear)

        # Print header.
        with self.terminal.location(0,0): print(self.terminal.black_on_yellow(self.terminal.center(header_text)))

        # Find the bottom of the screen.
        bottom = self.terminal.height - 1

        # Print the footer.
        with self.terminal.location(0, bottom): print(self.terminal.black_on_yellow(self.terminal.center(footer_text)), end="", flush=True)

        # Move cursor.
        self.terminal.location(0,1)

    def _menu(self, x: int, y: int, selected_item: int, items: list[str]) -> None:

        # For each item in the list...
        for i, item in enumerate(items):

            # If the item we're evaluating matches the selected item...
            if i == selected_item:

               # Print the highlighted item.
               with self.terminal.location(x,y+i): print(self.terminal.black_on_yellow(f">{item}"))

            # If its not the selected item...
            else:

                # Print the item un-highlighted.
                with self.terminal.location(x,y+i): print(f" {item}")

    def page_1(self):

        # Clear the screen and print a message.
        self._draw_frame("This is page 1", "Press any key to return to the main menu.")
        with self.terminal.location(0, 5): print(self.terminal.center("This is page 1. Press any key to return to the main menu."))

        # Wait for a key press.
        with self.terminal.cbreak(): 
            self.terminal.inkey()

        # Trigger redraw of main menu when returning.
        self.render_main = True  

    def page_2(self): pass
    def page_3(self): pass

    def page_main(self) -> None:
        
        # Declare the menu items.
        menu_items = ["page 1 ", "page 2 ", "page 3 "]
        page_list = [self.page_1, self.page_2, self.page_3]
        page_selection = 0

        # Debounce a bit.
        time.sleep(.2)

        # Track time for updates.
        last_update = time.time()

        # Loop indefinitely.
        while True:
            current_time = time.time()

            # Update once per second.
            if current_time - last_update >= 0.1:
                with self.terminal.location(1, 6): 
                    print(f" sample variable: {self.thread_bridge.get_data('test_value_1')} ")
                last_update = current_time

                # Redraw screen if needed.
                if self.render_main:
                    self._draw_frame("Main Menu", "q = quit")
                    self.render_main = False

                # Draw menu.
                self._menu(1, 2, page_selection, menu_items)

            # Get key press with 0.1 second timeout (non-blocking).
            with self.terminal.cbreak(): 
                key = self.terminal.inkey(timeout=0.1)

            # Respond to key (only if a key was pressed).
            if key:
                if key.name == "KEY_UP":
                    page_selection = (page_selection - 1) % len(menu_items)
                elif key.name == "KEY_DOWN":
                    page_selection = (page_selection + 1) % len(menu_items)
                elif key.name == "KEY_ENTER":
                    page_list[page_selection]()
                elif key.lower() == "q":
                    self.terminal.clear()
                    time.sleep(0.2)
                    self.thread_bridge.update_data("quit_flag", True)


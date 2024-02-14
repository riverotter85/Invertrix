import curses

class MenuController:

    def __init__(self, stdscr, imageFiles):
        self.stdscr = stdscr
        self.entries = imageFiles
        self.selectedEntry = 0
        self.selectedOptions = [0 for i in self.entries]
        self.executionStatus = ""

    def showMenu(self):
        options = ["None", "Vertical", "Horizontal", "Both"] # Configuration arguments for each entry

        # Clear the screen and display Invertrix title
        self.stdscr.clear()
        self.stdscr.addstr(1, 20, "INVERTRIX!")
        self.stdscr.addstr(2, 20, "==========")

        # Cursor for selected row/entry
        self.stdscr.addstr(self.selectedEntry+4, 0, ">>")

        # List out each entry, as well as the options (including which one is selected)
        for i in range(len(self.entries)):
            # Entry
            self.stdscr.addstr(i+4, 4, self.entries[i])

            # Start square bracket for options
            self.stdscr.addstr(i+4, 20, " [")

            # List out options
            prevOptionLength = 0
            for j in range(len(options)):
                # Case where option is currently selected
                if self.selectedOptions[i] == j:
                    self.stdscr.addstr(i+4, 22+prevOptionLength, options[j], curses.A_STANDOUT)
                # Case where option is not selected (default)
                else:
                    self.stdscr.addstr(i+4, 22+prevOptionLength, options[j])
                prevOptionLength += len(options[j])

                # Separate each option with ", "
                self.stdscr.addstr(i+4, 22+prevOptionLength, ", ")
                prevOptionLength += 2
            
            # Overwrite last comma instance with end square bracket
            self.stdscr.addstr(i+4, 22+prevOptionLength-2, "]")

        # Display options
        self.stdscr.addstr(len(self.entries)+5, 0, "ESC:")
        self.stdscr.addstr(len(self.entries)+5, 12, "Exit")
        self.stdscr.addstr(len(self.entries)+6, 0, "UP/DOWN:")
        self.stdscr.addstr(len(self.entries)+6, 12, "Navigate images")
        self.stdscr.addstr(len(self.entries)+7, 0, "LEFT/RIGHT:")
        self.stdscr.addstr(len(self.entries)+7, 12, "Set Invertrix choice")
        self.stdscr.addstr(len(self.entries)+8, 0, "ENTER")
        self.stdscr.addstr(len(self.entries)+8, 12, "Start!")

        # Below, display execution status (if any)
        self.stdscr.addstr(len(self.entries)+10, 0, self.executionStatus)

        # Show final output to screen
        self.stdscr.refresh()

    def setExecutionStatus(self, status):
        self.executionStatus = status
    
    def getKey(self):
        return self.stdscr.getch()

    def readKey(self):
        status = True

        key = self.getKey()
        if key == curses.KEY_LEFT:
            self.selectedOptions[self.selectedEntry] = (self.selectedOptions[self.selectedEntry] - 1) % 4
        elif key == curses.KEY_RIGHT:
            self.selectedOptions[self.selectedEntry] = (self.selectedOptions[self.selectedEntry] + 1) % 4
        elif key == curses.KEY_UP:
            self.selectedEntry = (self.selectedEntry - 1) % len(self.entries)
        elif key == curses.KEY_DOWN:
            self.selectedEntry = (self.selectedEntry + 1) % len(self.entries)
        elif key == curses.KEY_ENTER or key == 10 or key == 13:
            status = False
        elif key == 27:
            exit()

        return status
        
    def prompt(self):
        running = True
        while running:
            self.showMenu()
            running = self.readKey()
        
        return self.selectedOptions
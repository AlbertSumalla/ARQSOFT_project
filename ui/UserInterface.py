# ui/UserInterface.py
import os
from entities.core.SpreadsheetController import SpreadsheetController
from utilities.SpreadsheetRenderer import SpreadsheetRenderer
from entities.core.Spreadsheet import Spreadsheet

class UserInterface:
    def __init__(self):
        self.controller = SpreadsheetController()
        self.renderer = SpreadsheetRenderer()
        self.spreadsheet: Spreadsheet = None
        
    def display_menu(self) -> None:
        """
        Display the main menu of available commands.
        """
        print("\SPREADSHEET MENU:")
        print("C - Create new spreadsheet")
        print("E <coord> <new content> - Edit a cell")
        print("L <file_path> - Load spreadsheet from file")
        print("S <file_path> - Save spreadsheet to file")
        print("X - Exit the program")

    def run(self) -> None:
        running = True
        while running:
            self.display_menu()
            command_line = input("Enter command: ").strip()
            if not command_line:
                continue

            parts = command_line.split(maxsplit=2)
            command = parts[0].upper()

            match command:
                case 'C':
                    self.spreadsheet = self.controller.create_spreadsheet()

                case 'E':
                    if len(parts) < 3:
                        print("Usage: E <coord> <content>")
                        continue
                    coord = parts[1]
                    content = parts[2]
                    self.controller.set_cell_content(coord, content)

                case 'L':
                    if len(parts) < 2:
                        print("Missing file path.")
                        continue
                    path = parts[1]
                    try:
                        self.controller.load_spreadsheet(path)
                    except Exception:
                        print("Invalid path or file name")

                case 'S':
                    if len(parts) < 2:
                        print("Missing file path.")
                        continue
                    path = parts[1]
                    try:
                        self.controller.save_spreadsheet_to_file(path)
                    except Exception:
                        print("Invalid path or file name")

                case 'X':
                    running = False
                    continue

                case _:  # default case
                    print("Invalid command.")
                    continue

            self.renderer.display_spreadsheet(self.spreadsheet)




if __name__ == '__main__':
    ui = UserInterface()
    ui.run()
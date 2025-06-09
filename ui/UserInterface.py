# ui/UserInterface.py
import os

from entities.core.SpreadsheetController import SpreadsheetController
from utilities.SpreadsheetRenderer import SpreadsheetRenderer

class UserInterface:
    def __init__(self):
        # Initialize controller with this UI instance
        self.controller = SpreadsheetController(self)

    def display_cell_formula(self, coord: str) -> None:
        """
        Display the formula defined in a specific cell.

        :param coord: the cell coordinate (e.g., 'A1')
        """
        try:
            formula = self.controller.get_cell_formula_expression(coord)
            print(f"Formula at {coord}: {formula}")
        except Exception as e:
            print(f"Error displaying formula at {coord}: {e}")

    def display_menu(self) -> None:
        """
        Display the main menu of available commands.
        """
        print("Execute command:\n")
        print("Enter 'rf' to read commands from a text file")
        print("Enter 'c' to create a new Spreadsheet")
        print("Enter 'e' to edit a cell")
        print("Enter 'l' to load a Spreadsheet from a file")
        print("Enter 's' to save the Spreadsheet to a file")
        print("Enter 'w' to show the Spreadsheet")
        print("Enter 'x' to exit the program")

    def run(self) -> None:
        """
        Main loop: read user commands and dispatch to the controller.
        """
        running = True
        while running:
            self.display_menu()
            command = input().strip()

            if command == 'rf':
                filepath = input("Enter the complete name of the file (path + name + extension): ").strip()
                if not os.path.exists(filepath):
                    print("Invalid path or file name")
                    continue
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                    i = 0
                    while i < len(lines):
                        parts = lines[i].strip().split()
                        if not parts:
                            i += 1
                            continue
                        cmd = parts[0]
                        if cmd == 'c':
                            self.controller.create_spreadsheet()
                        elif cmd == 'e' and len(parts) >= 3:
                            self.controller.edit_cell(parts[1], parts[2])
                        elif cmd == 'l':
                            i += 1
                            path_line = lines[i].strip()
                            try:
                                self.controller.load_spreadsheet(path_line)
                            except Exception:
                                print("Invalid path or file name")
                        elif cmd == 's':
                            i += 1
                            path_line = lines[i].strip()
                            try:
                                self.controller.save_spreadsheet(path_line)
                            except Exception:
                                print("Invalid path or file name")
                        i += 1
                    print(self.controller.show_spreadsheet())
                except Exception:
                    print("Error reading commands from file")

            elif command == 'c':
                self.controller.create_spreadsheet()
                print(self.controller.show_spreadsheet())

            elif command == 'e':
                coords = input("Enter the cell coordinates: ").strip()
                new_content = input("Enter the new cell content: ").strip()
                self.controller.edit_cell(coords, new_content)
                print(self.controller.show_spreadsheet())

            elif command == 'l':
                filepath = input("Enter the complete name of the spreadsheet (path + filename + extension): ").strip()
                try:
                    self.controller.load_spreadsheet(filepath)
                    print(self.controller.show_spreadsheet())
                except Exception:
                    print("Invalid path or file name")

            elif command == 's':
                filepath = input("Enter the path and name of the spreadsheet (path + name + extension): ").strip()
                try:
                    self.controller.save_spreadsheet(filepath)
                    print(self.controller.show_spreadsheet())
                except Exception:
                    print("Invalid path or file name")

            elif command == 'w':
                print(self.controller.show_spreadsheet())

            elif command == 'x':
                running = False

            else:
                print("Invalid command, please enter it again")


if __name__ == '__main__':
    ui = UserInterface()
    ui.run()

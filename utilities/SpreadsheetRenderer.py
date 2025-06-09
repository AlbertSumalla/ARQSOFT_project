class SpreadsheetRenderer:
    ##
    # @brief Displays the empty spreadsheet in the console.
    # @param spreadsheet The spreadsheet instance.
    # @return None.
    def display_spreadsheet(self, spreadsheet) -> str:
        """
        Generate and return a string representation of the spreadsheet's current values.

        The output consists of row and column separators, followed by each cell's
        content (empty if unset), arranged in a grid.

        :param spreadsheet: an instance of the Spreadsheet model
        :return: multi-line string representing the spreadsheet
        """
        # Determine the number of rows and columns
        num_rows = spreadsheet.get_last_row()
        last_col = spreadsheet.get_last_column()  # e.g. 'A', 'B', ..., 'Z'
        # Calculate number of columns assuming single-letter columns
        num_columns = ord(last_col) - ord('A') + 1

        output = ""
        for row in range(1, num_rows + 1):
            # Draw horizontal separator line
            output += "+--" + "--" * num_columns + "--+\n"
            # Draw row values
            output += "| "
            for col in range(1, num_columns + 1):
                coord = self.int_to_string(col) + str(row)
                cell_str = ""
                try:
                    # Retrieve cell object and its value
                    cell = spreadsheet.get_cell(coord)
                    value = cell.get_value()
                    # Convert the value to its string form
                    cell_str = value.get_my_string()
                except Exception:
                    # Leave empty if any error occurs (e.g., no cell)
                    cell_str = ""
                # Append cell content and column separator
                output += cell_str + " | "
            # End of row
            output += "\n"
        return output


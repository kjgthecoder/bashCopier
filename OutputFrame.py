import tkinter as tk
import dark_mode_theme as col
import pyperclip

class OutputFrame(tk.Frame): 
    def __init__(self, parent, event_handler): 
        super().__init__(parent, width=400, height=400)
        self.event_handler = event_handler
        self.event_handler.subscribe("PASTE_EVENT_SCRAPE", self.begin_paste_process) # Subscribing to PASTE_EVENT_SCRAPE w/c is published by Root. 
        self.event_handler.subscribe("CLEAR_EVENT", self.begin_clear_process)

        # Parsed Code
        self.parsed_code = []
        # Array of Formatted Code Rows 
        self.formatted_code_rows_displayed = []

        # Left side 
        self.left_side = tk.Frame(self, bg="#007991", width=75, height=400)
        self.left_side.pack(side="left", fill="both", expand=True)

        # Right side 
        self.right_side = tk.Frame(self, bg=col.dark_bg, width=325, height=400)
        self.right_side.pack(side="left", fill="both", expand=True)

    def begin_paste_process(self, event, data): 
        print(f"OUTPUT_FRAME: {event} received -> begin_paste_process")
        print("\tAdding new row to background")
        # Clearing mother frame 
        self.clear_code_rows()
        # Setting data to be: parse_code 
        self.parsed_code = data # data = code_input_parsed
        print(data)
        # Adjusting size of mother window 
        self.update_window_size_on_paste()
        self.create_code_rows()

    def create_code_rows(self): 
        """
        Creating i rows based off the number of lines from the parsed code.
        """
        y_coord = 0 
        for i in range(len(self.parsed_code)):  
            new_row = FormattedCodeRows(self, i, self.parsed_code[i], self.master_indent_method, self.master_dedent_method)
            new_row.place(x=0, y=y_coord)
            y_coord += new_row.winfo_reqheight() 
            self.formatted_code_rows_displayed.append(new_row)

    def begin_clear_process(self, event, data): 
        print(f"OUTPUT_FRAME: {event} received -> begin_clear_process")
        self.clear_code_rows() 
        self.update_window_size_on_clear()

    def clear_code_rows(self): 
        """
        A hack that -> Clears all the FormattedCodeRows created from the mother frame
        """
        if (self.formatted_code_rows_displayed == []): 
            print("outputframe_class_setup: no FormattedCodeRows need to be deleted")
        while (self.formatted_code_rows_displayed != []): 
            code_row_to_delete = self.formatted_code_rows_displayed.pop() 
            code_row_to_delete.destroy() 

    def master_indent_method(self, row_index):
        """
        A hack that -> Tells which code_row to indent 
        """
        self.formatted_code_rows_displayed[row_index].indent_code_text()
        self.update_final_output()

    def master_dedent_method(self, row_index): 
        """
        A hack that -> Tell which code_row to dedent 
        """
        self.formatted_code_rows_displayed[row_index].dedent_code_text() 
        self.update_final_output()

    def update_final_output(self): 
        """ 
        Whenever a change is made to the output of code lines, joins the list of formatted code 
        and automatically copies that to the user's clipboard. 
        """
        final_output = ""
        for formatted_code_row in self.formatted_code_rows_displayed: 
            final_output += f"{formatted_code_row.code_text}\n"
        # Adding joined to clipboard 
        pyperclip.copy(final_output)

    def update_window_size_on_paste(self): 
        """
        Updates window size when rows created end up being more than what is provided by the mother window 
        """
        row_height = 50 
        num_rows = len(self.parsed_code)
        new_win_height = 50 * num_rows 
        if (new_win_height > 400): 
            self.winfo_toplevel().geometry(f"800x{new_win_height}")
            self.event_handler.publish("WINDOW_CHANGE_EVENT", new_win_height) # Sends an the Input Frame to adjust the text box
                                                              # pure eye canday, nothing functional

    def update_window_size_on_clear(self): 
        """
        Updates window size when rows are cleared. If window size grew, shrinks it back to 400 
        """
        window_height = self.winfo_height()
        print(f"Window height: {window_height}")
        if (window_height > 400): 
            print("I am here")
            self.event_handler.publish("WINDOW_CLEAR_EVENT", data=None) # Sends an event to the Input frame to reset
                                                             # textbox back to the original size when the clear button is hit
            self.winfo_toplevel().geometry(f"800x{400}") # Shrinking the entire ewindow 
            

class FormattedCodeRows(tk.Frame): 
    """
    A class that holds all the information and parameters needed for each line of code
    Gives user the option to indent or dedent their to format code more, and automatically 
    copies each change to the clipboard. 
    """
    def __init__(self, parent, number_line, code_text, master_indent, master_dedent): 
        # Extra Options -> , highlightcolor="black", highlightthickness=1)
        super().__init__(parent, 
                         bg="#D0E562", 
                         width=400, 
                         height=50)
        # Variables 
        self.number_line = number_line # Int & Array w/ in parent array
        self.number_line_str = str(number_line + 1) # Number line of code
        self.code_text = code_text # The individual line from the parsed code

        # ------------------------------ NUMBER_LINE_WRAPPER ----------------------------------------------
        # Same color as BackGround.left_side
        # Extra options -> , highlightcolor="black", highlightthickness=1)
        self.number_line_wrapper = tk.Frame(self, bg="#007991", width=75, height=50)
        self.number_line_wrapper.place(x=0, y=0)  

        # ------------------ TEST BUTTON WRAPPER ------------------------------------------------------------
        self.button_wrapper = tk.Frame(bg="blue")
        self.button_wrapper.place(in_=self.number_line_wrapper, relwidth=.85, relheight=.5, relx=.075, rely=.25)

        # BUTTONS --------------------------------------------------------------------------------------------
        # LINE NUMBER
        self.number_line_button = tk.Button(self.button_wrapper, 
                                    text=self.number_line_str.zfill(2), 
                                    bg="#E9D985", 
                                    width=2, 
                                    height=2,
                                    padx=2,
                                    pady=2,
                                    state="disabled",
                                    fg="#1E1E1E") 
        self.number_line_button.pack(side="left") 

        # UNINDENT BUTTON 
        self.unindent_button = tk.Button(self.button_wrapper, 
                                text="\u2190", 
                                width=1, 
                                height=1, 
                                bg="#E9D985", 
                                padx=2, 
                                pady=2, 
                                command=lambda: master_dedent(self.number_line))
        self.unindent_button.pack(side="left")

        # INDENT BUTTON 
        self.indent_button = tk.Button(self.button_wrapper, 
                                text="\u2192", 
                                width=1, 
                                height=1, 
                                bg="#E9D985", 
                                padx=2, 
                                pady=2, 
                                command=lambda: master_indent(self.number_line))
        self.indent_button.pack(side="left")  

        # ----------------------------------------- FORMATTED CODE SIDE ----------------------------------------------
        # Formatted Code Side 
        # Extra options -> , highlightbackground="black", highlightthickness=1)
        self.formatted_code_wrapper = tk.Frame(self, bg=col.dark_bg, width=375, height=50, padx=5) 
        self.formatted_code_wrapper.place(x=75, y=0)

        self.actual_code_line = tk.Label(text=self.code_text,
                                         font=("Consolas", 10), 
                                         bg=col.dark_bg, 
                                         fg=col.dark_fg)
        self.actual_code_line.place(in_=self.formatted_code_wrapper, relheight=.50, rely=.25)            

    def indent_code_text(self, indent_size=4): 
        """
        Adds 4 spaces to the specified line 
        """
        spaces = " " * indent_size # Literally, indent_size ' ' chars 
        new_code_text = spaces + self.code_text
        self.code_text = new_code_text 
        self.actual_code_line.config(text=self.code_text)

    def dedent_code_text(self, indent_size=4): 
        """
        If there are spaces that exist, removes 4 spaces from the specified line 
        """
        leading_spaces = len(self.code_text) - len(self.code_text.lstrip())
        indent_level = leading_spaces // indent_size
        if (((leading_spaces % indent_size) == 0) and (indent_level > 0)): 
            indent_level -= 1 
            stripped_text = self.code_text.lstrip() 
            spaces = " " * (indent_size * indent_level) 
            new_text = spaces + stripped_text 
            self.code_text = new_text 
            self.actual_code_line.config(text=self.code_text) 
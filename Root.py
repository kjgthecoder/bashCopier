import EventHandler 
import tkinter as tk 
import re 

class Root:
    def __init__(self, event_handler): 
        # Root
        self.root = tk.Tk() 
        self.root.geometry("800x400")
        self.root.title("EventHandlerPractice")
        self.root.resizable(False, False)
        self.root.config(bg="#F7DCED")

        self.code_input = "" # bash_script 
        self.code_lines_to_format = []

        self.event_handler = event_handler
        self.event_handler.subscribe("PASTE_EVENT", self.handle_paste_event) # Subscribing to PASTE_EVENT
        self.event_handler.subscribe("CLEAR_EVENT", self.handle_clear_event) # Subscribing to CLEAR_EVENT

    def scrapeDaNumbas(self):
        """
        Strips text from line numbers & splits script into an array. 
        """
        lines = self.code_input.splitlines()
        for i in range(len(lines)):
            # Checking to see if there are numbers lines in the beginning using regex 
            num_regex = re.match(r"^(\d+)", lines[i])
            if (num_regex != None): 
                num_str = num_regex.group(1)
            else: 
                num_str = None 
            if (self.try_parse_int(num_str)): 
                lines[i] = lines[i].split(' ', 1)[-1].lstrip()
            else: 
                lines[i] = lines[i].lstrip() 
        self.code_lines_to_format = lines

    def try_parse_int(self, num_str): 
        """
        Returns true or false if string passed can be a number or not
        """
        if num_str == None: 
            return False 
        try: 
            number = int(num_str) 
            return True 
        except ValueError: 
            return False 

    def formatBashScript(self, indent_size=4):
        """
        Adds indentation to final output. 
        """
        indented_code = ""
        indent_level = 0 

        for line in self.code_lines_to_format:
            stripped_line = line.strip()

            if stripped_line.startswith(("if", "elif", "else", "for", "while", "until", "case")):
                indented_line = " " * (indent_size * indent_level) + line
                indent_level += 1
            elif stripped_line.startswith(("done", "fi")):
                indent_level -= 1
                indented_line = " " * (indent_size * indent_level) + line
            else:
                indented_line = " " * (indent_size * indent_level) + line

            indented_code += indented_line + "\n"
        
        return indented_code.splitlines()

    def handle_paste_event(self, event, data): 
        """
        Receieves "PASTE_EVENT" from InputFrame, which then formats the code a bit 
        and puts the output of the now formatted code into the OutputFrame. 
        It then sends a "PASTE_EVENT_SCRAPE" event to OutputFrame
        """
        print("\nRoot: handle_paste_event")
        # Formatting text 
        self.code_input = data
        self.scrapeDaNumbas() 
        final_out = self.formatBashScript() 
        # Sending PASTE_EVENT_SCRAPE to Outputframe along w/ formatted code (code_input_parsed)
        self.event_handler.publish("PASTE_EVENT_SCRAPE", final_out)

    def handle_clear_event(self, event, data): 
        """
        Throws a signal to  the output frame to begin chain of events for when 
        the clear button is pressed. 
        """
        print("\nRoot: handle_clear_event") 
        





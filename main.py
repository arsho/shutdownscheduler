import subprocess
import os
import tkinter as tk
import platform


class Application(tk.Frame):
    def __init__(self, master = None):
        super().__init__(master)
        self.set_constants()
        self.pack()
        self.max_columns = 5
        self.current_row = 0
        self.set_initial_window()
        self.create_widgets()

    def set_constants(self):
        self.os = self.get_os().lower()
        self.program_title = "Shutdown Scheduler - arsho"
        self.header_title = "Shutdown Scheduler"
        self.shutdown_helper_text = "Schedule shutdown between 5 to 120 minutes"

    def set_initial_window(self):
        self.set_window_title()
        self.set_window_size(width = 1080, height = 550)

    def set_window_size(self, width = 720, height = 250):
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x_position = int((screen_width/4)-(width/4))
        y_position = int((screen_height/2)-(height/2))
        root.geometry('{}x{}+{}+{}'.format(width, height, x_position, y_position))        

    def set_window_title(self):
        root.title(self.program_title)

    def create_widgets(self):
        self.create_header_label()
        self.create_command_output_label()
        self.create_shutdown_buttons([5, 15, 30, 45, 60, 65, 75, 90, 105, 120])
        self.create_shutdown_now_button()
        self.create_shutdown_cancel_button()
        self.create_exit_button()

    def create_header_label(self):
        self.header = tk.Label(self)
        self.header["text"] = self.header_title
        self.header["font"] = ("Arial Bold", 24)
        self.header.grid(row=self.current_row,
                         columnspan=self.max_columns,
                         padx=10,
                         pady=10,
                         sticky=tk.W+tk.E+tk.S+tk.N)
        self.current_row+=1

    def create_command_output_label(self):
        self.command_output = tk.Label(self)
        self.command_output["font"] = ("Arial", 14)
        self.command_output["text"] = self.shutdown_helper_text
        self.command_output.grid(row=self.current_row,
                                 columnspan=self.max_columns,
                                 sticky=tk.W+tk.E+tk.S+tk.N)
        self.current_row+=1

    def create_shutdown_buttons(self, times):
        times_length = len(times)
        column=0
        for i in range(times_length):
            value = times[i]
            if i%self.max_columns==0:
                self.current_row+=1
                column=0
            shutdown_btn = tk.Button(self)
            shutdown_btn["text"] = "{} minutes".format(value)
            shutdown_btn["font"] = ("Arial Bold", 18)
            shutdown_btn["command"] = lambda value=value:self.shutdown(value)
            shutdown_btn.grid(row=self.current_row,
                              column=column,
                              padx=5,
                              pady=5,
                              sticky=tk.W+tk.E+tk.S+tk.N)
            column+=1
        self.current_row+=1

    def create_shutdown_now_button(self):
        self.shutdown_now_button = tk.Button(self)
        self.shutdown_now_button["text"]="Shutdown Now"
        self.shutdown_now_button["font"] = ("Arial Bold", 18)
        self.shutdown_now_button["fg"]="white"
        self.shutdown_now_button["bg"]="red"        
        self.shutdown_now_button["command"]=lambda value=0:self.shutdown(value)
        self.shutdown_now_button.grid(row=self.current_row,
                                      padx=5,
                                      pady=5,
                                      columnspan=self.max_columns,
                                      sticky=tk.W+tk.E+tk.S+tk.N)
        self.current_row+=1

    def create_shutdown_cancel_button(self):
        self.shutdown_cancel_button = tk.Button(self)
        self.shutdown_cancel_button["text"]="Cancel Shutdown"
        self.shutdown_cancel_button["font"] = ("Arial Bold", 18)
        self.shutdown_cancel_button["fg"]="blue"
        self.shutdown_cancel_button["command"]=self.shutdown_cancel
        self.shutdown_cancel_button.grid(row=self.current_row,
                                      padx=5,
                                      pady=5,
                                      columnspan=self.max_columns,
                                      sticky=tk.W+tk.E+tk.S+tk.N)
        self.current_row+=1

    def create_exit_button(self):
        self.exit_button = tk.Button(self)
        self.exit_button["text"] = "Exit"
        self.exit_button["font"] = ("Arial Bold", 18)
        self.exit_button["fg"]="red"
        self.exit_button["command"]=root.destroy
        self.exit_button.grid(row=self.current_row,
                       columnspan=self.max_columns,
                       padx=5,
                       pady=5,
                       sticky=tk.W+tk.E+tk.S+tk.N)
        self.current_row+=1

    def execute_command(self, command):
        command = command.split()
        try:
            command_process = subprocess.run(command,
                                             stdout=subprocess.PIPE,
                                             stderr=subprocess.PIPE)
            output = command_process.stdout.decode('utf-8')            
            output_message = "{}".format(output)
            error = command_process.stderr.decode('utf-8')            
            error_message = "{}".format(error)
            self.show_message(output_message)
            self.show_message(error_message)
        except Exception as error:
            command_error_message = str(error)
            self.show_message(command_error_message)

    def show_message(self, message):
        if message!="":
            print(message)
            self.command_output["text"] = message

    def shutdown_cancel(self):
        command = 'shutdown -c'
        if self.os == "windows":
            command = 'shutdown -a -y'
        self.command_output["text"] = "Cancelled scheduled shutdown"
        self.execute_command(command)

    def shutdown(self, value):
        command = 'shutdown -h {}'.format(value)
        if self.os == "windows":
            command = 'shutdown -s -t {} -y'.format(value*60)
        self.execute_command(command)

    def get_os(self):
        return platform.system()

if __name__ == '__main__':
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()   

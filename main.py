import pyvisa
import tkinter as tk
from tkinter import messagebox

class FunctionGeneratorApp:
    def __init__(self, master):
        self.master = master
        master.title("Keysight 33210A Controller")

        self.rm = None
        self.instrument = None

        # init output button
        self.output_button = tk.Button(master, text="Output ON", command=self.toggle_output)
        self.output_button.pack()

        self.output_status = tk.Label(master, text="Output status: OFF")
        self.output_status.pack()

        self.sin_button = tk.Button(master, text="Sine Wave", command=lambda: self.set_func('SIN'))
        self.sin_button.pack()

        self.dc_button = tk.Button(master, text="DC Wave", command=lambda: self.set_func('DC'))
        self.dc_button.pack()

        self.square_button = tk.Button(master, text="Square Wave", command=lambda: self.set_func('SQU'))
        self.square_button.pack()

        self.square_button = tk.Button(master, text="Pulse Wave", command=lambda: self.set_func('PULS'))
        self.square_button.pack()

        self.square_button = tk.Button(master, text="Ramp Wave", command=lambda: self.set_func('RAMP'))
        self.square_button.pack()

        self.square_button = tk.Button(master, text="Noise Wave", command=lambda: self.set_func('NOIS'))
        self.square_button.pack()

        self.func_status = tk.Label(master, text="Current Waveform: DC")
        self.func_status.pack()

        #connect to the keysight instrument
        self.keysight_connect()

    def keysight_connect(self):
        try:
            self.rm = pyvisa.ResourceManager('@py')
            instrument_address = 'TCPIP0::169.254.2.20::INSTR'
            self.instrument = self.rm.open_resource(instrument_address)
            
            idn = self.instrument.query('*IDN?')
            messagebox.showinfo("Connection Status", f"Connected to: {idn}")
            
            # Initialize the function generator
            self.instrument.write('*RST') # reset instrument to default settings
            self.instrument.write('*CLS') # clear the status registers
            
            #default settings when initilized
            self.instrument.write('FUNC DC')
            self.instrument.write('FREQ 4KHZ')
            self.instrument.write('VOLT:OFFS 1')  # Set the offset voltage to 1V

        except Exception as e:
            messagebox.showerror("Connection Error", str(e))
            self.output_button.config(state=tk.DISABLED)
    def set_func(self, func_type):
        try:
            if func_type == 'SIN':
                self.instrument.write('FUNC SIN')
                self.instrument.write('FREQ 1KHZ')  # Set frequency for SIN wave
                self.instrument.write('VOLT 2')     # Set amplitude for SIN wave
            elif func_type == 'DC':
                self.instrument.write('FUNC DC')
                self.instrument.write('VOLT:OFFS 1')  # Set the offset voltage to 1V for DC
            elif func_type == 'SQU':
                self.instrument.write('FUNC SQU')
                self.instrument.write('FREQ 1KHZ') 
                self.instrument.write('VOLT 2') 
            elif func_type == 'RAMP':
                self.instrument.write('FUNC RAMP')
                self.instrument.write('FREQ 1KHZ') 
                self.instrument.write('VOLT 2')     
            elif func_type == 'NOIS':
                self.instrument.write('FUNC NOIS')
                self.instrument.write('FREQ 1KHZ') 
                self.instrument.write('VOLT 2')   
            elif func_type == 'PULS':
                self.instrument.write('FUNC PULS')
                self.instrument.write('FREQ 1KHZ') 
                self.instrument.write('VOLT 2')     
            
            self.func_status.config(text=f"Waveform Set {func_type} waveform selected.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def toggle_output(self):
        try:
            current_status = self.instrument.query('OUTP?').strip()
            if current_status == '1':
                self.instrument.write('OUTP OFF')
                self.output_button.config(text="Output ON")
                self.output_status.config(text="Output status: OFF")
            else:
                self.instrument.write('OUTP ON')
                self.output_button.config(text="Output OFF")
                self.output_status.config(text="Output status: ON")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def close(self):
        if self.instrument:
            self.instrument.close()
        self.master.quit()

def main():
    root = tk.Tk()
    app = FunctionGeneratorApp(root)
    root.protocol("WM_DELETE_WINDOW", app.close)
    root.geometry('520x300')
    root.mainloop()

if __name__ == "__main__":
    main()

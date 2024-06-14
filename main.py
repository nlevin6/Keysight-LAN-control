import pyvisa

def main():
    # print("Available VISA backends:", pyvisa.highlevel.list_backends())

    # Initialize VISA resource manager
    rm = pyvisa.ResourceManager('@py') # this actually uses the pyvisa_py library

    # Replace 'TCPIP0::192.168.1.100::INSTR' with the actual IP address of your Keysight 33210A
    instrument_address = 'TCPIP0::169.254.2.20::INSTR'

    try:
        # Open a connection to the instrument
        instrument = rm.open_resource(instrument_address)

        # Query the instrument's ID
        idn = instrument.query('*IDN?')
        print(f"Connected to: {idn}")

        instrument.write('OUTP ON') # turn on the output button, set to OFF if you want it off
        instrument.write('FUNC SIN') # SIN wave
        instrument.write('FREQ 3KHZ') # frequency
        instrument.write('VOLT 4') # voltage amplitude
        

        # Query the current waveform settings
        frequency = instrument.query('FREQ?')
        amplitude = instrument.query('VOLT?')
        output_status = instrument.query('OUTP?')
        print(f"Output status: {'ON' if output_status.strip() == '1' else 'OFF'}")
        print(f"Waveform set to sine with frequency {frequency.strip()} and amplitude {amplitude.strip()} V")

        # Close the connection
        instrument.close()
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()

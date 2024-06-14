import pyvisa

def main():
    # print("Available VISA backends:", pyvisa.highlevel.list_backends())

    # Initialize VISA resource manager
    rm = pyvisa.ResourceManager('@py')

    # Replace 'TCPIP0::192.168.1.100::INSTR' with the actual IP address of your Keysight 33210A
    instrument_address = 'TCPIP0::169.254.2.20::INSTR'

    try:
        # Open a connection to the instrument
        instrument = rm.open_resource(instrument_address)

        # Query the instrument's ID
        idn = instrument.query('*IDN?')
        print(f"Connected to: {idn}")

        # Set the waveform to a sine wave with a freq of 1kHz and amplitude of 2V
        instrument.write('FUNC SIN')
        instrument.write('FREQ 1KHZ')
        instrument.write('VOLT 2')

        # Query the current waveform settings
        frequency = instrument.query('FREQ?')
        amplitude = instrument.query('VOLT?')
        print(f"Waveform set to sine with frequency {frequency.strip()} and amplitude {amplitude.strip()} V")

        # Close the connection
        instrument.close()
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()

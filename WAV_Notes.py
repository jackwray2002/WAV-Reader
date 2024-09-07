from os import path, chdir
import numpy as np
from scipy.signal import resample
from scipy.io import wavfile

# Frequencies of the notes from the second octave
NOTES_ARRAY = np.array([
65.40639, 69.29566, 73.41619, 77.78175, 82.40689, 87.30706,
92.49861, 97.99886, 103.8262, 110.0000, 116.5409, 123.4708], dtype=np.float64)

def generate_notes(path: path, instrument_name: str) -> None:
    NUM_OCTAVES = 6
    NUM_NOTES = 12

    # Original sound data
    wav_file = wavfile.read(path)

    # List to store arrays for resampled sounds
    note_data_array = [None] * (NUM_OCTAVES*NUM_NOTES)

    # Define parameters
    sound = wav_file[1]
    sampling_rate = wav_file[0]
    sampling_length = len(wav_file[1])
    base_frequency = 1 / (1 / sampling_rate * sampling_length)

    # Calculate and store notes resampled at frequencies C2-B7 in note_data_array
    for i in range(NUM_OCTAVES):
        for j in range(NUM_NOTES):
            temp_note_frequency = 2**i * NOTES_ARRAY[j]
            if base_frequency > temp_note_frequency:
                frequency_ratio = temp_note_frequency / base_frequency
            else:
                frequency_ratio = base_frequency / temp_note_frequency

            temp_sound = resample(sound, round(sampling_length * frequency_ratio))
            temp_sound = temp_sound.astype(np.uint8)
            note_data_array[12 * i + j] = temp_sound

    FILE = open(instrument_name+".txt", "a")

    # Print out macros for byte array sizes
    for i in range(NUM_OCTAVES):
        for j in range(NUM_NOTES):
            if j == 0:
                FILE.write(f"#define {instrument_name.upper()}_C{i+2}_SIZE "+
                f"{len(note_data_array[12 * i + j])}")
            elif j == 1:
                FILE.write(f"#define {instrument_name.upper()}_CSHARP{i+2}_SIZE "+
                f"{len(note_data_array[12 * i + j])}")
            elif j == 2:
                FILE.write(f"#define {instrument_name.upper()}_D{i+2}_SIZE "+
                f"{len(note_data_array[12 * i + j])}")
            elif j == 3:
                FILE.write(f"#define {instrument_name.upper()}_DSHARP{i+2}_SIZE "+
                f"{len(note_data_array[12 * i + j])}")
            elif j == 4:
                FILE.write(f"#define {instrument_name.upper()}_E{i+2}_SIZE "+
                f"{len(note_data_array[12 * i + j])}")
            elif j == 5:
                FILE.write(f"#define {instrument_name.upper()}_F{i+2}_SIZE "+
                f"{len(note_data_array[12 * i + j])}")
            elif j == 6:
                FILE.write(f"#define {instrument_name.upper()}_FSHARP{i+2}_SIZE "+
                f"{len(note_data_array[12 * i + j])}")
            elif j == 7:
                FILE.write(f"#define {instrument_name.upper()}_G{i+2}_SIZE "+
                f"{len(note_data_array[12 * i + j])}")
            elif j == 8:
                FILE.write(f"#define {instrument_name.upper()}_GSHARP{i+2}_SIZE "+
                f"{len(note_data_array[12 * i + j])}")
            elif j == 9:
                FILE.write(f"#define {instrument_name.upper()}_A{i+2}_SIZE "+
                f"{len(note_data_array[12 * i + j])}")
            elif j == 10:
                FILE.write(f"#define {instrument_name.upper()}_ASHARP{i+2}_SIZE "+
                f"{len(note_data_array[12 * i + j])}")
            elif j == 11:
                FILE.write(f"#define {instrument_name.upper()}_B{i+2}_SIZE "+
                f"{len(note_data_array[12 * i + j])}")
    FILE.write(end='\n')

    # Print out data section definitions for byte arrays
    FILE.write("#if __TI_COMPILER_VERSION__")
    pragma_string = "#pragma DATA_SECTION("
    for i in range(NUM_OCTAVES):
        for j in range(NUM_NOTES):
            if j == 0:
                FILE.write(f"{pragma_string}{instrument_name.upper()}_C{i+2}"+
                f", \".{instrument_name.lower()}_c{i+2}\")")
            elif j == 1:
                FILE.write(f"{pragma_string}{instrument_name.upper()}_CSHARP{i+2}"+
                f", \".{instrument_name.lower()}_csharp{i+2}\")")
            elif j == 2:
                FILE.write(f"{pragma_string}{instrument_name.upper()}_D{i+2}"+
                f", \".{instrument_name.lower()}_d{i+2}\")")
            elif j == 3:
                FILE.write(f"{pragma_string}{instrument_name.upper()}_DSHARP{i+2}"+
                f", \".{instrument_name.lower()}_dsharp{i+2}\")")
            elif j == 4:
                FILE.write(f"{pragma_string}{instrument_name.upper()}_E{i+2}"+
                f", \".{instrument_name.lower()}_e{i+2}\")")
            elif j == 5:
                FILE.write(f"{pragma_string}{instrument_name.upper()}_F{i+2}"+
                f", \".{instrument_name.lower()}_f{i+2}\")")
            elif j == 6:
                FILE.write(f"{pragma_string}{instrument_name.upper()}_FSHARP{i+2}"+
                f", \".{instrument_name.lower()}_fsharp{i+2}\")")
            elif j == 7:
                FILE.write(f"{pragma_string}{instrument_name.upper()}_G{i+2}"+
                f", \".{instrument_name.lower()}_g{i+2}\")")
            elif j == 8:
                FILE.write(f"{pragma_string}{instrument_name.upper()}_GSHARP{i+2}"+
                f", \".{instrument_name.lower()}_gsharp{i+2}\")")
            elif j == 9:
                FILE.write(f"{pragma_string}{instrument_name.upper()}_A{i+2}"+
                f", \".{instrument_name.lower()}_a{i+2}\")")
            elif j == 10:
                FILE.write(f"{pragma_string}{instrument_name.upper()}_ASHARP{i+2}"+
                f", \".{instrument_name.lower()}_asharp{i+2}\")")
            elif j == 11:
                FILE.write(f"{pragma_string}{instrument_name.upper()}_B{i+2}"+
                f", \".{instrument_name.lower()}_b{i+2}\")")
    FILE.write(end='\n')

    # Print out byte array definitions
    for i in range(NUM_OCTAVES):
        for j in range(NUM_NOTES):
            if j == 0:
                FILE.write(f"const uint8_t {instrument_name.upper()}_C{i+2}"+
                f"[{len(note_data_array[12 * i + j])}] = ", end='')
            elif j == 1:
                FILE.write(f"const uint8_t {instrument_name.upper()}_CSHARP{i+2}"+
                f"[{len(note_data_array[12 * i + j])}] = ", end='')
            elif j == 2:
                FILE.write(f"const uint8_t {instrument_name.upper()}_D{i+2}"+
                f"[{len(note_data_array[12 * i + j])}] = ", end='')
            elif j == 3:
                FILE.write(f"const uint8_t {instrument_name.upper()}_DSHARP{i+2}"+
                f"[{len(note_data_array[12 * i + j])}] = ", end='')
            elif j == 4:
                FILE.write(f"const uint8_t {instrument_name.upper()}_E{i+2}"+
                f"[{len(note_data_array[12 * i + j])}] = ", end='')
            elif j == 5:
                FILE.write(f"const uint8_t {instrument_name.upper()}_F{i+2}"+
                f"[{len(note_data_array[12 * i + j])}] = ", end='')
            elif j == 6:
                FILE.write(f"const uint8_t {instrument_name.upper()}_FSHARP{i+2}"+
                f"[{len(note_data_array[12 * i + j])}] = ", end='')
            elif j == 7:
                FILE.write(f"const uint8_t {instrument_name.upper()}_G{i+2}"+
                f"[{len(note_data_array[12 * i + j])}] = ", end='')
            elif j == 8:
                FILE.write(f"const uint8_t {instrument_name.upper()}_GSHARP{i+2}"+
                f"[{len(note_data_array[12 * i + j])}] = ", end='')
            elif j == 9:
                FILE.write(f"const uint8_t {instrument_name.upper()}_A{i+2}"+
                f"[{len(note_data_array[12 * i + j])}] = ", end='')
            elif j == 10:
                FILE.write(f"const uint8_t {instrument_name.upper()}_ASHARP{i+2}"+
                f"[{len(note_data_array[12 * i + j])}] = ", end='')
            elif j == 11:
                FILE.write(f"const uint8_t {instrument_name.upper()}_B{i+2}"+
                f"[{len(note_data_array[12 * i + j])}] = ", end='')
            FILE.write("{", end='')
            for k, l in enumerate(note_data_array[12 * i + j]):
                if k > 0:
                    FILE.write(", ", end='')
                FILE.write(str(hex(l)), end='')
            FILE.write("};")
    FILE.write("\n#endif\n")
    FILE.close()

    # Print out section declarations for linker file
    for i in range(NUM_OCTAVES):
        for j in range(NUM_NOTES):
            if j == 0:
                print(f"    .{instrument_name.lower()}_c{i+2}".ljust(22) +
                ": {}  > FRAM")
            elif j == 1:
                print(f"    .{instrument_name.lower()}_csharp{i+2}".ljust(22) +
                ": {}  > FRAM")
            elif j == 2:
                print(f"    .{instrument_name.lower()}_d{i+2}".ljust(22) +
                ": {}  > FRAM")
            elif j == 3:
                print(f"    .{instrument_name.lower()}_dsharp{i+2}".ljust(22) +
                ": {}  > FRAM")
            elif j == 4:
                print(f"    .{instrument_name.lower()}_e{i+2}".ljust(22) +
                ": {}  > FRAM")
            elif j == 5:
                print(f"    .{instrument_name.lower()}_f{i+2}".ljust(22) +
                ": {}  > FRAM")
            elif j == 6:
                print(f"    .{instrument_name.lower()}_fsharp{i+2}".ljust(22) +
                ": {}  > FRAM")
            elif j == 7:
                print(f"    .{instrument_name.lower()}_g{i+2}".ljust(22) +
                ": {}  > FRAM")
            elif j == 8:
                print(f"    .{instrument_name.lower()}_gsharp{i+2}".ljust(22) +
                ": {}  > FRAM")
            elif j == 9:
                print(f"    .{instrument_name.lower()}_a{i+2}".ljust(22) +
                ": {}  > FRAM")
            elif j == 10:
                print(f"    .{instrument_name.lower()}_asharp{i+2}".ljust(22) +
                ": {}  > FRAM")
            elif j == 11:
                print(f"    .{instrument_name.lower()}_b{i+2}".ljust(22) +
                ": {}  > FRAM")
    print(end='\n')

    # Print out array of pointers to byte arrays which store note signal data
    print(f"const uint8_t* {instrument_name.upper()}_NOTES[{NUM_OCTAVES*NUM_NOTES}" +
    "] = {", end='')
    for i in range(NUM_OCTAVES):
        for j in range(NUM_NOTES):
            if i > 0 or j > 0: print(", ", end='')
            if j == 0:
                print(f"{instrument_name.upper()}_C{i+2}", end='')
            elif j == 1:
                print(f"{instrument_name.upper()}_CSHARP{i+2}", end='')
            elif j == 2:
                print(f"{instrument_name.upper()}_D{i+2}", end='')
            elif j == 3:
                print(f"{instrument_name.upper()}_DSHARP{i+2}", end='')
            elif j == 4:
                print(f"{instrument_name.upper()}_E{i+2}", end='')
            elif j == 5:
                print(f"{instrument_name.upper()}_F{i+2}", end='')
            elif j == 6:
                print(f"{instrument_name.upper()}_FSHARP{i+2}", end='')
            elif j == 7:
                print(f"{instrument_name.upper()}_G{i+2}", end='')
            elif j == 8:
                print(f"{instrument_name.upper()}_GSHARP{i+2}", end='')
            elif j == 9:
                print(f"{instrument_name.upper()}_A{i+2}", end='')
            elif j == 10:
                print(f"{instrument_name.upper()}_ASHARP{i+2}", end='')
            elif j == 11:
                print(f"{instrument_name.upper()}_B{i+2}", end='')
    print("};\n")

    # Print out array of sizes cooresponding to byte arrays which store notes
    print(f"const uint8_t* {instrument_name.upper()}_SIZES[{NUM_OCTAVES*NUM_NOTES}" +
    "] = {", end='')
    for i in range(NUM_OCTAVES):
        for j in range(NUM_NOTES):
            if i > 0 or j > 0: print(", ", end='')
            if j == 0:
                print(f"{instrument_name.upper()}_C{i+2}_SIZE", end='')
            elif j == 1:
                print(f"{instrument_name.upper()}_CSHARP{i+2}_SIZE", end='')
            elif j == 2:
                print(f"{instrument_name.upper()}_D{i+2}_SIZE", end='')
            elif j == 3:
                print(f"{instrument_name.upper()}_DSHARP{i+2}_SIZE", end='')
            elif j == 4:
                print(f"{instrument_name.upper()}_E{i+2}_SIZE", end='')
            elif j == 5:
                print(f"{instrument_name.upper()}_F{i+2}_SIZE", end='')
            elif j == 6:
                print(f"{instrument_name.upper()}_FSHARP{i+2}_SIZE", end='')
            elif j == 7:
                print(f"{instrument_name.upper()}_G{i+2}_SIZE", end='')
            elif j == 8:
                print(f"{instrument_name.upper()}_GSHARP{i+2}_SIZE", end='')
            elif j == 9:
                print(f"{instrument_name.upper()}_A{i+2}_SIZE", end='')
            elif j == 10:
                print(f"{instrument_name.upper()}_ASHARP{i+2}_SIZE", end='')
            elif j == 11:
                print(f"{instrument_name.upper()}_B{i+2}_SIZE", end='')
    print("};")

if __name__ == "__main__":
    chdir("C://Users//jackw//vs_workspace//Python//WAV Reader")
    generate_notes("flute.wav", "flute")
import pyaudio
import numpy as np
import curses
import time
import wave

# Ajusta el tamaño de la ventana de la consola
stdscr = curses.initscr()
cursed_window_height, cursed_window_width = stdscr.getmaxyx()
cursed_window_height -= 1
cursed_window_width -= 1
cursed_window_height //= 2

# Inicializa PyAudio
p = pyaudio.PyAudio()

# Abre el archivo de audio
wave_file = wave.open("nombre_del_archivo.wav", "rb")

# Obtiene las características del archivo de audio
num_channels = wave_file.getnchannels()
sample_width = wave_file.getsampwidth()
sample_rate = wave_file.getframerate()
num_frames = wave_file.getnframes()

# Abre el flujo de audio
stream = p.open(format=p.get_format_from_width(sample_width),
                channels=num_channels,
                rate=sample_rate,
                output=True,
                frames_per_buffer=1024)

# Dibuja el gráfico en la consola
while wave_file.tell() < num_frames:
    # Lee los datos del audio
    data = wave_file.readframes(1024)
    # Reproduce el audio
    stream.write(data)
    # Calcula la intensidad de los datos
    peak = np.average(np.abs(np.fromstring(data, dtype=np.int16))) * 2
    bars = int(50 * peak / 2**16)
    # Borra la consola
    stdscr.clear()
    # Dibuja el gráfico
    for i in range(bars):
        stdscr.addstr(cursed_window_height - i, i, "|")
    # Actualiza la pantalla
    stdscr.refresh()


import ssl
from pytube import YouTube
import matplotlib.pyplot as plt
import numpy as np
import wave
import scipy.io.wavfile as wav
from scipy.signal import spectrogram
import scipy.fftpack as fft
import os
import subprocess

# Paso 1: Descargar el video de YouTube
def download_youtube_video(url, output_path='video.mp4'):
    ssl._create_default_https_context = ssl._create_unverified_context
    
    yt = YouTube(url)
    stream = yt.streams.filter(only_audio=True).first()
    stream.download(filename=output_path)
    print(f"Video descargado correctamente: {output_path}")

# Paso 2: Extraer el audio del video usando ffmpeg
def extract_audio_from_video(video_path, audio_path):
    if not os.path.exists(video_path):
        print(f"El archivo de video {video_path} no existe.")
        return
    try:
        command = f"ffmpeg -i {video_path} -q:a 0 -map a {audio_path}"
        subprocess.run(command, shell=True, check=True)
        print(f"Audio extraído correctamente: {audio_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error al extraer el audio: {e}")

# Paso 3: Crear la forma de onda del audio
def create_audio_waveform(audio_path, output_path):
    samplerate, data = wav.read(audio_path)
    plt.figure(figsize=(12, 6))
    plt.plot(data)
    plt.title('Forma de Onda del Audio')
    plt.xlabel('Muestras')
    plt.ylabel('Amplitud')
    plt.savefig(output_path)
    plt.close()
    print(f"Forma de onda guardada en: {output_path}")

# Paso 4: Crear el espectrograma del audio
def create_audio_spectrogram(audio_path, output_path):
    samplerate, data = wav.read(audio_path)
    f, t, Sxx = spectrogram(data, samplerate)
    plt.figure(figsize=(12, 6))
    plt.pcolormesh(t, f, 10 * np.log10(Sxx), shading='gouraud')
    plt.title('Espectrograma del Audio')
    plt.ylabel('Frecuencia [Hz]')
    plt.xlabel('Tiempo [s]')
    plt.colorbar(label='Intensidad [dB]')
    plt.savefig(output_path)
    plt.close()
    print(f"Espectrograma guardado en: {output_path}")

# Paso 5: Crear el espectro de frecuencia del audio
def create_audio_frequency_spectrum(audio_path, output_path):
    samplerate, data = wav.read(audio_path)
    N = len(data)
    T = 1.0 / samplerate
    yf = fft.fft(data)
    xf = np.fft.fftfreq(N, T)[:N // 2]
    plt.figure(figsize=(12, 6))
    plt.plot(xf, 2.0 / N * np.abs(yf[:N // 2]))
    plt.title('Espectro de Frecuencia del Audio')
    plt.xlabel('Frecuencia [Hz]')
    plt.ylabel('Amplitud')
    plt.savefig(output_path)
    plt.close()
    print(f"Espectro de frecuencia guardado en: {output_path}")

# Paso 6: Crear un video con las visualizaciones del audio
def create_video_with_visualizations(audio_path, waveform_path, spectrogram_path, spectrum_path, output_path):
    audio = AudioFileClip(audio_path)
    waveform_clip = ImageClip(waveform_path).set

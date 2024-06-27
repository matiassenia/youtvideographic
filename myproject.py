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
from moviepy.editor import AudioFileClip, ImageClip, concatenate_videoclips

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
    if Sxx.ndim == 1: 
        Sxx = np.expand_dims(Sxx, axis=1)
    
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
    waveform_clip = ImageClip(waveform_path).set_duration(audio.duration)
    spectrogram_clip = ImageClip(spectrogram_path).set_duration(audio.duration)
    spectrum_clip = ImageClip(spectrum_path).set_duration(audio.duration)

    # Ajusta el tamaño y la posición de los clips si es necesario
    waveform_clip = waveform_clip.resize(height=480).set_position(('center', 'top'))
    spectrogram_clip = spectrogram_clip.resize(height=480).set_position(('center', 'center'))
    spectrum_clip = spectrum_clip.resize(height=480).set_position(('center', 'bottom'))

    # Combina los clips en un solo video
    final_clip = concatenate_videoclips([waveform_clip, spectrogram_clip, spectrum_clip])

    # Guarda el video resultante
    final_clip.write_videofile(output_path, fps=24)

    print(f"Video con visualizaciones guardado en: {output_path}")

# Función principal para ejecutar los pasos
if __name__ == "__main__":
    # URL del video de YouTube
    youtube_url = 'https://www.youtube.com/watch?v=8-to2VbCyxc&ab_channel=matiasezequiel'

    # Nombres de archivos de salida
    video_output = 'video.mp4'
    audio_output = 'audio.wav'
    waveform_output = 'forma_de_onda.png'
    spectrogram_output = 'espectrograma.png'
    spectrum_output = 'espectro_de_frecuencia.png'
    video_visualizations_output = 'video_visualizaciones.mp4'

    # Paso 1: Descargar el video de YouTube
    download_youtube_video(youtube_url, video_output)

    # Paso 2: Extraer el audio del video
    extract_audio_from_video(video_output, audio_output)

    # Paso 3: Crear la forma de onda del audio
    create_audio_waveform(audio_output, waveform_output)

    # Paso 4: Crear el espectrograma del audio
    create_audio_spectrogram(audio_output, spectrogram_output)

    # Paso 5: Crear el espectro de frecuencia del audio
    create_audio_frequency_spectrum(audio_output, spectrum_output)

    # Paso 6: Crear un video con las visualizaciones del audio
    create_video_with_visualizations(audio_output, waveform_output, spectrogram_output, spectrum_output, video_visualizations_output)

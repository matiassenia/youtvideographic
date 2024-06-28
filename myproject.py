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
from pydub import AudioSegment
from moviepy.editor import AudioFileClip, ImageClip, concatenate_videoclips

# Paso 1: Descargar el video de YouTube
def download_youtube_video(url, output_path='video.mp4'):
    ssl._create_default_https_context = ssl._create_unverified_context
    
    try:
        yt = YouTube(url)
        stream = yt.streams.filter(only_audio=True).first()
        if not stream:
            print(f"No se encontró ningún stream de audio para {url}")
            return False
        stream.download(filename=output_path)
        print(f"Video descargado correctamente: {output_path}")
        return True
    except Exception as e:
        print(f"Error al descargar el video: {e}")
        return False

# Paso 2: Extraer el audio del video usando ffmpeg
def extract_audio_from_video(video_path, audio_path):
    if not os.path.exists(video_path):
        print(f"El archivo de video {video_path} no existe.")
        return False
    try:
        command = f"ffmpeg -i {video_path} -q:a 0 -map a {audio_path}"
        subprocess.run(command, shell=True, check=True)
        print(f"Audio extraído correctamente: {audio_path}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error al extraer el audio: {e}")
        return False

# Paso 3: Crear la forma de onda del audio
def create_audio_waveform(audio_path, output_path):
    if not os.path.exists(audio_path):
        print(f"El archivo de audio {audio_path} no existe.")
        return False
    try:
        samplerate, data = wav.read(audio_path)
        plt.figure(figsize=(12, 6))
        plt.plot(data)
        plt.title('Forma de Onda del Audio')
        plt.xlabel('Muestras')
        plt.ylabel('Amplitud')
        plt.savefig(output_path)
        plt.close()
        print(f"Forma de onda guardada en: {output_path}")
        return True
    except Exception as e:
        print(f"Error al crear la forma de onda: {e}")
        return False

# Paso 4: Crear la visualización de rapé de colores
def create_color_rave_visualization(audio_path, output_path):
    if not os.path.exists(audio_path):
        print(f"El archivo de audio {audio_path} no existe.")
        return False
    try:
        samplerate, data = wav.read(audio_path)
        
        data = data[:, 0] if data.ndim == 2 else data

        print(f"Dimensiones de data: {data.shape}")
        
        # Normalización de la amplitud
        normalized_amplitude = data / np.max(np.abs(data))
        print(f"Dimensiones de normalized_amplitude: {normalized_amplitude.shape}")
        
        # Generar el tiempo
        time = np.linspace(0, len(data) / samplerate, num=len(data))
        
        plt.figure(figsize=(12, 6))
        plt.scatter(time, normalized_amplitude, c=normalized_amplitude, cmap='viridis', s=2)
        plt.title('Rapé de Colores del Audio')
        plt.xlabel('Tiempo [s]')
        plt.ylabel('Amplitud Normalizada')
        plt.colorbar(label='Amplitud')
        plt.savefig(output_path)
        plt.close()
        print(f"Rapé de colores guardado en: {output_path}")
        return True
    except Exception as e:
        print(f"Error al crear la visualización de rapé de colores: {e}")
        return False

# Paso 5: Crear el espectro de frecuencia del audio
def create_audio_frequency_spectrum(audio_path, output_path):
    if not os.path.exists(audio_path):
        print(f"El archivo de audio {audio_path} no existe.")
        return False
    try:
        samplerate, data = wav.read(audio_path)
        data = data[:, 0] if data.ndim == 2 else data  # Asegurarse de que los datos sean unidimensionales
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
        return True
    except Exception as e:
        print(f"Error al crear el espectro de frecuencia: {e}")
        return False

# Paso 6: Crear un video con las visualizaciones del audio
def create_video_with_visualizations_and_audio(audio_path, waveform_path, color_rave_path, spectrum_path, video_output_path):
    try:
        # Cargar los clips de audio y visualizaciones
        audio = AudioFileClip(audio_path)
        audio_duration = audio.duration 
        
        waveform_clip = ImageClip(waveform_path).set_duration(audio_duration)
        color_rave_clip = ImageClip(color_rave_path).set_duration(audio_duration)
        spectrum_clip = ImageClip(spectrum_path).set_duration(audio_duration)

        waveform_clip = waveform_clip.resize(height=480).set_position(('center', 'top'))
        color_rave_clip = color_rave_clip.resize(height=480).set_position(('center', 'center'))
        spectrum_clip = spectrum_clip.resize(height=480).set_position(('center', 'bottom'))
        
        # Combina los clips en un solo video
        final_clip = concatenate_videoclips([waveform_clip, color_rave_clip, spectrum_clip])
        # Asignar audio al video generado
        final_clip = final_clip.set_audio(audio)
        
        # Guarda el video final
        final_clip.write_videofile(video_output_path, fps=24, codec='libx264', audio_codec='aac')

        print(f"Video con visualizaciones y audio guardado en: {video_output_path}")
        return True
    except Exception as e:
        print(f"Error al crear el video con visualizaciones y audio: {e}")
        return False 

# Función principal para ejecutar los pasos
if __name__ == "__main__":
    youtube_url = 'https://www.youtube.com/watch?v=8-to2VbCyxc&ab_channel=matiasezequiel'
    video_output = 'video.mp4'
    audio_output = 'audio.wav'
    waveform_output = 'forma_de_onda.png'
    color_rave_output = 'rape_colores.png'
    spectrum_output = 'espectro_de_frecuencia.png'
    video_visualizations_output = 'video_visualizaciones.mp4'

    if download_youtube_video(youtube_url, video_output):
        if extract_audio_from_video(video_output, audio_output):
            if create_audio_waveform(audio_output, waveform_output):
                if create_color_rave_visualization(audio_output, color_rave_output):
                    if create_audio_frequency_spectrum(audio_output, spectrum_output):
                        create_video_with_visualizations_and_audio(audio_output, waveform_output, color_rave_output, spectrum_output, video_visualizations_output)
                    else:
                        print("No se pudo crear el espectro de frecuencia.")
                else:
                    print("No se pudo crear la visualización de rapé de colores.")
            else:
                print("No se pudo crear la forma de onda.")

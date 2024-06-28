# youtvideographic

## Proyecto de Procesamiento de Audio de Videos de YouTube

Este proyecto es un invento propio con el interés de probar librerías y posibilidades de manipulación de audio, gráficos y video con Python. Me divertí mucho haciéndolo y fue realmente satisfactorio. Lo probé con una canción y video grabada por mí que había hecho y subido a YouTube hace unos años.

Al final, es un pequeño proyecto que permite descargar un video de YouTube, extraer el audio del video y crear varias visualizaciones del audio. Las visualizaciones incluyen una forma de onda, un rapé de colores y un espectro de frecuencia. Finalmente, combina estas visualizaciones con el audio para crear un video.

## Requisitos

- Python 3.6+
- ffmpeg
- pip (para instalar dependencias)

## Instalación

1. Clona este repositorio:
    ```sh
    git clone https://github.com/matiassenia/youtvideographic.git
    cd youtvideographic
    ```

2. Crea y activa un entorno virtual:
    ```sh
    python3 -m venv youtubedl_env
    source youtubedl_env/bin/activate  # En Windows usa `youtubedl_env\Scripts\activate`
    ```

3. Instala las dependencias:
    ```sh
    pip install -r requirements.txt
    ```

4. Asegúrate de tener ffmpeg instalado en tu sistema. Puedes descargarlo desde [aquí](https://ffmpeg.org/download.html).

## Uso

1. Ejecuta el script principal con la URL de YouTube del video que deseas procesar:
    ```sh
    python main.py
    ```

2. El script descargará el video, extraerá el audio y generará las visualizaciones. Finalmente, creará un video combinando las visualizaciones y el audio.

## Funciones

### Descargar Video de YouTube
Descarga el video de YouTube en formato de solo audio.
```python
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


## Ejemplo

URL de YouTube usada para el ejemplo: `https://www.youtube.com/watch?v=8-to2VbCyxc&ab_channel=matiasezequiel`

Archivos generados:
- `video.mp4`: Video descargado.
- `audio.wav`: Audio extraído.
- `forma_de_onda.png`: Imagen de la forma de onda.
- `rape_colores.png`: Imagen de la visualización de rapé de colores.
- `espectro_de_frecuencia.png`: Imagen del espectro de frecuencia.
- `video_visualizaciones.mp4`: Video final con las visualizaciones y el audio.

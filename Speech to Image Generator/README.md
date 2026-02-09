# Speech to Image Generator

A Python script that takes an audio file as input, transcribes the speech to text using Whisper (via MonsterAPI), and generates an image from the transcribed text using Stable Diffusion XL (SDXL) (also via MonsterAPI).

## Features
- **Speech-to-Text**: High-accuracy transcription using Whisper model.
- **Text-to-Image**: Generates high-quality images from text descriptions using SDXL.
- **Automated Workflow**: Processes audio to image in one go.

## Prerequisites
- Python 3.x
- MonsterAPI Key

## Installation
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Create a `.env` file and add your API key:
   ```
   MONSTER_API_KEY=your_api_key_here
   ```

## Usage
Run the script with an audio file path:
```bash
python app.py /path/to/audio/file.wav
```
Or run interactively and enter the path when prompted:
```bash
python app.py
```
Wait for the process to complete and view the generated image URL in the console.

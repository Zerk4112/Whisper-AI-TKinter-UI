# WhisperAI UI

WhisperAI UI is a graphical user interface for the WhisperAI speech recognition system. It allows users to select an audio file and a speech recognition model, and then transcribe the audio file using the selected model.

## Requirements

WhisperAI UI requires Python 3 and the following external Python packages:

- whisper

## Usage

To use WhisperAI UI, run the `whisperai_ui.py` script:

``` cmd
python whisperai_ui.py
```

The UI will open in a new window. The UI consists of the following components:

- A file selection widget, which allows the user to select an audio file to transcribe.
- A model selection widget, which allows the user to select a speech recognition model to use for transcription.
  - By default this is set to "Tiny", you may choose a different model based on how much available video memory you have.
- A button to start the transcription process.

To transcribe an audio file, follow these steps:

1. Select a speech recognition model from the dropdown list.
2. Click the "Select File" button to open a file dialog.
3. Select an audio file to transcribe.
4. Click the "Transcribe" button to start the transcription process.

The transcription results will be displayed in the console during the transcription progress.

Once transcription is complete, the results will be saved to a .txt file within the execution directory. The file will be named based on the selected audio file.

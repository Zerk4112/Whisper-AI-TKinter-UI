import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import whisper
import os
import threading

models = {
    "Tiny - ~1GB": "tiny",
    "Base - ~1GB": "base",
    "Small - ~2GB": "small",
    "Medium - ~5GB": "medium",
    "Large - ~10GB": "large",
}

class WhisperAIUI:
    def __init__(self, master):
        self.master = master
        self.default_resolution="300x100"
        master.title("WhisperAI Transcriber")
        master.geometry(self.default_resolution)
        master.resizable(False, False)
        self.file_frame = tk.Frame(master)

        self.file_path = None
        self.model = None
        self.selected_model = None
        self.model_label = tk.Label(self.file_frame, text="Select Model:")
        self.model_combo = ttk.Combobox(self.file_frame, values=list(models.keys()))
        self.model_combo.bind("<<ComboboxSelected>>", self.select_model)
        self.model_combo.current(0)
        self.select_model(1)
        self.model_label.grid(row=0, column=0, padx=1, pady=1)
        self.model_combo.grid(row=0, column=1, padx=1, pady=1)
        # self.file_frame.grid(row=0, column=1, padx=1, pady=1)
        self.file_frame.pack()
        # self.model_combo.pack()

        self.file_label = tk.Label(master, text="No file selected")
        # self.file_label.grid(row=1, column=1, padx=10, pady=10)
        self.file_label.pack()

        self.select_button = tk.Button(master, text="Select File", command=self.select_file)
        # self.select_button.grid(row=2, column=1, padx=10, pady=10)
        self.select_button.pack()

        self.transcribe_button = tk.Button(master, text="Transcribe", command=self.transcribe_file)
        # self.transcribe_button.grid(row=3, column=1, padx=10, pady=10)
        self.transcribe_button.pack()

        self.monitor_string=""
    def select_file(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3 *.mp4 *.mpeg *.mpga *.m4a *.wav *.webm")])
        self.file_name=self.file_path.split("/")[-1].split(".")[0]+".txt"
        if self.file_path:
            self.file_label.config(text=self.file_path)
        else:
            self.file_label.config(text="No file selected")
        current_width=self.master.winfo_width()
        new_width=len(self.file_path)*6+2
        if new_width>current_width and new_width > 300:
            self.master.geometry("{}x100".format(new_width))
        elif new_width<300:
            self.master.geometry(self.default_resolution)
        

    def select_model(self, model):
        self.model = models[self.model_combo.get()]
        self.selected_model = whisper.load_model(self.model)

    def transcribe(self):
        self.result = whisper.transcribe(self.selected_model, self.file_path, verbose=True)
        with open(self.file_name, "w") as f:
            for segment in self.result["segments"]:
                f.write(segment["text"]+"\n")
        self.transcribe_button.config(state="normal")
        self.select_button.config(state="normal")
        tk.messagebox.showinfo("Transcription Complete", "Transcription complete.\nFile saved as " + self.file_name + ".")
        self.file_label.config(text=self.file_path)

    def transcribe_file(self):
        if self.file_path:
            try:
                if os.path.exists(self.file_name):
                    confirm = tk.messagebox.askyesno("File Exists", "The file " + self.file_name + " already exists. Do you want to overwrite it?")
                    if not confirm:
                        return
                
                self.transcribe_button.config(state="disabled")
                self.select_button.config(state="disabled")
                self.file_label.config(text="Transcribing...")
                tk.messagebox.showinfo("Transcription Started", "Transcription started.\nYou will be notified when it is complete.")
                self.transcribe_thread = threading.Thread(target=self.transcribe)
                self.transcribe_thread.start()

            except Exception as e:
                tk.messagebox.showerror("Error", "An error occurred during transcription.\n" + str(e))
        else:
            tk.messagebox.showerror("Error", "No file selected")

root = tk.Tk()
app = WhisperAIUI(root)

root.mainloop()

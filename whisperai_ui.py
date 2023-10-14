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
        master.title("WhisperAI Transcriber")
        master.geometry("400x120")
        self.file_path = None
        self.model = None
        self.selected_model = None
        self.model_combo = ttk.Combobox(master, values=list(models.keys()))
        self.model_combo.bind("<<ComboboxSelected>>", self.select_model)
        self.model_combo.current(0)

        self.model_combo.pack()

        self.file_label = tk.Label(master, text="No file selected")
        self.file_label.pack()

        self.select_button = tk.Button(master, text="Select File", command=self.select_file)
        self.select_button.pack()

        self.transcribe_button = tk.Button(master, text="Transcribe", command=self.transcribe_file)
        self.transcribe_button.pack()

        self.monitor_string=""
    def select_file(self):
        self.file_path = filedialog.askopenfilename()
        self.file_name=self.file_path.split("/")[-1].split(".")[0]+".txt"
        self.file_label.config(text=self.file_path)

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
app.select_model(1)
root.mainloop()

from transcription_tool import YouTubeTranscriptTool
from video_summarizer import VideoSummarizer

import customtkinter as ctk
from customtkinter import *
from tkinter.filedialog import askopenfilename
import threading

class App:
    def __init__(self, root):
        self.transcript_tool = YouTubeTranscriptTool()
        self.vid_summarizer = VideoSummarizer()
        self.root = root
        self.root.title("Video Summarizer")
        self.root.geometry("800x800")
        self.root.resizable(False, False)
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        self.create_widgets()

    def create_widgets(self):
        self.title_label = ctk.CTkLabel(self.root,
                                        text="YouTube Summary Generator",
                                        font=("Times New Roman", 30, "bold"),
                                        text_color="red")
        self.title_label.pack(pady=10)

        self.link_entry = ctk.CTkEntry(self.root,
                                       placeholder_text="Enter link here...",
                                       font=("Arial", 20),
                                       width=400)
        self.link_entry.pack(padx=25, pady=10, fill=X)

        self.summarize_button = ctk.CTkButton(self.root,
                                              text="Summarize",
                                              command=self.summarize,
                                              font=("Arial", 20, "bold"),
                                              fg_color="#4CAF50",
                                              hover_color="#45a049",
                                              width=200)
        self.summarize_button.pack(pady=10)

        self.text_box = ctk.CTkTextbox(self.root,
                                       wrap=WORD,
                                       font=("Calibri", 20))
        self.text_box.pack(padx=15, pady=15, fill=BOTH, expand=True)
        self.text_box.configure(state='disabled')

        self.bottom_label = ctk.CTkLabel(self.root,
                                         text="Powered by Google Gemini API & Created by @the_coderunknown",
                                         font=("Arial", 12))
        self.bottom_label.pack(side=BOTTOM, pady=10)

    def summarize(self):
        link = self.link_entry.get()
        if link:
            self.summarize_button.configure(state=DISABLED)
            self.text_box.configure(state=NORMAL)
            self.text_box.delete(1.0, END)
            self.text_box.insert(END, "Summarizing....")
            self.text_box.configure(state=DISABLED)
            threading.Thread(target=self.process_and_display_summary, args=(link,)).start()
        else:
            self.text_box.configure(state=NORMAL)
            self.text_box.delete(1.0, END)
            self.text_box.insert(END, "Please enter a valid link.")
            self.text_box.configure(state='disabled')

    def process_and_display_summary(self, link):
        transcript = self.transcript_tool.fetch_transcript(link)
        self.transcript_tool.close_driver()

        summary = self.vid_summarizer.generate(transcript)

        self.text_box.configure(state=NORMAL)
        self.text_box.delete(1.0, END)
        self.text_box.insert(END, summary)
        self.text_box.configure(state=DISABLED)
        self.summarize_button.configure(state=NORMAL)


if __name__ == "__main__":
    root = ctk.CTk()
    app = App(root)
    root.mainloop()
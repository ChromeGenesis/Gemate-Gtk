from pytube import YouTube
import customtkinter as ctk
import CTkMessagebox
import pyperclip, re
import threading


class Gemate:
    def __init__(self) -> None:
        self.root = ctk.CTk()
        self.title = "Genesis YT Downloader"
        self.root.title(self.title)
        self.root.geometry("378x418+667+120")
        self.root.resizable(0, 0)
        self.font = ("Comic Sans MS bold", 14)

        self._media_format_var = ctk.StringVar(value="audio")
        self._url_var = ctk.StringVar()
        self._completed_var = ctk.StringVar(value="Completed 0%")

        ctk.CTkLabel(
            self.root, height=19, width=59, text="<Genesis>", font=self.font
        ).place(relx=0.423, rely=0.048)

        ctk.CTkLabel(
            self.root,
            height=39,
            width=225,
            text="Tool For Downloading Videos",
            text_color="#008080",
            font=(self.font[0], self.font[1] + 3),
        ).place(relx=0.185, rely=0.144)

        self.audio_rbtn = ctk.CTkRadioButton(
            self.root,
            height=21,
            variable=self._media_format_var,
            value="audio",
            text="Mp3 [Audio]",
            font=self.font,
        )
        self.audio_rbtn.place(relx=0.37, rely=0.335)
        self.video_rbtn = ctk.CTkRadioButton(
            self.root,
            height=21,
            variable=self._media_format_var,
            value="video",
            text="Mp4 [Video]",
            font=self.font,
        )
        self.video_rbtn.place(relx=0.37, rely=0.431)

        ctk.CTkLabel(
            self.root,
            height=19,
            width=88,
            text="Video URL:",
            font=self.font,
        ).place(relx=0.37, rely=0.55)

        self.url_entry = ctk.CTkEntry(
            self.root,
            justify="center",
            textvariable=self._url_var,
            height=27,
            width=250,
            font=self.font,
        )
        self.url_entry.place(relx=0.058, rely=0.622, relwidth=0.889)

        self.progress_bar = ctk.CTkProgressBar(
            self.root,
            orientation="horizontal",
            mode="determinate",
            height=22,
        )
        self.progress_bar.place(relx=0.265, rely=0.722)
        self.progress_bar.set(0)

        completed_label = ctk.CTkLabel(
            self.root,
            height=19,
            width=105,
            font=self.font,
            textvariable=self._completed_var,
        )
        completed_label.place(relx=0.378, rely=0.800)

        self.download_btn = ctk.CTkButton(
            self.root,
            height=35,
            width=96,
            text="Download",
            font=self.font,
            command=self.download_thread,
        )
        self.download_btn.place(relx=0.400, rely=0.881)

        self.root.bind("<FocusIn>", lambda e: self.paste_clipboard_content())
        self.paste_clipboard_content()
        self.root.mainloop()

    def paste_clipboard_content(self):
        content = pyperclip.paste()

        youtube_pattern = re.compile(
            r"^(?:https?://)?(?:www\.)?(?:youtu\.be/|youtube\.com/(?:embed/|v/|watch\?v=|watch\?.+&v=))([\w-]{11})"
        )
        match = youtube_pattern.match(content)
        if not content or not match:
            return

        self.url_entry.delete(0, "end")
        self._url_var.set(content)
        self.url_entry.update_idletasks()
        self.url_entry.focus_set()
        self.url_entry.select_range(0, "end")

    def download_thread(self):
        if not self._url_var.get():
            CTkMessagebox.CTkMessagebox(
                title="NO URL",
                message="Please Provide A URL",
                icon="warning",
                sound=True,
                font=self.font,
                width=250,
                justify="center",
            )
            return
        download_t = threading.Thread(target=self.download)
        download_t.start()

    def on_progress(self, stream, chunk: bytes, bytes_remaining: int):
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        val = bytes_downloaded / total_size
        self._completed_var.set(f"Completed {val * 100:.0f}%")
        self.progress_bar.set(val)

    def download(self):
        self.root.title(f"{self.title} - Downloading...")
        self.progress_bar.set(0)

        audio = self._media_format_var.get() == "audio"

        try:
            yt = YouTube(self._url_var.get(), on_progress_callback=self.on_progress)
            if audio:
                stream = yt.streams.itag_index[140]
            else:
                stream = yt.streams.filter(file_extension="mp4", res="720p").first()
            stream.download()
        except Exception as e:
            CTkMessagebox.CTkMessagebox(
                title="ERROR",
                message=str(e),
                icon="cancel",
                sound=True,
                font=self.font,
                width=250,
                justify="center",
            )
            print(e)

        self.root.title(self.title)


if __name__ == "__main__":
    Gemate()

# Importações
import tkinter as tk
from tkinter import messagebox, filedialog
from pytube import YouTube
import ttkbootstrap as ttk
from PIL import Image, ImageTk
from os import path


class Menu():
    def __init__(self):
        self.url = str
        self.yt = YouTube
        self.entry_url = tk.Entry

        self.ICON = 'imgs/YT.ico'
        self.IMAGE = Image.open('imgs/YT.png')
        self.FONTE_TEXT = 'Youtube Sans'

        self.config_janela()

    def config_janela(self):

        def check():
            if self.combobox['values'][0] != 'Webm':
                self.combobox.set('')
                self.combobox['values'] = ['Webm', 'Mp3']
            else:
                self.combobox.set('')
                self.combobox['values'] = ['144p', '240p', '360p', '480p', '720p (HD)', '1080p (FHD)', '1440p (QHD)', '2160p (4K)']

        def exec_botao_dir():
            destino = filedialog.askdirectory()
            if destino:
                self.dire.set(destino)

        def exec_botao():
            try:
                if not self.dire.get():
                    self.dire.set('.')

                url = self.entry_url.get().strip()

                formato = self.combobox.get()

                if formato[-1] == ')':
                    formato = formato[:5].strip()

                if self.so_audio.get():
                    yt = YouTube(url)
                    streams = yt.streams.filter(only_audio=True).first()

                    if formato == 'Mp3':
                        streams.download(filename=f'{yt.title} ({formato}).mp3', output_path=self.dire.get())
                    elif formato == 'Webm':
                        streams.download(filename=f'{yt.title} ({formato}).webm', output_path=self.dire.get())

                    if path.exists(f'{self.dire.get()}\\{yt.title} ({formato}).mp3') or path.exists(f'{self.dire.get()}\\{yt.title} ({formato}).webm'):
                        messagebox.showinfo('Sucesso!', f'O vídeo {yt.title} foi baixado com sucesso!')
                    else:
                        messagebox.showwarning('[AVISO]', 'Essa resolução não esta disponível para esse vídeo')
                else:
                    yt = YouTube(url)

                    videos_streams = yt.streams.filter(res=formato)

                    for stream in videos_streams:
                        try:
                            stream.download(filename=(f'{yt.title} ({formato}).mp4'), output_path=self.dire.get())
                        except Exception as err:
                            messagebox.showerror('[ERRO]', err)
                        
                    if path.exists(f'{self.dire.get()}\\{yt.title} ({formato}).mp4'):
                        messagebox.showinfo('Sucesso!', f'O vídeo {yt.title} foi baixado com sucesso!')
                    else:
                        messagebox.showwarning('[AVISO]', 'Essa resolução não esta disponível para esse vídeo') 
            except IndexError:
                messagebox.showerror('[ERRO]', 'Insira uma resolução!')
            except Exception as err:
                messagebox.showerror('[ERRO]', f'Erro ao acessar o link!')
            

        self.janela = tk.Tk()
        self.janela.title('Baixar vídeos do Youtube')
        self.janela.geometry('500x400+800+300')
        self.janela.iconbitmap(self.ICON)
        self.janela.resizable(False, False)

        self.IMAGE = ImageTk.PhotoImage(self.IMAGE.resize((180,170)))
        tk.Label(self.janela,
              image=self.IMAGE).place(x=30, y=-20)
        tk.Label(self.janela,
              text='Youtube',
              font=(self.FONTE_TEXT, 46)).place(x=205, y=25)
        tk.Label(self.janela,
              text='URL:',
              font=(self.FONTE_TEXT, 22)).place(x=27, y=135)
        
        self.entry_url = ttk.Entry(self.janela,
                                   bootstyle='dark',
                                   width=62)
        self.entry_url.place(x=90, y=143)

        estilo = ttk.Style()
        estilo.configure('dark.TButton', font=(self.FONTE_TEXT, 22), width=10)
        estilo.configure('dark.TCheckbutton', font=('Banschirift', 16))

        self.so_audio = tk.BooleanVar()

        ttk.Checkbutton(style='dark.TCheckbutton',
                        text='Apenas áudio',
                        variable=self.so_audio,
                        onvalue=True,
                        offvalue=False,
                        command=check).place(x=316,y=200)
        
        tk.Label(self.janela,
              text='Formato:',
              font=(self.FONTE_TEXT, 20)).place(x=26, y=190)

        opcoes = ['144p', '240p', '360p', '480p', '720p (HD)', '1080p (FHD)', '1440p (QHD)', '2160p (4K)']
        self.combobox = ttk.Combobox(bootstyle='dark',
                     values=opcoes)
        self.combobox.place(x=142, y=197)

        tk.Label(self.janela,
                text='Caminho:',
                font=(self.FONTE_TEXT, 20)).place(x=26, y=250)
        
        self.dire = tk.StringVar()
        ttk.Entry(bootstyle='dark',
                textvariable=self.dire,
                width=40).place(x=140, y=255)

        tk.Button(self.janela,
                text='Escolher',
                font=(self.FONTE_TEXT, 12),
                command=exec_botao_dir).place(x=410,y=255)

        ttk.Button(self.janela,
                text='BAIXAR',
                style='dark.TButton',
                command=exec_botao).place(x=150, y=320)

        self.janela.mainloop()

if __name__ == '__main__':
    Menu()
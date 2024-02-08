# Importações
import tkinter as tk
from tkinter import messagebox, filedialog
from pytube import YouTube
import ttkbootstrap as ttk
from PIL import Image, ImageTk
from os import path
import re


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
                # Definindo o diretório padrão se não especificado
                if not self.dire.get():
                    self.dire.set('.')
                    messagebox.showinfo('Aviso', 'Nenhum diretório especificado. Usando diretório atual.')

                url = self.entry_url.get().strip()
                formato = self.combobox.get()

                # Extrair o formato corretamente usando expressões regulares
                formato_match = re.match(r"(.+?)\s*\(\d+p\)", formato)
                if formato_match:
                    formato = formato_match.group(1).strip()

                yt = YouTube(url)
                file_extension = 'mp3' if formato == 'Mp3' else 'webm'
                try:
                    file_name = f"{yt.title} ({formato}).{file_extension}"
                except Exception as err:
                    messagebox.showerror('[ERRO!]', 'Caracteres inválidos no titulo'+err)
                file_path = f'{self.dire.get()}/{file_name}'
                
                if self.so_audio.get():
                    streams = yt.streams.filter(only_audio=True).first()
                    streams.download(filename=file_name, output_path=self.dire.get())
                else:
                    videos_streams = yt.streams.filter(res=formato)
                    for stream in videos_streams:
                        file_name = f"{yt.title} ({formato}).mp4"
                        stream.download(filename=file_name, output_path=f'{self.dire.get()}/')

                # Verificar se o arquivo foi baixado com sucesso
                print(f'{self.dire.get()}/{file_name}')
                if path.exists(f'{self.dire.get()}/{file_name}'):
                    messagebox.showinfo('Sucesso!', f'O vídeo {yt.title} foi baixado com sucesso em {file_path}!')
                else:
                    messagebox.showwarning('Aviso', f'Não foi possível baixar o vídeo {yt.title} na resolução {formato}.')
            
            except IndexError:
                messagebox.showerror('[ERRO]', 'Insira uma resolução!')
            except Exception as err:
                messagebox.showerror('[ERRO]', f'Erro ao acessar o link! {err}')
            

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
        self.entry_url.place(x=100, y=143)

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
                width=40).place(x=150, y=255)

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
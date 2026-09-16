import json
import sqlite3
import sys
import customtkinter as ctk

# Configuração visual
ctk.set_appearance_mode("Light")

# --- BANCO DE DADOS (SQLite) ---

def inicializar_banco():
    conn = sqlite3.connect("musicas_vibe_pastel.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS musicas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            artista TEXT NOT NULL,
            humor TEXT NOT NULL,
            duracao TEXT NOT NULL
        )
    """)
    
    # Limpa a tabela para garantir que apenas as faixas pedidas fiquem ativas
    cursor.execute("DELETE FROM musicas")
    
    # Músicas e Artistas solicitados
    playlist_custom = [
        # Triste: Adele (Álbum 21)
        ("Someone Like You", "Adele (21)", "triste", "4:45"),
        ("Rolling in the Deep", "Adele (21)", "triste", "3:48"),
        ("Turning Tables", "Adele (21)", "triste", "4:10"),
        ("Set Fire to the Rain", "Adele (21)", "triste", "4:02"),
        
        # Energético: Ariana Grande (positions)
        ("positions", "Ariana Grande", "energetico", "2:52"),
        ("34+35", "Ariana Grande", "energetico", "2:53"),
        ("motive", "Ariana Grande ft. Doja Cat", "energetico", "2:47"),
        ("pov", "Ariana Grande", "energetico", "3:21"),
        
        # Relaxado: Marisa Monte
        ("Ainda Bem", "Marisa Monte", "relaxado", "3:35"),
        ("Vilarejo", "Marisa Monte", "relaxado", "3:28"),
        ("Beija Eu", "Marisa Monte", "relaxado", "3:10"),
        ("Amor I Love You", "Marisa Monte", "relaxado", "3:12"),
        
        # Focado: Seu Jorge
        ("Burguesinha", "Seu Jorge", "focado", "3:57"),
        ("Amiga da Minha Mulher", "Seu Jorge", "focado", "4:10"),
        ("Carolina", "Seu Jorge", "focado", "5:53"),
        ("Mina do Condomínio", "Seu Jorge", "focado", "4:46")
    ]
    
    cursor.executemany("INSERT INTO musicas (titulo, artista, humor, duracao) VALUES (?, ?, ?, ?)", playlist_custom)
    conn.commit()
    conn.close()

def buscar_musicas(humor):
    conn = sqlite3.connect("musicas_vibe_pastel.db")
    cursor = conn.cursor()
    cursor.execute("SELECT titulo, artista, duracao FROM musicas WHERE humor = ?", (humor.lower(),))
    res = cursor.fetchall()
    conn.close()
    return res

def exportar_json(humor, playlist):
    dados = {
        "humor": humor,
        "playlist": [{"titulo": m[0], "artista": m[1], "duracao": m[2]} for m in playlist]
    }
    with open(f"playlist_{humor}.json", "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)

# --- INTERFACE COM CORES PASTÉIS (GUI) ---

class AppVibePastel(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("VibeStream - Cores Pastéis")
        self.geometry("850x580")
        self.minsize(800, 500)

        # Paleta de Cores Pastéis
        self.AZUL_PASTEL_FUNDO = "#E3F2FD"
        self.AZUL_PASTEL_CARD = "#BBDEFB"
        self.AMARELO_PASTEL = "#FFF59D"
        self.AMARELO_HOVER = "#FFEE58"
        self.TEXTO_ESCURO = "#2C3E50"

        self.configure(fg_color=self.AZUL_PASTEL_FUNDO)

        # Layout Principal
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # 1. Sidebar (Menu Lateral Azul Pastel)
        self.sidebar = ctk.CTkFrame(self, width=220, fg_color=self.AZUL_PASTEL_CARD, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")

        self.logo = ctk.CTkLabel(self.sidebar, text="✨ Vibe Stream", font=ctk.CTkFont(size=22, weight="bold"), text_color=self.TEXTO_ESCURO)
        self.logo.pack(pady=25, padx=20)

        self.lbl_humor = ctk.CTkLabel(self.sidebar, text="Qual é a sua vibe?", font=ctk.CTkFont(size=13, weight="bold"), text_color=self.TEXTO_ESCURO)
        self.lbl_humor.pack(pady=(10, 5))

        self.combo_humor = ctk.CTkOptionMenu(
            self.sidebar, 
            values=["Energetico", "Triste", "Relaxado", "Focado"],
            fg_color="#FFFFFF",
            button_color=self.AMARELO_PASTEL,
            button_hover_color=self.AMARELO_HOVER,
            text_color=self.TEXTO_ESCURO,
            dropdown_text_color=self.TEXTO_ESCURO
        )
        self.combo_humor.pack(pady=10, padx=15)

        # Botão Amarelo Pastel
        self.btn_gerar = ctk.CTkButton(
            self.sidebar, 
            text="⚡ Gerar Playlist", 
            command=self.gerar_playlist,
            fg_color=self.AMARELO_PASTEL,
            hover_color=self.AMARELO_HOVER,
            text_color=self.TEXTO_ESCURO,
            font=ctk.CTkFont(size=13, weight="bold")
        )
        self.btn_gerar.pack(pady=15, padx=15)

        self.btn_exportar = ctk.CTkButton(
            self.sidebar, 
            text="💾 Exportar JSON", 
            command=self.salvar_json,
            fg_color="#FFFFFF",
            hover_color=self.AZUL_PASTEL_FUNDO,
            text_color=self.TEXTO_ESCURO,
            border_width=1,
            border_color="#90CAF9"
        )
        self.btn_exportar.pack(pady=10, padx=15)

        # 2. Área de Conteúdo Estilo Web
        self.content = ctk.CTkFrame(self, fg_color="transparent")
        self.content.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

        # Banner Amarelo Pastel
        self.banner = ctk.CTkFrame(self.content, fg_color=self.AMARELO_PASTEL, height=90, corner_radius=15)
        self.banner.pack(fill="x", pady=(0, 20))

        self.banner_title = ctk.CTkLabel(self.banner, text="Sua Trilha Sonora", font=ctk.CTkFont(size=20, weight="bold"), text_color=self.TEXTO_ESCURO)
        self.banner_title.pack(anchor="w", padx=20, pady=(15, 2))

        self.banner_sub = ctk.CTkLabel(self.banner, text="Artistas selecionados para o seu momento.", font=ctk.CTkFont(size=12), text_color="#5D4037")
        self.banner_sub.pack(anchor="w", padx=20, pady=(0, 15))

        # Scroll para Cards de Música
        self.scroll_list = ctk.CTkScrollableFrame(self.content, label_text="Playlist Disponível", fg_color="#FFFFFF", label_text_color=self.TEXTO_ESCURO)
        self.scroll_list.pack(fill="both", expand=True)

        self.playlist_atual = []
        self.gerar_playlist()

    def gerar_playlist(self):
        humor = self.combo_humor.get().lower()
        self.playlist_atual = buscar_musicas(humor)

        for widget in self.scroll_list.winfo_children():
            widget.destroy()

        for musica in self.playlist_atual:
            card = ctk.CTkFrame(self.scroll_list, fg_color=self.AZUL_PASTEL_FUNDO, height=45, corner_radius=10)
            card.pack(fill="x", pady=4, padx=5)

            lbl_faixa = ctk.CTkLabel(card, text=f"🎶 {musica[0]}", font=ctk.CTkFont(size=13, weight="bold"), text_color=self.TEXTO_ESCURO)
            lbl_faixa.pack(side="left", padx=15)

            lbl_duracao = ctk.CTkLabel(card, text=musica[2], font=ctk.CTkFont(size=11), text_color="#78909C")
            lbl_duracao.pack(side="right", padx=15)

            lbl_artista = ctk.CTkLabel(card, text=f"por {musica[1]}", font=ctk.CTkFont(size=12), text_color="#546E7A")
            lbl_artista.pack(side="right", padx=15)

    def salvar_json(self):
        humor = self.combo_humor.get().lower()
        if self.playlist_atual:
            exportar_json(humor, self.playlist_atual)

# --- MODO CLI ---

def rodar_cli():
    print("\n--- 🎵 VIBESTREAM CLI (PASTEL EDITION) ---")
    humor = input("Escolha o humor (energetico, triste, relaxado, focado): ").strip().lower()
    musicas = buscar_musicas(humor)
    print(f"\nPlaylist [{humor.upper()}]:")
    for idx, m in enumerate(musicas, 1):
        print(f"{idx}. {m[0]} - {m[1]} ({m[2]})")

if __name__ == "__main__":
    inicializar_banco()
    if len(sys.argv) > 1 and sys.argv[1] == "--cli":
        rodar_cli()
    else:
        app = AppVibePastel()
        app.mainloop()
import json
import random
import sqlite3
import sys
import time
import threading
import tkinter as tk
from tkinter import messagebox, ttk
from faker import Faker

# --- BANCO DE DADOS (SQLite + Hits Pop Reais + Faker) ---

def inicializar_banco():
    conn = sqlite3.connect("musicas_pop.db")
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
    
    cursor.execute("SELECT COUNT(*) FROM musicas")
    if cursor.fetchone()[0] == 0:
        # Base inicial com Hits Pop Populares / Pop em Alta
        hits_pop = [
            # Feliz
            ("Espresso", "Sabrina Carpenter", "feliz", "2:55"),
            ("Cruel Summer", "Taylor Swift", "feliz", "2:58"),
            ("Dance The Night", "Dua Lipa", "feliz", "2:56"),
            ("Greedy", "Tate McRae", "feliz", "2:11"),
            ("PLEASE PLEASE PLEASE", "Sabrina Carpenter", "feliz", "3:06"),
            # Triste
            ("BIRDS OF A FEATHER", "Billie Eilish", "triste", "3:30"),
            ("drivers license", "Olivia Rodrigo", "triste", "4:02"),
            ("Glimpse of Us", "Joji", "triste", "3:53"),
            ("vampire", "Olivia Rodrigo", "triste", "3:39"),
            ("Pilantra", "Jão, Anitta", "triste", "3:10"),
            # Animado / Festa
            ("Houdini", "Dua Lipa", "animado", "3:05"),
            ("Super Shy", "NewJeans", "animado", "2:34"),
            ("Alibi", "Sevdaliza, Pabllo Vittar, Yseult", "animado", "2:41"),
            ("Von dutch", "Charli xcx", "animado", "2:44"),
            ("FUNK RAVE", "Anitta", "animado", "2:27"),
            # Relaxado
            ("WILDFLOWER", "Billie Eilish", "relaxado", "4:21"),
            ("Golden Hour", "JVKE", "relaxado", "3:29"),
            ("Saturn", "SZA", "relaxado", "3:06"),
            ("Snooze", "SZA", "relaxado", "3:21"),
            ("Idiota", "Jão", "relaxado", "3:04"),
            # Focado
            ("Blinding Lights", "The Weeknd", "focado", "3:20"),
            ("As It Was", "Harry Styles", "focado", "2:47"),
            ("Starboy", "The Weeknd", "focado", "3:50"),
            ("Midnight Rain", "Taylor Swift", "focado", "2:54"),
            ("Flowers", "Miley Cyrus", "focado", "3:20")
        ]
        
        cursor.executemany("INSERT INTO musicas (titulo, artista, humor, duracao) VALUES (?, ?, ?, ?)", hits_pop)
        
        # Complementa com Faker para simular novas faixas populares
        fake = Faker('pt_BR')
        humores = ["feliz", "triste", "animado", "relaxado", "focado"]
        for _ in range(15):
            titulo = f"{fake.word().capitalize()} {fake.word()}"
            artista = fake.name()
            humor = random.choice(humores)
            duracao = f"{random.randint(2, 4)}:{random.randint(10, 59):02d}"
            cursor.execute("INSERT INTO musicas (titulo, artista, humor, duracao) VALUES (?, ?, ?, ?)", (titulo, artista, humor, duracao))
            
        conn.commit()
    conn.close()

def buscar_playlist_por_humor(humor):
    conn = sqlite3.connect("musicas_pop.db")
    cursor = conn.cursor()
    cursor.execute("SELECT titulo, artista, duracao FROM musicas WHERE humor = ? ORDER BY RANDOM() LIMIT 6", (humor.lower(),))
    resultados = cursor.fetchall()
    conn.close()
    return resultados

def exportar_para_json(humor, playlist):
    dados = {
        "humor": humor,
        "gerado_em": time.strftime("%Y-%m-%d %H:%M:%S"),
        "playlist": [{"titulo": m[0], "artista": m[1], "duracao": m[2]} for m in playlist]
    }
    nome_arquivo = f"playlist_pop_{humor}.json"
    with open(nome_arquivo, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)
    return nome_arquivo

# --- INTERFACE GRÁFICA ESTILO WEB APP / CORREIOS-SPOTIFY (GUI) ---

class WebAppMusicaGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("VibeStream - Pop Music Assistant")
        self.root.geometry("850x600")
        self.root.configure(bg="#F4F6F9")
        
        # Estilos de Cores (Azul Correios + Amarelo Destaque + Layout Spotify)
        self.COLOR_NAV = "#004182"       # Azul Escuro
        self.COLOR_BANNER = "#0072C6"    # Azul Médio
        self.COLOR_ACCENT = "#FFCC00"    # Amarelo
        self.COLOR_TEXT_LIGHT = "#FFFFFF"
        self.COLOR_BG_CARD = "#FFFFFF"
        
        self.tocando = False
        self.progresso_val = 0
        self.musica_atual = None

        self.criar_layout()

    def criar_layout(self):
        # 1. Barra de Navegação Superior (Header Web)
        nav_bar = tk.Frame(self.root, bg=self.COLOR_NAV, height=50)
        nav_bar.pack(fill=tk.X, side=tk.TOP)
        
        lbl_logo = tk.Label(nav_bar, text="🎵 VibeStream", font=("Segoe UI", 14, "bold"), bg=self.COLOR_NAV, fg=self.COLOR_TEXT_LIGHT)
        lbl_logo.pack(side=tk.LEFT, padx=20, pady=10)

        lbl_sub = tk.Label(nav_bar, text="O mês do Pop com as melhores vibes!", font=("Segoe UI", 9, "italic"), bg=self.COLOR_NAV, fg=self.COLOR_ACCENT)
        lbl_sub.pack(side=tk.LEFT, padx=10)

        # 2. Banner Promocional estilo App Web
        banner = tk.Frame(self.root, bg=self.COLOR_BANNER, height=80)
        banner.pack(fill=tk.X, side=tk.TOP)
        
        lbl_banner_title = tk.Label(banner, text="SINTA O RITMO DO SEU DIA!", font=("Segoe UI", 16, "bold"), bg=self.COLOR_BANNER, fg=self.COLOR_TEXT_LIGHT)
        lbl_banner_title.pack(anchor="w", padx=25, pt=10)
        
        lbl_banner_desc = tk.Label(banner, text="Escolha seu humor e gere uma playlist pop exclusiva instantaneamente.", font=("Segoe UI", 10), bg=self.COLOR_BANNER, fg=self.COLOR_TEXT_LIGHT)
        lbl_banner_desc.pack(anchor="w", padx=25, pb=10)

        # 3. Conteúdo Principal (Sidebar + Playlist Area)
        main_container = tk.Frame(self.root, bg="#F4F6F9")
        main_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        # Sidebar (Seleção de Humor)
        sidebar = tk.Frame(main_container, bg=self.COLOR_BG_CARD, width=220, relief=tk.RAISED, bd=1)
        sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))

        lbl_sidebar = tk.Label(sidebar, text="Qual é a sua vibe?", font=("Segoe UI", 11, "bold"), bg=self.COLOR_BG_CARD, fg="#333333")
        lbl_sidebar.pack(pady=15, padx=10, anchor="w")

        self.humor_var = tk.StringVar(value="feliz")
        humores = [("😊 Feliz / High", "feliz"), ("😢 Bad / Triste", "triste"), ("🔥 Animação / Festa", "animado"), ("☕ Relax / Chill", "relaxado"), ("🎧 Foco / Work", "focado")]

        for texto, valor in humores:
            rb = tk.Radiobutton(
                sidebar, text=texto, value=valor, variable=self.humor_var,
                font=("Segoe UI", 10), bg=self.COLOR_BG_CARD, activebackground=self.COLOR_BG_CARD,
                selectcolor=self.COLOR_ACCENT, anchor="w", indicatoron=0, bd=0, padx=10, pady=8
            )
            rb.pack(fill=tk.X, padx=10, pady=3)

        btn_gerar = tk.Button(
            sidebar, text="⚡ GERAR PLAYLIST", command=self.gerar_playlist,
            bg=self.COLOR_ACCENT, fg="#000", font=("Segoe UI", 10, "bold"), bd=0, cursor="hand2", pady=8
        )
        btn_gerar.pack(fill=tk.X, padx=10, pady=20)

        # Área da Playlist (Tabela Estilo Web App)
        playlist_area = tk.Frame(main_container, bg=self.COLOR_BG_CARD, relief=tk.RAISED, bd=1)
        playlist_area.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        header_pl = tk.Frame(playlist_area, bg=self.COLOR_BG_CARD)
        header_pl.pack(fill=tk.X, padx=15, pady=10)

        lbl_pl_title = tk.Label(header_pl, text="🎶 Músicas Recomendadas", font=("Segoe UI", 12, "bold"), bg=self.COLOR_BG_CARD, fg="#333")
        lbl_pl_title.pack(side=tk.LEFT)

        btn_export = tk.Button(
            header_pl, text="💾 Exportar JSON", command=self.salvar_json,
            bg=self.COLOR_NAV, fg="white", font=("Segoe UI", 9, "bold"), bd=0, padx=10, cursor="hand2"
        )
        btn_export.pack(side=tk.RIGHT)

        # Tabela (Treeview)
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", font=("Segoe UI", 10), rowheight=30, background="#FFFFFF", fieldbackground="#FFFFFF", borderwidth=0)
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"), background="#EBF3FA", foreground=self.COLOR_NAV)
        style.map("Treeview", background=[("selected", self.COLOR_BANNER)], foreground=[("selected", "#FFFFFF")])

        self.tree = ttk.Treeview(playlist_area, columns=("Titulo", "Artista", "Duracao"), show="headings", height=8)
        self.tree.heading("Titulo", text="MÚSICA")
        self.tree.heading("Artista", text="ARTISTA")
        self.tree.heading("Duracao", text="DURAÇÃO")
        
        self.tree.column("Titulo", width=200)
        self.tree.column("Artista", width=150)
        self.tree.column("Duracao", width=70, anchor="center")
        
        self.tree.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
        self.tree.bind("<Double-1>", self.tocar_musica_selecionada)

        # 4. Player de Música Flutuante / Rodapé (Estilo Spotify/YT Music)
        player_bar = tk.Frame(self.root, bg=self.COLOR_NAV, height=70)
        player_bar.pack(fill=tk.X, side=tk.BOTTOM)

        self.lbl_now_playing = tk.Label(player_bar, text="Nenhuma música tocando", font=("Segoe UI", 9, "bold"), bg=self.COLOR_NAV, fg=self.COLOR_TEXT_LIGHT)
        self.lbl_now_playing.pack(anchor="w", padx=20, pt=5)

        player_controls = tk.Frame(player_bar, bg=self.COLOR_NAV)
        player_controls.pack(fill=tk.X, padx=20, pady=2)

        self.btn_play = tk.Button(player_controls, text="▶ PLAY", command=self.toggle_play, bg=self.COLOR_ACCENT, fg="#000", font=("Segoe UI", 8, "bold"), bd=0, padx=10)
        self.btn_play.pack(side=tk.LEFT, padx=(0, 10))

        self.progress = ttk.Progressbar(player_controls, orient="horizontal", mode="determinate")
        self.progress.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.playlist_atual = []
        self.gerar_playlist()

    # --- AUTOMAÇÃO & PLAYER SIMULADO ---

    def gerar_playlist(self):
        humor = self.humor_var.get()
        self.playlist_atual = buscar_playlist_por_humor(humor)
        
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        for m in self.playlist_atual:
            self.tree.insert("", tk.END, values=(m[0], m[1], m[2]))
            
        # Seleciona automaticamente a primeira música ao gerar
        if self.playlist_atual:
            primeiro = self.tree.get_children()[0]
            self.tree.selection_set(primeiro)
            self.preparar_musica(self.playlist_atual[0])

    def preparar_musica(self, musica):
        self.musica_atual = musica
        self.lbl_now_playing.config(text=f"🎧 Tocando agora: {musica[0]} - {musica[1]} ({musica[2]})")
        self.progresso_val = 0
        self.progress["value"] = 0

    def tocar_musica_selecionada(self, event):
        item = self.tree.selection()
        if item:
            valores = self.tree.item(item, "values")
            self.preparar_musica(valores)
            if not self.tocando:
                self.toggle_play()

    def toggle_play(self):
        if not self.musica_atual and self.playlist_atual:
            self.preparar_musica(self.playlist_atual[0])

        if not self.tocando:
            self.tocando = True
            self.btn_play.config(text="⏸ PAUSE")
            threading.Thread(target=self._simular_player, daemon=True).start()
        else:
            self.tocando = False
            self.btn_play.config(text="▶ PLAY")

    def _simular_player(self):
        while self.tocando and self.progresso_val < 100:
            time.sleep(0.3)
            self.progresso_val += 2
            self.progress["value"] = self.progresso_val
        if self.progresso_val >= 100:
            self.tocando = False
            self.btn_play.config(text="▶ PLAY")
            self.progresso_val = 0

    def salvar_json(self):
        humor = self.humor_var.get()
        if self.playlist_atual:
            arq = exportar_para_json(humor, self.playlist_atual)
            messagebox.showinfo("Sucesso", f"Playlist exportada para o arquivo '{arq}' com sucesso!")

# --- MODO CLI INTERATIVO ---

def rodar_cli():
    print("\n=======================================================")
    print(" 🎵 VIBESTREAM POP ASSISTANT (MODO CLI) ")
    print("=======================================================")
    humores = ["feliz", "triste", "animado", "relaxado", "focado"]
    print("Escolha seu humor atual:", ", ".join(humores))
    
    humor = input("👉 Seu humor agora: ").strip().lower()
    if humor not in humores:
        humor = "feliz"
        
    playlist = buscar_playlist_por_humor(humor)
    print(f"\n🔥 HITS POP EM ALTA PARA SUA VIBE [{humor.upper()}]:")
    print("-" * 55)
    for idx, (t, a, d) in enumerate(playlist, 1):
        print(f"{idx:02d}. 🎶 {t:<25} | 👤 {a:<20} | ⏱️ {d}")
    print("-" * 55)
    
    salvar = input("\n💾 Exportar playlist em JSON? (s/n): ").strip().lower()
    if salvar == 's':
        arq = exportar_para_json(humor, playlist)
        print(f"✅ Arquivo '{arq}' criado!")

# --- EXECUÇÃO PRINCIPAL ---

if __name__ == "__main__":
    inicializar_banco()
    if len(sys.argv) > 1 and sys.argv[1] == "--cli":
        rodar_cli()
    else:
        root = tk.Tk()
        app = WebAppMusicaGUI(root)
        root.mainloop()
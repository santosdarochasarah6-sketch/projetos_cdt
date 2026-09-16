import tkinter as tk
from tkinter import ttk

# --- CORES DA PALETA ---
BG_DARK = "#FFF0F5"       # Rosa Bebê (Fundo Geral)
PANEL_BG = "#FFFACD"      # Amarelo Pastel (Painéis / Cards)
CARD_BG = "#FEF9E7"       # Amarelo Pastel mais claro (Cards)
ACCENT_PURPLE = "#D8BFD8"  # Roxo Claro (Botões e Destaques)
HOVER_PURPLE = "#E6E6FA"   # Roxo bem leve (Hover / Filtros inativos)
TEXT_COLOR = "#4A3B52"     # Roxo bem escuro para texto
TEXT_MUTED = "#8A7A93"     # Roxo acinzentado para subtítulos

class SpotifyPastelApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Meu Player - Estilo Pastel")
        self.geometry("700x700")
        self.geometry("700x700")
        self.configure(bg=BG_DARK)

        # Configuração de Estilos TTK
        self.style = ttk.Style()
        self.style.theme_use("clam")

        # Construção dos componentes da interface
        self.create_top_bar()
        self.create_main_container()
        self.create_bottom_player()

    def create_top_bar(self):
        """Barra Superior: Busca e Perfil"""
        top_frame = tk.Frame(self, bg=BG_DARK, height=60, padding=10)
        top_frame.pack(side="top", fill="x", padx=10, pady=5)

        # Ícone / Botão Home
        home_btn = tk.Button(
            top_frame, text="🏠", font=("Arial", 12),
            bg=ACCENT_PURPLE, fg=TEXT_COLOR, bd=0, relief="flat",
            width=4, height=1, cursor="hand2"
        )
        home_btn.pack(side="left", padx=(0, 10))

        # Barra de Pesquisa
        search_frame = tk.Frame(top_frame, bg=PANEL_BG, bd=1, relief="solid")
        search_frame.pack(side="left", fill="x", expand=True, padx=10)

        search_icon = tk.Label(search_frame, text="🔍", bg=PANEL_BG, fg=TEXT_MUTED)
        search_icon.pack(side="left", padx=8)

        search_entry = tk.Entry(
            search_frame, bg=PANEL_BG, fg=TEXT_COLOR,
            font=("Arial", 11), bd=0, insertbackground=TEXT_COLOR
        )
        search_entry.insert(0, "O que você quer ouvir?")
        search_entry.pack(side="left", fill="x", expand=True, py=6)

        # Botões da direita
        premium_btn = tk.Button(
            top_frame, text="Ver planos Premium", font=("Arial", 9, "bold"),
            bg=ACCENT_PURPLE, fg=TEXT_COLOR, bd=0, relief="flat",
            padx=12, pady=6, cursor="hand2"
        )
        premium_btn.pack(side="right", padx=5)

        profile_btn = tk.Button(
            top_frame, text="👤", font=("Arial", 11),
            bg=PANEL_BG, fg=TEXT_COLOR, bd=0, relief="flat",
            width=3, height=1, cursor="hand2"
        )
        profile_btn.pack(side="right", padx=5)

    def create_main_container(self):
        """Container do Corpo (Barra Lateral + Área Principal)"""
        body_frame = tk.Frame(self, bg=BG_DARK)
        body_frame.pack(side="top", fill="both", expand=True, padx=10, pady=5)

        # ---------------- BARRA LATERAL (ESQUERDA) ----------------
        sidebar = tk.Frame(body_frame, bg=PANEL_BG, width=280)
        sidebar.pack(side="left", fill="y", padx=(0, 10))
        sidebar.pack_propagate(False)

        # Cabeçalho Biblioteca
        lib_header = tk.Frame(sidebar, bg=PANEL_BG)
        lib_header.pack(fill="x", padx=15, pady=15)

        lib_title = tk.Label(
            lib_header, text="📚 Sua Biblioteca", font=("Arial", 12, "bold"),
            bg=PANEL_BG, fg=TEXT_COLOR
        )
        lib_title.pack(side="left")

        add_btn = tk.Label(lib_header, text="＋", font=("Arial", 14, "bold"), bg=PANEL_BG, fg=TEXT_MUTED, cursor="hand2")
        add_btn.pack(side="right")

        # Filtros da Biblioteca
        filter_frame = tk.Frame(sidebar, bg=PANEL_BG)
        filter_frame.pack(fill="x", padx=15, pady=(0, 10))

        for tag in ["Playlists", "Artistas"]:
            btn = tk.Label(
                filter_frame, text=tag, font=("Arial", 9, "bold"),
                bg=HOVER_PURPLE, fg=TEXT_COLOR, padx=10, pady=4, cursor="hand2"
            )
            btn.pack(side="left", padx=(0, 5))

        # Lista de Playlists na Lateral
        playlists = [
            ("Anitta", "Playlist • Sarah"),
            ("Músicas Curtidas", "Playlist • 4 músicas"),
            ("✨ Vôlei ✨", "Playlist • Jessy"),
            ("hokku + sarah", "Playlist • Spotify")
        ]

        for title, subtitle in playlists:
            item = tk.Frame(sidebar, bg=PANEL_BG, cursor="hand2")
            item.pack(fill="x", padx=10, pady=4)

            # Capa (Placeholder Roxo)
            cover = tk.Frame(item, bg=ACCENT_PURPLE, width=40, height=40)
            cover.pack(side="left", padx=(5, 10))
            cover.pack_propagate(False)

            info = tk.Frame(item, bg=PANEL_BG)
            info.pack(side="left", fill="both")

            t_lbl = tk.Label(info, text=title, font=("Arial", 9, "bold"), bg=PANEL_BG, fg=TEXT_COLOR, anchor="w")
            t_lbl.pack(fill="x")
            s_lbl = tk.Label(info, text=subtitle, font=("Arial", 8), bg=PANEL_BG, fg=TEXT_MUTED, anchor="w")
            s_lbl.pack(fill="x")

        # ---------------- CONTEÚDO PRINCIPAL (DIREITA) ----------------
        main_content = tk.Frame(body_frame, bg=PANEL_BG)
        main_content.pack(side="right", fill="both", expand=True)

        # Filtros Principais (Tudo, Músicas, Podcasts)
        main_filters = tk.Frame(main_content, bg=PANEL_BG)
        main_filters.pack(fill="x", padx=20, pady=15)

        for i, tag in enumerate(["Tudo", "Músicas", "Podcasts"]):
            bg_c = ACCENT_PURPLE if i == 0 else HOVER_PURPLE
            btn = tk.Label(
                main_filters, text=tag, font=("Arial", 9, "bold"),
                bg=bg_c, fg=TEXT_COLOR, padx=12, pady=5, cursor="hand2"
            )
            btn.pack(side="left", padx=(0, 8))

        # Título da Seção
        sec_title = tk.Label(
            main_content, text="Singles e álbuns que todo mundo gosta",
            font=("Arial", 14, "bold"), bg=PANEL_BG, fg=TEXT_COLOR
        )
        sec_title.pack(anchor="w", padx=20, pady=(10, 15))

        # Grid de Cards de Álbuns
        cards_frame = tk.Frame(main_content, bg=PANEL_BG)
        cards_frame.pack(fill="x", padx=20)

        albums = [
            ("Nada Como um Dia...", "Racionais MC's"),
            ("Churrasquinho 3", "Grupo Menos É Mais"),
            ("Tubarões (Ao Vivo)", "Diego & Victor Hugo"),
            ("Bem-Vindo ao Meu...", "Wesley Safadão"),
            ("Manifesto Musical 2", "Henrique & Juliano")
        ]

        for title, artist in albums:
            card = tk.Frame(cards_frame, bg=CARD_BG, width=130, height=190, relief="solid", bd=1)
            card.pack(side="left", padx=8)
            card.pack_propagate(False)

            # Capa Imagem Placeholder
            img_box = tk.Frame(card, bg=ACCENT_PURPLE, height=110)
            img_box.pack(fill="x", padx=8, pady=8)

            icon_lbl = tk.Label(img_box, text="🎵", font=("Arial", 24), bg=ACCENT_PURPLE, fg=TEXT_COLOR)
            icon_lbl.place(relx=0.5, rely=0.5, anchor="center")

            # Título e Artista
            t_lbl = tk.Label(card, text=title, font=("Arial", 8, "bold"), bg=CARD_BG, fg=TEXT_COLOR, wraplength=110, justify="left")
            t_lbl.pack(anchor="w", padx=8)

            a_lbl = tk.Label(card, text=artist, font=("Arial", 8), bg=CARD_BG, fg=TEXT_MUTED, wraplength=110, justify="left")
            a_lbl.pack(anchor="w", padx=8, pady=(2, 0))

    def create_bottom_player(self):
        """Barra Inferior do Player de Música"""
        player_frame = tk.Frame(self, bg=BG_DARK, height=70)
        player_frame.pack(side="bottom", fill="x", padx=10, pady=5)

        # Esquerda: Informações da música atual
        track_info = tk.Frame(player_frame, bg=BG_DARK)
        track_info.pack(side="left", padx=10)

        track_title = tk.Label(track_info, text="Nome da Música", font=("Arial", 9, "bold"), bg=BG_DARK, fg=TEXT_COLOR)
        track_title.pack(anchor="w")
        artist_title = tk.Label(track_info, text="Nome do Artista", font=("Arial", 8), bg=BG_DARK, fg=TEXT_MUTED)
        artist_title.pack(anchor="w")

        # Centro: Controles e Barra de Progresso
        controls_frame = tk.Frame(player_frame, bg=BG_DARK)
        controls_frame.pack(side="left", fill="x", expand=True)

        buttons_box = tk.Frame(controls_frame, bg=BG_DARK)
        buttons_box.pack()

        for btn_text in ["🔀", "⏮", "▶", "⏭", "🔁"]:
            b = tk.Button(
                buttons_box, text=btn_text, font=("Arial", 10),
                bg=BG_DARK, fg=TEXT_COLOR, bd=0, activebackground=BG_DARK, cursor="hand2"
            )
            b.pack(side="left", padx=8)

        # Barra de Progresso
        progress_box = tk.Frame(controls_frame, bg=BG_DARK)
        progress_box.pack(fill="x", padx=50, pady=(2, 0))

        time_start = tk.Label(progress_box, text="0:00", font=("Arial", 7), bg=BG_DARK, fg=TEXT_MUTED)
        time_start.pack(side="left")

        progress_bar = ttk.Progressbar(progress_box, orient="horizontal", mode="determinate", value=30)
        progress_bar.pack(side="left", fill="x", expand=True, padx=5)

        time_end = tk.Label(progress_box, text="3:45", font=("Arial", 7), bg=BG_DARK, fg=TEXT_MUTED)
        time_end.pack(side="right")

        # Direita: Controle de Volume
        volume_frame = tk.Frame(player_frame, bg=BG_DARK)
        volume_frame.pack(side="right", padx=10)

        vol_icon = tk.Label(volume_frame, text="🔊", bg=BG_DARK, fg=TEXT_COLOR)
        vol_icon.pack(side="left", padx=2)

        vol_bar = ttk.Scale(volume_frame, from_=0, to=100, value=70, orient="horizontal", length=80)
        vol_bar.pack(side="left")

if __name__ == "__main__":
    app = SpotifyPastelApp()
    app.mainloop()
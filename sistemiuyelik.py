import tkinter as tk
from tkinter import messagebox
import subprocess, sys, tempfile, textwrap, os

# --- Kullanıcı verileri (csv yerine kod içinde) ---
USERS = {
    "taha": "6767",
    "mami": "2013",
    "yigirit": "0101",
    "dursun": "3169"
}

# --- Login Ekranı ---
class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Giriş Ekranı")
        self.root.geometry("300x200")
        tk.Label(root, text="Kullanıcı Adı:").pack(pady=5)
        self.user_entry = tk.Entry(root)
        self.user_entry.pack()
        tk.Label(root, text="Şifre:").pack(pady=5)
        self.pass_entry = tk.Entry(root, show="*")
        self.pass_entry.pack()
        tk.Button(root, text="Giriş Yap", command=self.login).pack(pady=10)
        self.root.bind("<Return>", lambda e: self.login())

    def login(self):
        user = self.user_entry.get().strip()
        pw = self.pass_entry.get().strip()
        if user in USERS and USERS[user] == pw:
            messagebox.showinfo("Başarılı", f"Hoşgeldin {user}!")
            self.root.destroy()
            MainMenu(user)
        else:
            messagebox.showerror("Hata", "Kullanıcı adı veya şifre yanlış.")

# --- Ana Menü ---
class MainMenu:
    def __init__(self, username):
        self.username = username
        self.win = tk.Tk()
        self.win.title(f"Hoşgeldin {username}")
        self.win.geometry("400x300")
        tk.Label(self.win, text=f"Merhaba {username}!", font=("Arial", 14, "bold")).pack(pady=10)
        tk.Button(self.win, text="🧮 Hesap Makinesi", width=25, command=self.open_calc).pack(pady=8)
        tk.Button(self.win, text="🐍 Yılan Oyunu", width=25, command=self.open_snake).pack(pady=8)
        tk.Button(self.win, text="🐤 Flappy Bird", width=25, command=self.open_flappy).pack(pady=8)
        tk.Button(self.win, text="Çıkış", width=25, command=self.win.destroy).pack(pady=20)
        self.win.mainloop()

    def open_calc(self):
        top = tk.Toplevel(self.win)
        top.title("Hesap Makinesi")
        top.geometry("300x400")
        entry = tk.Entry(top, font=("Arial", 18))
        entry.pack(fill="x", padx=10, pady=10)
        def add_text(t): entry.insert("end", t)
        def calc():
            try:
                result = eval(entry.get())
                entry.delete(0, "end")
                entry.insert("end", str(result))
            except Exception:
                entry.delete(0, "end")
                entry.insert("end", "Hata")
        btns = [
            "7","8","9","/",
            "4","5","6","*",
            "1","2","3","-",
            "0",".","=","+"
        ]
        frame = tk.Frame(top)
        frame.pack()
        for i,b in enumerate(btns):
            cmd = (lambda x=b: calc() if x=="=" else add_text(x))
            tk.Button(frame, text=b, width=5, height=2, command=cmd).grid(row=i//4, column=i%4, padx=2, pady=2)
        tk.Button(top, text="Temizle", command=lambda: entry.delete(0,"end")).pack(pady=5)

    def open_snake(self):
        code = textwrap.dedent("""
        import pygame, sys, random
        pygame.init()
        size = (500,500)
        screen = pygame.display.set_mode(size)
        pygame.display.set_caption("Yılan Oyunu")
        clock = pygame.time.Clock()
        snake = [(100,100),(90,100),(80,100)]
        direction = (10,0)
        food = (200,200)
        score = 0
        font = pygame.font.Font(None, 36)
        while True:
            for e in pygame.event.get():
                if e.type == pygame.QUIT: pygame.quit(); sys.exit()
                elif e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_UP and direction!=(0,10): direction=(0,-10)
                    elif e.key == pygame.K_DOWN and direction!=(0,-10): direction=(0,10)
                    elif e.key == pygame.K_LEFT and direction!=(10,0): direction=(-10,0)
                    elif e.key == pygame.K_RIGHT and direction!=(-10,0): direction=(10,0)
            new_head = (snake[0][0]+direction[0], snake[0][1]+direction[1])
            if new_head in snake or not (0<=new_head[0]<500 and 0<=new_head[1]<500):
                pygame.quit(); sys.exit()
            snake.insert(0,new_head)
            if new_head == food:
                score+=1
                food = (random.randrange(0,50)*10, random.randrange(0,50)*10)
            else:
                snake.pop()
            screen.fill((0,0,0))
            for s in snake: pygame.draw.rect(screen,(0,255,0),(s[0],s[1],10,10))
            pygame.draw.rect(screen,(255,0,0),(food[0],food[1],10,10))
            txt = font.render(f"Skor: {score}", True, (255,255,255))
            screen.blit(txt,(10,10))
            pygame.display.flip()
            clock.tick(15)
        """)
        self._run_game(code)

    def open_flappy(self):
        # 🔧 Düzeltilmiş flappy bird
        code = textwrap.dedent("""
        import pygame, sys, random
        pygame.init()
        W,H = 400,600
        screen = pygame.display.set_mode((W,H))
        pygame.display.set_caption("Flappy Bird")
        clock = pygame.time.Clock()
        bird = pygame.Rect(100,300,34,24)
        gravity = 0.5
        velocity = 0
        pipes = []
        gap = 150
        score = 0
        font = pygame.font.Font(None, 36)

        PIPE_SPAWN = pygame.USEREVENT + 1
        pygame.time.set_timer(PIPE_SPAWN, 1500)

        def new_pipe():
            y = random.randint(150, 450)
            pipes.append([W, y])

        new_pipe()

        running = True
        while running:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                if e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
                    velocity = -8
                if e.type == PIPE_SPAWN:
                    new_pipe()

            # Fizik
            velocity += gravity
            bird.y += int(velocity)

            # Oyun bitti mi
            if bird.y > H - 40 or bird.y < 0:
                running = False

            # Boru hareketi
            for p in pipes:
                p[0] -= 4

            # Boruları temizle
            pipes = [p for p in pipes if p[0] > -60]

            # Çizim
            screen.fill((135,206,235))  # gökyüzü
            for p in pipes:
                top_rect = pygame.Rect(p[0], 0, 60, p[1] - gap//2)
                bottom_rect = pygame.Rect(p[0], p[1] + gap//2, 60, H - p[1])
                pygame.draw.rect(screen, (0,255,0), top_rect)
                pygame.draw.rect(screen, (0,255,0), bottom_rect)
                # Skor
                if p[0] + 60 == bird.x:
                    score += 1

                if bird.colliderect(top_rect) or bird.colliderect(bottom_rect):
                    running = False

            pygame.draw.rect(screen, (255,255,0), bird)
            txt = font.render(f"Skor: {score}", True, (0,0,0))
            screen.blit(txt, (10,10))

            pygame.display.flip()
            clock.tick(60)

        pygame.quit()
        sys.exit()
        """)
        self._run_game(code)

    def _run_game(self, code):
        fd, tmp = tempfile.mkstemp(suffix=".py", text=True)
        with os.fdopen(fd, "w") as f: f.write(code)
        subprocess.Popen([sys.executable, tmp])

# --- Çalıştır ---
if __name__ == "__main__":
    root = tk.Tk()
    app = LoginApp(root)
    root.mainloop()

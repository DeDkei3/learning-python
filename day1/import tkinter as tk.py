import tkinter as tk
from tkinter import messagebox
import random

class RPGGame:
    def __init__(self, root):
        self.root = root
        self.root.title("2D RPG Боёвка")
        self.root.geometry("520x460")
        self.root.configure(bg="#1e1e1e")

        # Характеристики
        self.player_hp = 60
        self.player_max_hp = 60
        self.player_damage = 12
        self.player_armor = 3

        self.monster_hp = 40
        self.monster_max_hp = 40
        self.monster_damage = 8
        self.monster_name = "Гоблин-копейщик"

        # Создание интерфейса
        self.create_widgets()

    def create_widgets(self):
        # Заголовок
        title_label = tk.Label(self.root, text="⚔️ СРАЖЕНИЕ", font=("Arial", 16, "bold"), bg="#1e1e1e", fg="white")
        title_label.pack(pady=10)

        # Панели статусов
        status_frame = tk.Frame(self.root, bg="#1e1e1e")
        status_frame.pack(pady=5)

        # Статус Игрока
        self.lbl_player = tk.Label(status_frame, text=f"👤 Александр\nHP: {self.player_hp}/{self.player_max_hp}\n⚔️ Урон: {self.player_damage}", 
                                  font=("Arial", 11), bg="#2d2d2d", fg="#4cd137", padx=15, pady=10, relief="groove", bd=2)
        self.lbl_player.grid(row=0, column=0, padx=10)

        # Статус Монстра
        self.lbl_monster = tk.Label(status_frame, text=f"👹 {self.monster_name}\nHP: {self.monster_hp}/{self.monster_max_hp}\n⚔️ Урон: {self.monster_damage}", 
                                   font=("Arial", 11), bg="#2d2d2d", fg="#e84118", padx=15, pady=10, relief="groove", bd=2)
        self.lbl_monster.grid(row=0, column=1, padx=10)

        # Текстовый лог боя
        self.log_box = tk.Text(self.root, height=8, width=58, bg="#121212", fg="#f5f6fa", font=("Consolas", 10))
        self.log_box.pack(pady=15)
        self.log_box.insert(tk.END, "Бой начался! Сделай свой ход.\n")
        self.log_box.config(state=tk.DISABLED)

        # Панель кнопок управления
        btn_frame = tk.Frame(self.root, bg="#1e1e1e")
        btn_frame.pack(pady=5)

        self.btn_attack = tk.Button(btn_frame, text="⚔️ Атака", command=self.action_attack, width=12, bg="#0097e6", fg="white", font=("Arial", 10, "bold"))
        self.btn_attack.grid(row=0, column=0, padx=6)

        self.btn_defend = tk.Button(btn_frame, text="🛡 Защита", command=self.action_defend, width=12, bg="#40739e", fg="white", font=("Arial", 10, "bold"))
        self.btn_defend.grid(row=0, column=1, padx=6)

        self.btn_flee = tk.Button(btn_frame, text="🏃 Сбежать", command=self.action_flee, width=12, bg="#e1b12c", fg="white", font=("Arial", 10, "bold"))
        self.btn_flee.grid(row=0, column=2, padx=6)

    def log(self, message):
        """Добавляет строку в текстовый лог на экране"""
        self.log_box.config(state=tk.NORMAL)
        self.log_box.insert(tk.END, message + "\n")
        self.log_box.see(tk.END)
        self.log_box.config(state=tk.DISABLED)

    def update_labels(self):
        """Обновляет цифры HP на экранах статусов"""
        self.lbl_player.config(text=f"👤 Александр\nHP: {max(0, self.player_hp)}/{self.player_max_hp}\n⚔️ Урон: {self.player_damage}")
        self.lbl_monster.config(text=f"👹 {self.monster_name}\nHP: {max(0, self.monster_hp)}/{self.monster_max_hp}\n⚔️ Урон: {self.monster_damage}")

    def action_attack(self):
        if self.monster_hp <= 0 or self.player_hp <= 0:
            return

        # Ход игрока
        dmg = random.randint(self.player_damage - 2, self.player_damage + 2)
        self.monster_hp -= dmg
        self.log(f"💥 Ты нанёс {dmg} урона!")
        self.update_labels()

        if self.monster_hp <= 0:
            self.log(f"🎉 ПОБЕДА! {self.monster_name} повержен!")
            self.disable_buttons()
            messagebox.showinfo("Победа!", "Ты победил монстра!")
            return

        # Ход монстра
        self.monster_turn()

    def action_defend(self):
        if self.monster_hp <= 0 or self.player_hp <= 0:
            return

        self.log("🛡 Ты встал в защиту (+5 брони на этот ход)!")
        original_armor = self.player_armor
        self.player_armor += 5
        
        # Ход монстра с учетом временной брони
        self.monster_turn()
        self.player_armor = original_armor  # Возвращаем стандартную броню

    def action_flee(self):
        if random.random() < 0.5:
            self.log("🏃 Ты успешно сбежал с поля боя!")
            self.disable_buttons()
            messagebox.showinfo("Побег", "Ты успешно сбежал!")
        else:
            self.log("❌ Побег не удался! Враг преградил путь.")
            self.monster_turn()

    def monster_turn(self):
        effective_dmg = max(1, self.monster_damage - self.player_armor)
        self.player_hp -= effective_dmg
        self.log(f"👹 {self.monster_name} наносит тебе {effective_dmg} урона.")
        self.update_labels()

        if self.player_hp <= 0:
            self.log("☠️ Ты погиб... Игра окончена.")
            self.disable_buttons()
            messagebox.showerror("Поражение", "Ты проиграл бой!")

    def disable_buttons(self):
        self.btn_attack.config(state=tk.DISABLED)
        self.btn_defend.config(state=tk.DISABLED)
        self.btn_flee.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = RPGGame(root)
    root.mainloop()
import tkinter as tk
from tkinter import messagebox, scrolledtext
import os

from game import Game
from word_list import WordList

RULES_FILE = os.path.join(os.path.dirname(__file__), 'rules.txt')


class WordleGameFrame(tk.Frame):
    """Frame que contiene el juego Wordle (reutiliza la lógica existente)."""

    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.game = Game()
        self.valid_length = WordList.VALID_LENGTH
        self.max_attempts = self.game.get_intentos_restantes()
        self.current_attempt = 0
        self.entries_rows = []
        self._build_ui()

    def _build_ui(self):
        self.status_var = tk.StringVar(value="Escribe una palabra para jugar")
        status = tk.Label(self, textvariable=self.status_var, font=(None, 12))
        status.grid(row=0, column=0, columnspan=self.valid_length, pady=(10, 5))

        grid_frame = tk.Frame(self)
        grid_frame.grid(row=1, column=0, padx=10, pady=5)

        entry_font = ("Helvetica", 24, "bold")

        for r in range(self.max_attempts):
            row_entries = []
            for c in range(self.valid_length):
                e = tk.Entry(grid_frame, width=2, font=entry_font, justify='center')
                e.grid(row=r, column=c, padx=5, pady=5)
                if r != 0:
                    e.config(state='disabled')
                e.bind('<Key>', lambda ev, rr=r, cc=c: self._on_key(ev, rr, cc))
                e.bind('<FocusIn>', lambda ev, rr=r, cc=c: self._on_focus(ev, rr, cc))
                # valida para permitir solo una letra
                e.config(validate='key', validatecommand=(self.register(self._validate_entry), '%P'))
                row_entries.append(e)
            self.entries_rows.append(row_entries)

        buttons_frame = tk.Frame(self)
        buttons_frame.grid(row=2, column=0, pady=(5, 10))

        listo_btn = tk.Button(buttons_frame, text='Listo', command=self.submit_guess, width=10)
        listo_btn.pack(side='left', padx=5)

        reiniciar_btn = tk.Button(buttons_frame, text='Reiniciar', command=self.restart, width=10)
        reiniciar_btn.pack(side='left', padx=5)

        # tecla enter
        self.bind_all('<Return>', self._on_return)

        
        self.after(50, lambda: self._focus_cell(0, 0))

    def _on_return(self, event):
        
        widget = self.focus_get()
        if not widget:
            return
        
        for idx, row in enumerate(self.entries_rows):
            if widget in row:
                if idx == self.current_attempt:
                    self.submit_guess()
                return

    def _on_focus(self, event, row, col):
        if row != self.current_attempt:
            event.widget.master.focus()

    def _on_key(self, event, row, col):
        if row != self.current_attempt:
            return 'break'

        key = event.keysym
        widget = event.widget

        if key == 'BackSpace':
            if widget.get() == '':
                if col > 0:
                    prev = self.entries_rows[row][col-1]
                    prev.config(state='normal')
                    prev.focus()
                    prev.delete(0, 'end')
            return

        if key == 'Return':
            self.submit_guess()
            return 'break'

        # ahce que solo se pueda una letra
        if len(event.char) == 1 and event.char.isalpha():
            widget.delete(0, 'end')
            widget.insert(0, event.char.upper())
            if col + 1 < self.valid_length:
                nxt = self.entries_rows[row][col+1]
                nxt.config(state='normal')
                nxt.focus()
            return 'break'

        return 'break'

    def _focus_cell(self, row, col):
        try:
            cell = self.entries_rows[row][col]
            cell.config(state='normal')
            cell.focus()
        except Exception:
            pass

    def _validate_entry(self, proposed: str) -> bool:
        if proposed == "":
            return True
        if len(proposed) > 1:
            return False
        return proposed.isalpha()

    def get_current_word(self):
        letters = []
        for e in self.entries_rows[self.current_attempt]:
            val = e.get().strip()
            letters.append(val.lower() if val else '')
        return ''.join(letters)

    def submit_guess(self, event=None):
        word = self.get_current_word()
        if len(word) != self.valid_length or any(len(ch) == 0 for ch in word):
            self.status_var.set('Completa todas las casillas antes de enviar ({} letras).'.format(self.valid_length))
            return

        resultados, is_length_valid, is_known, is_winner = self.game.check_word(word)
        if not is_length_valid:
            self.status_var.set('Longitud inválida.')
            return

        # si la palabra no fue encontrada devuelve Game(None, True, False, False)
        if resultados is None:
            self.status_var.set('Palabra no encontrada en la lista, Intenta otra')
            return

        colors = {
            'verde': '#6aaa64',
            'amarillo': '#c9b458',
            'rojo': '#787c7e'
        }

        for idx, (letter, estado) in enumerate(resultados):
            e = self.entries_rows[self.current_attempt][idx]
            e.config(disabledbackground=colors.get(estado, '#ffffff'), disabledforeground='white')
            e.delete(0, 'end')
            e.insert(0, letter.upper())
            e.config(state='disabled')

        if not is_known:
            self.status_var.set('Palabra incorrecta, se muestran las pistas.')
        else:
            self.status_var.set('Palabra correcta.')

        if is_winner:
            messagebox.showinfo('¡Ganaste!', '¡Felicidades! La palabra era {}'.format(self.game.get_palabra_secreta()))
            return

        self.current_attempt += 1
        if self.current_attempt >= self.max_attempts:
            messagebox.showinfo('Perdiste', 'Has agotado los intentos. La palabra era {}'.format(self.game.get_palabra_secreta()))
            return

        for e in self.entries_rows[self.current_attempt]:
            e.config(state='normal')
            e.delete(0, 'end')
        self._focus_cell(self.current_attempt, 0)

    def restart(self):
        self.game = Game()
        self.current_attempt = 0
        self.max_attempts = self.game.get_intentos_restantes()
        self.status_var.set("Juego reiniciado")
        for r, row in enumerate(self.entries_rows):
            for e in row:
                e.config(state='normal')
                e.delete(0, 'end')
                e.config(bg='SystemButtonFace', fg='black')
                try:
                    e.config(disabledbackground='SystemButtonFace', disabledforeground='black')
                except Exception:
                    pass
            if r != 0:
                for e in row:
                    e.config(state='disabled')
        self._focus_cell(0, 0)


class RulesFrame(tk.Frame):
    """Frame para mostrar y editar reglas desde un archivo de texto."""

    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self._build_ui()
        self._load_rules()

    def _build_ui(self):
        label = tk.Label(self, text='Reglas del juego', font=(None, 14, 'bold'))
        label.pack(pady=(10, 5))

        self.text = scrolledtext.ScrolledText(self, width=60, height=15)
        self.text.pack(padx=10, pady=5)

        save_btn = tk.Button(self, text='Guardar reglas', command=self._save_rules)
        save_btn.pack(pady=(5, 10))

    def _load_rules(self):
        try:
            with open(RULES_FILE, 'r', encoding='utf-8') as f:
                content = f.read()
        except FileNotFoundError:
            content = ''
        self.text.delete('1.0', tk.END)
        self.text.insert(tk.END, content)

    def _save_rules(self):
        with open(RULES_FILE, 'w', encoding='utf-8') as f:
            f.write(self.text.get('1.0', tk.END))
        messagebox.showinfo('Reglas', 'Reglas guardadas correctamente')


class MainMenuApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Wordle - Menú')
        self.geometry('600x600')
        self.resizable(False, False)

        self.container = tk.Frame(self)
        self.container.pack(fill='both', expand=True)

        self._build_menu()
        self.game_frame = None
        self.rules_frame = None

    def _build_menu(self):
        menu_frame = tk.Frame(self.container)
        menu_frame.place(relx=0.5, rely=0.4, anchor='center')

        title = tk.Label(menu_frame, text='WORDLE', font=(None, 36, 'bold'))
        title.pack(pady=(0, 20))

        play_btn = tk.Button(menu_frame, text='Jugar', width=20, height=2, command=self._start_game)
        play_btn.pack(pady=10)

        rules_btn = tk.Button(menu_frame, text='Ver reglas', width=20, height=2, command=self._show_rules)
        rules_btn.pack(pady=10)

        exit_btn = tk.Button(menu_frame, text='Salir', width=20, height=2, command=self._exit)
        exit_btn.pack(pady=10)

    def _start_game(self):
        for child in self.container.winfo_children():
            child.destroy()
        self.game_frame = WordleGameFrame(self.container)
        self.game_frame.pack(fill='both', expand=True)

    def _show_rules(self):
        for child in self.container.winfo_children():
            child.destroy()
        self.rules_frame = RulesFrame(self.container)
        self.rules_frame.pack(fill='both', expand=True)

        back_btn = tk.Button(self.container, text='Volver', command=self._back_to_menu)
        back_btn.pack(pady=(5, 10))

    def _back_to_menu(self):
        for child in self.container.winfo_children():
            child.destroy()
        self._build_menu()

    def _exit(self):
        messagebox.showinfo('Salir', 'Gracias por jugar! ')
        self.destroy()


def main():
    app = MainMenuApp()
    app.mainloop()


if __name__ == '__main__':
    main()

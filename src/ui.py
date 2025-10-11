import tkinter as tk
from tkinter import messagebox, scrolledtext
import os

from game import Game
from word_list import WordList

RULES_FILE = os.path.join(os.path.dirname(__file__), 'rules.txt')


class WordleGameFrame(tk.Frame):
    """Frame that contains the Wordle game (reuses the existing logic).

    Español: Frame que contiene el juego Wordle y reutiliza la lógica del
    módulo `game.py`. Este widget es configurable por longitud (5/6/7 letras)
    y expone un callback `on_back` para volver al menú.
    """

    def __init__(self, master=None, length: int = 6, on_back=None, **kwargs):
        super().__init__(master, **kwargs)
        self.length = length
        self.on_back = on_back
        self.game = Game(length=self.length)
        self.valid_length = self.length
        self.max_attempts = self.game.get_intentos_restantes()
        self.current_attempt = 0
        self.entries_rows = []
        self._build_ui()

    def _build_ui(self):
        # Status label (multilingual-friendly text variable)
        # Label de estado (texto manejado por variable para facilidad de traducción)
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
                # Bindings: key and focus handlers
                # Enlaces: manejadores de tecla y foco
                e.bind('<Key>', lambda ev, rr=r, cc=c: self._on_key(ev, rr, cc))
                e.bind('<FocusIn>', lambda ev, rr=r, cc=c: self._on_focus(ev, rr, cc))
                # Validate input: only allow a single alphabetic character
                # Validación: solo permitir un carácter alfabético por casilla
                e.config(validate='key', validatecommand=(self.register(self._validate_entry), '%P'))
                row_entries.append(e)
            self.entries_rows.append(row_entries)

        buttons_frame = tk.Frame(self)
        buttons_frame.grid(row=2, column=0, pady=(5, 10))

        listo_btn = tk.Button(buttons_frame, text='Listo', command=self.submit_guess, width=10)
        listo_btn.pack(side='left', padx=5)

        reiniciar_btn = tk.Button(buttons_frame, text='Reiniciar', command=self.restart, width=10)
        reiniciar_btn.pack(side='left', padx=5)
        back_btn = tk.Button(buttons_frame, text='Volver', command=self._on_back, width=10)
        back_btn.pack(side='left', padx=5)

        # Bind global Enter to submit when focus is inside the active row.
        # Enlaza Enter globalmente para enviar cuando el foco esté en la fila activa.
        self.bind_all('<Return>', self._on_return)

        # focus first cell
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
            # Offer options: play again or go back
            # Ofrece opciones: jugar de nuevo o volver atrás.
            again = messagebox.askyesno('¡Ganaste!', '¡Felicidades! La palabra era {}.\n¿Jugar de nuevo?'.format(self.game.get_palabra_secreta()))
            if again:
                self.restart()
            else:
                self._on_back()
            return

        self.current_attempt += 1
        if self.current_attempt >= self.max_attempts:
            again = messagebox.askyesno('Perdiste', 'Has agotado los intentos. La palabra era {}.\n¿Jugar de nuevo?'.format(self.game.get_palabra_secreta()))
            if again:
                self.restart()
            else:
                self._on_back()
            return

        for e in self.entries_rows[self.current_attempt]:
            e.config(state='normal')
            e.delete(0, 'end')
        self._focus_cell(self.current_attempt, 0)

    def restart(self):
        self.game = Game()
        # ensure game uses the same length when restarting
        # se asegura de que use la misma longitud cuando se reinicia
        self.game = Game(length=self.length)
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

    def _on_back(self):
        # callback to return to menu
        # función de retorno para volver al menú
        try:
            # unbind Enter globally for this frame
            # desasocia la tecla Enter globalmente para este marco
            self.unbind_all('<Return>')
        except Exception:
            pass

        # destroy this frame's widgets to avoid layering
        # destruye los widgets de este marco para evitar superposiciones
        try:
            for child in self.winfo_children():
                child.destroy()
        except Exception:
            pass

        if callable(self.on_back):
            self.on_back()
        else:
            # default: destroy parent content and rebuild menu if available
            # predeterminado: destruye el contenido principal y reconstruye el menú si está disponible
            root = self.master
            try:
                for child in root.winfo_children():
                    child.destroy()
            except Exception:
                pass


class RulesFrame(tk.Frame):
    """Frame to display and edit rules from a text file.
       Frame para mostrar y editar reglas desde un archivo de texto.
    """

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

        # Use a single active frame inside `self.container` to avoid
        # leftover widgets or stacked frames. We store it in
        # `self.current_frame` and always destroy it before switching.
        # Usar un único frame activo para evitar widgets residuales.
        self.current_frame = None

        self._build_menu()

    def _build_menu(self):
        # Always clear the container before building the main menu. This
        # removes any leftover widgets (including stray buttons created by
        # earlier views) and guarantees a clean menu state.
        # Siempre limpiar el contenedor antes de construir el menú.
        for child in self.container.winfo_children():
            try:
                child.destroy()
            except Exception:
                pass

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

        # Track the active menu frame so other flows can destroy it explicitly
        # when switching views.
        self.current_frame = menu_frame

    def _start_game(self):
        # Show mode selection (5 or 7 letters)
        # muestra los modos (5 o 7 letras)
        # Replace the current frame with the mode selection frame.
        if self.current_frame is not None:
            try:
                self.current_frame.destroy()
            except Exception:
                for child in self.container.winfo_children():
                    child.destroy()
            self.current_frame = None

        mode_frame = tk.Frame(self.container)
        mode_frame.place(relx=0.5, rely=0.4, anchor='center')
        self.current_frame = mode_frame

        title = tk.Label(mode_frame, text='Selecciona modo', font=(None, 24, 'bold'))
        title.pack(pady=(0, 20))

        btn5 = tk.Button(mode_frame, text='Jugar - 5 letras', width=20, height=2, command=lambda: self._launch_mode(5))
        btn5.pack(pady=8)

        btn7 = tk.Button(mode_frame, text='Jugar - 7 letras', width=20, height=2, command=lambda: self._launch_mode(7))
        btn7.pack(pady=8)

        # Use the safe back callback which clears the container and rebuilds
        # the menu. This prevents the previous frame from remaining visible
        # underneath the new menu.
        # Usa el retorno seguro que limpia el contenedor y reconstruye el menú.
        back_btn = tk.Button(mode_frame, text='Volver', width=20, height=2, command=self._back_to_menu)
        back_btn.pack(pady=8)

    def _launch_mode(self, length: int):
        # Replace the current frame with the game frame
        # Remplaza el frame actual con el frame del juego
        if self.current_frame is not None:
            try:
                self.current_frame.destroy()
            except Exception:
                for child in self.container.winfo_children():
                    child.destroy()
            self.current_frame = None

        game_frame = WordleGameFrame(self.container, length=length, on_back=self._back_to_menu)
        game_frame.pack(fill='both', expand=True)
        self.current_frame = game_frame

    def _show_rules(self):
        # Replace the current frame with the rules frame
        # Remplaza el frame actual con el frame de las reglas
        if self.current_frame is not None:
            try:
                self.current_frame.destroy()
            except Exception:
                for child in self.container.winfo_children():
                    child.destroy()
            self.current_frame = None

        rules_frame = RulesFrame(self.container)
        rules_frame.pack(fill='both', expand=True)
        self.current_frame = rules_frame

        # Place the back button inside the rules frame so it is part of the
        # same widget tree and will be destroyed together with the frame.
        # Coloca el botón 'Volver' dentro del frame de reglas.
        back_btn = tk.Button(rules_frame, text='Volver', command=self._back_to_menu)
        back_btn.pack(pady=(5, 10))

    def _back_to_menu(self):

        if self.current_frame is not None:
            try:
                self.current_frame.destroy()
            except Exception:
                for child in self.container.winfo_children():
                    child.destroy()
            self.current_frame = None
        self._build_menu()

    def _exit(self):
        messagebox.showinfo('Salir', 'Gracias por jugar! ')
        self.destroy()


def main():
    app = MainMenuApp()
    app.mainloop()


if __name__ == '__main__':
    main()

import tkinter as tk
from tkinter import messagebox

from game import Game
from word_list import WordList


class WordleUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Wordle - GUI")
        self.resizable(False, False)

        self.game = Game()
        self.valid_length = WordList.VALID_LENGTH
        self.max_attempts = self.game.get_intentos_restantes()
        self.current_attempt = 0

        self.entries_rows = []

        self._build_ui()

    def _build_ui(self):
        # mensajr / estado de label
        self.status_var = tk.StringVar(value="Escribe una palabra para jugar")
        status = tk.Label(self, textvariable=self.status_var, font=(None, 12))
        status.grid(row=0, column=0, columnspan=self.valid_length, pady=(10, 5))

        # Grid frame
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
                else:
                    
                    pass
                # bindea una key para poder pasar al siguiente cuadro cuando se pone un caracter
                e.bind('<Key>', lambda ev, rr=r, cc=c: self._on_key(ev, rr, cc))
                # valida para evitar poner mas de un caracter en cada cuadro
                e.config(validate='key', validatecommand=(self.register(self._validate_entry), '%P'))
                # navigacion/backspace
                e.bind('<FocusIn>', lambda ev, rr=r, cc=c: self._on_focus(ev, rr, cc))
                row_entries.append(e)
            self.entries_rows.append(row_entries)

        # botones
        buttons_frame = tk.Frame(self)
        buttons_frame.grid(row=2, column=0, pady=(5, 10))

        listo_btn = tk.Button(buttons_frame, text='Listo', command=self.submit_guess, width=10)
        listo_btn.pack(side='left', padx=5)

        reiniciar_btn = tk.Button(buttons_frame, text='Reiniciar', command=self.restart, width=10)
        reiniciar_btn.pack(side='left', padx=5)

        # bindea la tecla Enter
        self.bind('<Return>', self.submit_guess)

        
        self.after(50, lambda: self._focus_cell(0, 0))

    def _on_focus(self, event, row, col):
        
        if row != self.current_attempt:
            event.widget.master.focus()

    def _on_key(self, event, row, col):
        
        if row != self.current_attempt:
            return 'break'

        key = event.keysym
        widget = event.widget

        if key == 'BackSpace':
            # borra el caracter actual y vuelve una casilla atras
            if widget.get() == '':
                if col > 0:
                    prev = self.entries_rows[row][col-1]
                    prev.config(state='normal')
                    prev.focus()
                    prev.delete(0, 'end')
            return

        if key == 'Return':
            # enter para aceptar
            self.submit_guess()
            return 'break'

        if len(event.char) == 1 and event.char.isalpha():
            # remplaza la casilla vacia con la tecla presionada y avanza a la siguiente 
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

        # el color de las celdas dependiendo si esta bien, en el lugar incorrecto o esta mal
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
            self.status_var.set('Palabra correcta!')

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
        # reinicia el juego y limpia la UI
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


def main():
    app = WordleUI()
    app.mainloop()


if __name__ == '__main__':
    main()

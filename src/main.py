import sys
from game import Game

try:
    from ui import MainMenuApp
except Exception:
    MainMenuApp = None


def cli_main():
    """Run the original CLI loop.

    This is preserved for users who prefer the terminal. Use the
    `--cli` argument to force CLI mode.
    """
    juego = Game()

    # si falla, juego por consola
    while juego.get_intentos_restantes() > 0:
        entrada = input("Ingrese una palabra: ")

        resultados, is_length_valid, is_known_word, is_winner = juego.check_word(entrada)

        if not is_length_valid:
            print("Palabra incorrecta o de longitud inválida (longitud inválida).\n")
            continue

        if not is_known_word:
            print("Palabra no encontrada en la lista. Intenta otra.\n")
            continue

        for letra, estado in resultados:
            print(f"{letra} -> {estado}", end=" | ")
        print("\n")

        if is_winner:
            print("¡GANASTE!")
            return

    print(f"PERDISTE. La palabra era: {juego.get_palabra_secreta()}")


def main():
    # If user requested CLI, or GUI is unavailable, run CLI loop.
    if '--cli' in sys.argv or MainMenuApp is None:
        cli_main()
        return

    # Otherwise start the Tk GUI
    app = MainMenuApp()
    app.mainloop()


if __name__ == "__main__":
    main()

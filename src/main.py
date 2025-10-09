from game import Game


def main():
    """CLI entry point / Punto de entrada para línea de comandos.

    English: Simple loop that prompts for a guess and prints the per-letter
    feedback returned by Game.check_word.

    Español: Bucle sencillo que pide una palabra y muestra la retroalimentación
    por letra que devuelve Game.check_word.
    """
    juego = Game()

    while juego.get_intentos_restantes() > 0:
        entrada = input("Ingrese una palabra: ")

        resultados, is_length_valid, is_known_word, is_winner = juego.check_word(entrada)

        if not is_length_valid:
            print("Palabra incorrecta o de longitud inválida (debe tener 6 letras).\n")
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


if __name__ == "__main__":
    main()

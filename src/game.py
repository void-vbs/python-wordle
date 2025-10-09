from word_list import WordList


class Game:
    """Game logic for the Wordle-like application.

    English: Encapsulates the target word, attempts and the scoring logic.
    The scoring uses a two-pass algorithm to correctly handle repeated letters:
      1) Mark 'green' (verde) for letters in the correct positions.
      2) Count remaining unmatched letters in the target.
      3) Mark 'yellow' (amarillo) for letters present in remaining counts.
      4) Otherwise mark 'red' (rojo).

    Español: Contiene la palabra objetivo, los intentos y la lógica de puntuación.
    La puntuación usa un algoritmo en dos pasadas para manejar correctamente
    letras repetidas: primero marca verdes, luego usa contadores para marcar
    amarillos hasta agotar las ocurrencias reales.

    API summary / Resumen:
      - Game(length=6)              # crea juego con palabras de 6 letras por defecto
      - check_word(input_word) -> (resultados, is_length_valid, is_known, is_winner)
        resultados: list[(letter, estado)] or None when unknown
        is_length_valid: bool
        is_known: bool (is word in dict for the mode)
        is_winner: bool
    """

    def __init__(self, palabra_secreta=None, length: int = 6, intentos=6):
        self.length = length
        self.palabra_secreta = palabra_secreta or WordList.get_random_word(self.length)
        self.intentos = intentos
        self.historial = []

    def check_word(self, input_word: str):
        """Validate and score a guess.

        English: Returns a tuple: (resultados, is_length_valid, is_known, is_winner)

        - resultados: list of (letter, estado) where estado is 'verde'|'amarillo'|'rojo'.
            If the word is not known, resultados is None.
        - is_length_valid: whether the guess has the expected length.
        - is_known: whether the guess is present in the dictionary for the mode.
        - is_winner: True when all letters are 'verde'.
        
        Español: Devuelve una tupla: (resultados, longitud_valida, es_conocida, es_ganador)

        - resultados: lista de (letra, estado) donde estado es 'verde' | 'amarillo' | 'rojo'.
            Si la palabra no es conocida, resultados es None.
        - longitud_valida: indica si la suposición tiene la longitud esperada.
        - es_conocida: indica si la suposición está presente en el diccionario del modo.
        - es_ganador: True cuando todas las letras son 'verde'.
        """
        if not isinstance(input_word, str):
            return None, False, False, False

        word = input_word.strip().lower()

        # length validation using the game's configured length
        # Validación de longitud usando la longitud configurada del juego.
        is_length_valid = WordList.is_correct_length(word, self.length)

        if not is_length_valid:
            return None, False, False, False

        # Known-word check (dictionary depends on length)
        # Verificación de palabra conocida (el diccionario depende de la longitud)
        is_known = WordList.is_known_word(word, self.length)

        # If not known, do not compute hints or consume attempts
        # Si no es conocida, no calcular pistas ni consumir intentos.
        if not is_known:
            return None, True, False, False

        target = self.palabra_secreta
        resultados = [None] * len(target)

        # First pass: greens and build remaining counts for unmatched target letters
        # Primer paso: identificar verdes y construir el conteo restante de letras objetivo no coincidentes.
        remaining = {}
        for i, ch in enumerate(target):
            if word[i] == ch:
                resultados[i] = (word[i], 'verde')
            else:
                remaining[ch] = remaining.get(ch, 0) + 1

        # Second pass: yellows (if remaining count available) or red
        # Segundo paso: amarillos (si hay conteo restante disponible) o rojo.
        for i, ch in enumerate(word):
            if resultados[i] is not None:
                continue
            if remaining.get(ch, 0) > 0:
                resultados[i] = (ch, 'amarillo')
                remaining[ch] -= 1
            else:
                resultados[i] = (ch, 'rojo')

        self.historial.append(resultados)

        is_winner = all(estado == 'verde' for _, estado in resultados)

        # Consume an attempt for a valid known guess
        # Consume un intento para una suposición válida y conocida.
        self.intentos -= 1

        return resultados, True, True, is_winner

    def get_historial(self):
        """Return the history of past guesses.

        Español: Devuelve la lista de intentos previos con sus estados.
        """
        return self.historial

    def get_intentos_restantes(self):
        """Return remaining attempts.

        Español: Devuelve el número de intentos que quedan.
        """
        return self.intentos

    def get_palabra_secreta(self):
        """Return the secret target word.

        Español: Devuelve la palabra objetivo actual.
        """
        return self.palabra_secreta
from word_list import WordList

class Game:
    def __init__(self, palabra_secreta=None, intentos=6):
        self.palabra_secreta = palabra_secreta or WordList.get_random_word()
        self.intentos = intentos
        self.historial = []

    def check_word(self, input_word: str):
    
        if not isinstance(input_word, str):
            return None, False, False, False

        word = input_word.strip().lower()

        is_length_valid = WordList.is_correct_length(word)
        is_known = False

        if not is_length_valid:
            return None, False, False, False

        is_known = WordList.is_known_word(word)

        resultados = []
        target = self.palabra_secreta

        for i in range(len(target)):
            letter_input = word[i]
            letter_target = target[i]

            if letter_input == letter_target:
                estado = "verde"
            elif letter_input in target:
                estado = "amarillo"
            else:
                estado = "rojo"

            resultados.append((letter_input, estado))

        self.historial.append(resultados)

        is_winner = all(estado == "verde" for _, estado in resultados)

        self.intentos -= 1

        return resultados, True, is_known, is_winner

    def get_historial(self):
        return self.historial

    def get_intentos_restantes(self):
        return self.intentos

    def get_palabra_secreta(self):
        return self.palabra_secreta
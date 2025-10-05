from word_list import WordList

class Game:
    def __init__(self, palabraSecreta, intentos):
        self.palabraSecreta = palabraSecreta
        self.intentos = intentos
        self.historial = []
    
    def check_word(self, input_word):
        self.input_word = input_word
        if WordList.is_valid_word(input_word):
            return True
        
if __name__ == "__main__":
    palabra_secreta = WordList.get_random_word()
    juego = Game(palabra_secreta, intentos=6)

    while juego.intentos > 0:
        entrada = input("Ingrese una palabra: ")
        juego.check_word(entrada)
                      
            
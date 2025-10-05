import random

words = [
    "buffer"#, "syntax", "binary", "thread", "kernel",
    #"module", "object", "script", "static", "editor",
    #"client", "server", "daemon", "socket", "layout",
    #"update", "branch", "repeat", "device"
]

class WordList:

    @classmethod
    def get_random_word(cls):
        return random.choice(words)
    
    @classmethod
    def is_valid_word(cls, word):
        if word in words:
            print("Palabra correcta!")
            True
        elif len(word) > 6 or len(word) < 6:
            print("La palabra debe tener 6 letras")
        else:
            print("Palabra incorrecta")
            
        
    



        
        


        
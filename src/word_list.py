import random
import os

# Directory where this module and the words files live.
# Directorio donde se encuentran este módulo y los archivos de palabras.
MODULE_DIR = os.path.dirname(__file__)

# In-memory cache mapping word length -> list of words.
# Caché en memoria que mapea longitud de palabra -> lista de palabras.
_words_by_length = {}


def _load_words_file(length: int):
    """Load a words_N.txt file for the requested length.

    English: Open and read 'words_{length}.txt' next to this module. Returns
    a list of lower-cased, deduplicated words or None if the file does not exist.

    Español: Abre y lee 'words_{length}.txt' al lado de este módulo. Devuelve
    una lista de palabras en minúsculas y sin duplicados, o None si el archivo
    no existe.
    """
    path = os.path.join(MODULE_DIR, f'words_{length}.txt')
    if not os.path.exists(path):
        return None
    with open(path, 'r', encoding='utf-8') as f:
        words = [w.strip().lower() for w in f if w.strip()]
    # dedupe while preserving order
    return list(dict.fromkeys(words))


class WordList:
    """Utility methods to work with per-length word lists.

    - English: Provides lazy loading of word files (words_5.txt, words_6.txt, etc.)
      and a small fallback list when files are missing. Public API is length-aware:
        - get_random_word(length)
        - is_correct_length(word, length)
        - is_known_word(word, length)

    - Español: Provee carga perezosa de archivos de palabras (words_5.txt,
      words_6.txt, etc.) y una lista de respaldo pequeña cuando faltan archivos.
      La API pública está basada en la longitud:
        - get_random_word(length)
        - is_correct_length(word, length)
        - is_known_word(word, length)
    """

    @classmethod
    def _ensure_loaded(cls, length: int):
        """Ensure the words list for `length` is loaded into the cache.

        English: If a words_N.txt file exists it will be loaded; otherwise a
        small fallback list is used so the game remains functional.

        Español: Si existe el archivo words_N.txt se cargará; de lo contrario
        se usa una lista de respaldo pequeña para que el juego funcione.
        """
        if length in _words_by_length:
            return
        loaded = _load_words_file(length)
        if loaded is not None and len(loaded) > 0:
            _words_by_length[length] = loaded
            return

        # Fallback small lists if files missing (examples only).
        # Listas de respaldo pequeñas si faltan los archivos (ejemplos).
        if length == 5:
            _words_by_length[length] = ['apple', 'train', 'coche', 'gatoo', 'perro']
        elif length == 6:
            _words_by_length[length] = ['buffer', 'perrer']
        elif length == 7:
            _words_by_length[length] = ['puzzled', 'running', 'esperar']
        else:
            _words_by_length[length] = []

    @classmethod
    def get_random_word(cls, length: int):
        """Return a random word of the requested length.

        English: Raises ValueError if there are no words available for the
        requested length.

        Español: Lanza ValueError si no hay palabras disponibles para la
        longitud solicitada.
        """
        cls._ensure_loaded(length)
        words = _words_by_length.get(length, [])
        if not words:
            raise ValueError(f'No words available for length {length}')
        return random.choice(words)

    @classmethod
    def is_correct_length(cls, word: str, length: int):
        """Return True when the provided word has the expected length.

        English: Validates that `word` is a string and its length
        matches the requested `length`.
        Español: Valida que word sea una cadena de texto y que su longitud coincida con la length solicitada.
        """
        return isinstance(word, str) and len(word) == length

    @classmethod
    def is_known_word(cls, word: str, length: int):
        """Return True when the provided word is in the known words list.

        English: Ensures the list for the requested length is loaded first.
        Español: Se asegura de cargar la lista para la longitud solicitada.
        """
        cls._ensure_loaded(length)
        return word in _words_by_length.get(length, [])



        
        








# Wordle (Python)

Languages available: English and Spanish

---

## English

A modern, small Wordle-like implementation in Python. This repository contains a command-line interface and a Tkinter-based GUI. Comments and documentation inside the code are bilingual (English / Spanish).

High-level overview
- Purpose: A Wordle-inspired game for learning and experimentation with UI and simple game logic.
- Interfaces: CLI (terminal) and GUI (Tkinter).
- Word lists: Separate files per length (e.g., `words_5.txt`, `words_7.txt`) placed in `src/`.

Repository structure
- `src/`
  - `main.py` — central entry point. Launches GUI by default; `--cli` runs the terminal version.
  - `ui.py` — Tkinter GUI. Contains `MainMenuApp`, `WordleGameFrame`, and `RulesFrame`.
  - `game.py` — Core game logic. Contains `Game` class: secret word, scoring algorithm, attempts tracking.
  - `word_list.py` — Word loading and helpers. Loads per-length word files and provides helper methods to check membership and random selection.
  - `words_5.txt`, `words_7.txt` — example small wordlists.
  - `rules.txt` — editable rules shown by the UI.

Key algorithms & design choices
- Scoring (Wordle semantics): Two-pass algorithm.
  1. First pass marks green letters (correct position). It builds a counter of remaining letters in the secret word excluding greens.
  2. Second pass marks yellows only if the guessed letter exists in the remaining counter (decrementing counts).
  This ensures correct handling of repeated letters (e.g., guessing `perrer` vs secret `buffer`).

- UI: Tkinter-based, single-active-frame pattern.
  - The application keeps exactly one active child frame in the main container (`self.current_frame`) to avoid stacked/overlapping widgets.
  - Each view (menu, mode selection, game, rules) replaces the active frame.
  - The game grid uses per-cell `tk.Entry` widgets with validation allowing only a single letter and navigation handlers.

Running the project
- GUI (default):
  cd src
  python main.py

- CLI:
  cd src
  python main.py --cli

Development notes
- Python 3.x required. Uses only standard library modules (tkinter).
- To add more words, place a file named `words_N.txt` in `src/` where `N` is the word length.

License & credits
- Simple personal project. No external wordlist provided beyond small example files.

---

## Español

Idiomas disponibles: Inglés y Español (los comentarios en el código y este README están en ambos idiomas)

Resumen
- Propósito: Implementación inspirada en Wordle para aprender y experimentar con UI y lógica de juego.
- Interfaces: Interfaz de línea de comandos (CLI) y GUI con Tkinter.
- Listas de palabras: Archivos separados por longitud (`words_5.txt`, `words_7.txt`) dentro de `src/`.

Estructura del repositorio
- `src/`
  - `main.py` — punto de entrada central. Lanza la GUI por defecto; `--cli` ejecuta la versión de terminal.
  - `ui.py` — GUI en Tkinter. Contiene `MainMenuApp`, `WordleGameFrame` y `RulesFrame`.
  - `game.py` — Lógica del juego. Contiene la clase `Game`: palabra secreta, algoritmo de puntuación, control de intentos.
  - `word_list.py` — Carga de palabras y utilidades. Carga ficheros de palabras por longitud y ofrece métodos para comprobaciones y selección aleatoria.
  - `words_5.txt`, `words_7.txt` — pequeños ejemplos de listas de palabras.
  - `rules.txt` — reglas editables mostradas por la UI.

Algoritmos y decisiones clave
- Puntuación (semántica Wordle): Algoritmo en dos pases.
  1. Primer pase marca verdes (posición correcta) y construye un contador de las letras restantes en la palabra secreta excluyendo verdes.
  2. Segundo pase marca amarillos sólo si la letra adivinada existe en el contador restante (decrementando contadores).
  Esto garantiza el manejo correcto de letras repetidas (p.ej., adivinar `perrer` contra secreto `buffer`).

- UI: Basada en Tkinter, patrón de un solo frame activo.
  - La aplicación mantiene exactamente un frame hijo activo en el contenedor principal (`self.current_frame`) para evitar widgets superpuestos.
  - Cada vista (menú, selección de modo, juego, reglas) reemplaza el frame activo.
  - La cuadrícula del juego usa widgets `tk.Entry` por celda con validación para aceptar sólo una letra y manejadores de navegación.

Ejecución
- GUI (por defecto):
  cd src
  python main.py

- CLI:
  cd src
  python main.py --cli

Notas de desarrollo
- Requiere Python 3.x. Sólo usa la librería estándar (tkinter).
- Para añadir más palabras, coloca un archivo llamado `words_N.txt` en `src/` donde `N` es la longitud deseada.

Licencia y créditos
- Proyecto personal sencillo. No se proporcionan grandes diccionarios externos más allá de los ejemplos incluidos.

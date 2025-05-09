# pip install keyboard

import keyboard
from difflib import SequenceMatcher
import time
braille_alphabet = {
    'A': [{'D'}],
    'B': [{'D', 'W'}],
    'C': [{'D', 'Q'}],
    'D': [{'D', 'Q', 'K'}],
    'E': [{'D', 'K'}],
    'F': [{'D', 'W', 'Q'}],
    'G': [{'D', 'W', 'Q', 'K'}],
    'H': [{'D', 'W', 'K'}],
    'I': [{'W', 'Q'}],
    'J': [{'W', 'Q', 'K'}],
    'K': [{'D', 'O'}],
    'L': [{'D', 'W', 'O'}],
    'M': [{'D', 'Q', 'O'}],
    'N': [{'D', 'Q', 'K', 'O'}],
    'O': [{'D', 'K', 'O'}],
    'P': [{'D', 'W', 'Q', 'O'}],
    'Q': [{'D', 'W', 'Q', 'K', 'O'}],
    'R': [{'D', 'W', 'K', 'O'}],
    'S': [{'W', 'Q', 'O'}],
    'T': [{'W', 'Q', 'K', 'O'}],
    'U': [{'D', 'O', 'P'}],
    'V': [{'D', 'W', 'O', 'P'}],
    'W': [{'W', 'Q', 'K', 'P'}],
    'X': [{'D', 'Q', 'O', 'P'}],
    'Y': [{'D', 'Q', 'K', 'O', 'P'}],
    'Z': [{'D', 'K', 'O', 'P'}]
}                                                # QWERTY Braille dot mapping for A-Z


def load_braille_dictionary(file_path, braille_map):
    braille_dict = {}
    with open(file_path, 'r') as f:
        for line in f:
            word = line.strip().upper()
            if not word.isalpha():
                continue
            braille_sequence = []
            for char in word:
                if char in braille_map:
                    braille_sequence.extend(braille_map[char])
            braille_dict[word] = braille_sequence
    return braille_dict


def normalize_sequence(seq):
    return [tuple(sorted(ch)) for ch in seq]


def similarity(seq1, seq2):
    seq1_norm = normalize_sequence(seq1)
    seq2_norm = normalize_sequence(seq2)
    return SequenceMatcher(None, seq1_norm, seq2_norm).ratio()


def suggest_word(input_sequence, dictionary):
    best_match = None
    best_score = -1
    for word, braille_seq in dictionary.items():
        score = similarity(input_sequence, braille_seq)
        if score > best_score:
            best_score = score
            best_match = word
    return best_match


def get_braille_input():
    print("\nBraille typing mode activated (QWERTY keys: D W Q K O P)")
    print("→ Press key combinations for a character, then press [Space]")
    print("→ Press [Enter] when your word is complete\n")

    current_char = set()
    word_sequence = []

    while True:
        event = keyboard.read_event()
        if event.event_type == keyboard.KEY_DOWN:
            key = event.name.upper()

            if key in {'D', 'W', 'Q', 'K', 'O', 'P'}:
                current_char.add(key)

            elif key == 'SPACE':
                if current_char:
                    word_sequence.append(current_char.copy())
                    current_char.clear()
                    print("✔️ Braille char recorded.")

            elif key == 'ENTER':
                if current_char:
                    word_sequence.append(current_char.copy())
                print("✅ Word entry complete.")
                break

            elif key == 'BACKSPACE':
                if word_sequence:
                    removed = word_sequence.pop()
                    print(f"❌ Removed: {removed}")

            elif key == 'ESC':
                print("🚪 Exiting...")
                exit()

    return word_sequence

braille_dict = load_braille_dictionary('braille_words.txt', braille_alphabet) #Loading the Braille word

while True:
    print("\nPress QWERTY keys for Braille input. Press ESC to quit.")
    user_input = get_braille_input()
    suggestion = suggest_word(user_input, braille_dict)
    print("🔍 Suggested word:", suggestion)
    print("-" * 40)
    time.sleep(1)

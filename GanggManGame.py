




import random
import time

def display_hangman(lives):
    stages = [
        """
         +---+
         |   |
         O   |
        /|\\  |
        / \\  |
             |
        =========
        """,
        """
         +---+
         |   |
         O   |
        /|\\  |
        /     |
             |
        =========
        """,
        """
         +---+
         |   |
         O   |
        /|\\  |
             |
             |
        =========
        """,
        """
         +---+
         |   |
         O   |
        /|    |
             |
             |
        =========
        """,
        """
         +---+
         |   |
         O   |
         |   |
             |
             |
        =========
        """,
        """
         +---+
         |   |
         O   |
             |
             |
             |
        =========
        """,
        """
         +---+
         |   |
             |
             |
             |
             |
        =========
        """
    ]
    return stages[lives]

def hangman():
    words = ["apple", "mango", "banana", "orange", "grapes"]
    chosen_word = random.choice(words)
    display_word = ['_' for _ in chosen_word]
    guessed_letters = []
    lives = 6

    print("🎮 Welcome to Hangman! Guess the word letter by letter.")
    print("You have", lives, "lives. Good Luck!")
    time.sleep(1)
    print(display_hangman(lives))
    print("Word:", " ".join(display_word))
    
    while lives > 0 and '_' in display_word:
        guess = input("Enter a letter: ").lower()
        
        if not guess.isalpha() or len(guess) != 1:
            print("❌ Invalid input! Please enter a single letter.")
            continue
        
        if guess in guessed_letters:
            print("⚠️ You already guessed that letter. Try another one!")
            continue
        
        guessed_letters.append(guess)
        
        if guess in chosen_word:
            for i in range(len(chosen_word)):
                if chosen_word[i] == guess:
                    display_word[i] = guess
            print("✅ Correct! Keep going!")
        else:
            lives -= 1
            print("❌ Wrong guess! You lost a life.")
        
        time.sleep(1)
        print(display_hangman(lives))
        print("Word:", " ".join(display_word))
        print("Lives Left:", lives)
        print("Guessed Letters:", ", ".join(guessed_letters) if guessed_letters else "None")
        print()
        
    if '_' not in display_word:
        print("🎉 Congratulations! You Win! The word was:", chosen_word.upper())
    else:
        print("💀 Game Over! You Lost! The word was:", chosen_word.upper())

if __name__ == "__main__":
    hangman()


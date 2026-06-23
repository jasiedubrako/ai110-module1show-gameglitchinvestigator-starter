# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

- [ ] Describe the game's purpose.
   
   A number guessing game where the player tries to guess a randomly generated secret number within a limited number of attempts. The difficulty setting controls the number range and attempt limit, and the player earns points for guessing correctly — with fewer points the more attempts they use.
- [ ] Detail which bugs you found.

   1. Hints were backwards — "Go Higher" showed when the guess was too high, and vice versa.

   2. The secret number ignored the selected difficulty range (e.g. Easy mode still generated numbers up to 100).

   3. Attempts started at 1 instead of 0 before any guess was made.

   4. Pressing Enter did not submit a guess despite the UI suggesting it would.

   5. "New Game" only reset attempts — score, history, and status carried over from the previous game.

   6. Switching difficulty mid-game did not reset the game state.

   7. The difficulty curve was illogical — Hard had a smaller range (1–50) than Normal (1–100).

- [ ] Explain what fixes you applied.

   1. Corrected the comparison in check_guess so "Too High" returns "Go LOWER!" and "Too Low" returns "Go HIGHER!"

   2. Refactored all game logic (check_guess, parse_guess, get_range_for_difficulty, update_score) out of app.py into logic_utils.py.

   3. Fixed difficulty ranges to Easy=1–20, Normal=1–50, Hard=1–100.

   4. Wrapped the guess input in a st.form so pressing Enter submits the guess.

   5. Fixed "New Game" to reset all session state: secret, attempts, score, status, and history.

   6. Added a difficulty-change check that resets the full game state when a new difficulty is selected.

   7. Reset attempt counter initial value from 1 to 0.

## 📸 Demo Walkthrough

Describe your fixed game in numbered steps so a reader can follow along without watching a video:

1. Game starts on 'Normal' (Default); User enters a guess of 20 (and clicks the 'Submit Guess' button)
2. Game returns "Go Lower"
3. User enters a guess of 2 (and presses the 'Enter' key)
4. Game returns "Go Higher"
5. Score updates correctly after each guess (ie. Always a flat -5 penalty. No odd/even weirdness here.)
6. Game ends after the correct guess and resets game when 'New Game' button is pressed.
7. Game ends after attempts are used up and also resets when 'New Game' button is pressed.
8. User selects different difficulty level in the midst of a current game.
9. Game detects change in game setting and resets game with parameters that align with current difficulty level selected.

**Screenshot** *(optional)*: <!-- Insert a screenshot of your fixed, winning game here -->

## 🧪 Test Results

```
# Paste your pytest output here, e.g.:
# pytest tests/
# ========================= X passed in 0.XXs =========================
```

pytest tests/test_game_logic.py 
========================================================================================== test session starts ==========================================================================================
platform win32 -- Python 3.12.6, pytest-8.3.5, pluggy-1.6.0
rootdir: C:\Users\ja2597\Desktop\shared\princeton\next_steps\Learnings_tutorials_projects\codePath\AI_110\ai110-module1show-gameglitchinvestigator-starter
plugins: mock-3.14.1
collected 29 items                                                                                                                                                                                       

tests\test_game_logic.py .............................                                                                                                                                             [100%]

========================================================================================== 29 passed in 0.08s ===========================================================================================

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]

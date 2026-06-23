# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
When I first ran the game, the main interface loaded, but several parts of the game state did not match the rules shown in the settings pane.
Some bugs were visible from the player interface, while others became clearer by checking the Developer Debug Info.

- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").
  Bugs/Issues Observed
  1. The displayed number range did not update based on difficulty.
    The settings pane showed different ranges for Easy, Normal and Hard mode, but the main game page always displayed "Guess a number between 1 and 100."
    I expcted the main game instructions to update based on the selected difficulty.
  
  2. Easy mode generated a secret number outside the Easy range.
    According to the settings pane, Easy mode should use range of 1-20. However, the Developer Debug Info showed 'Secret=88', which is outside that range.
    I expected the secret number to always stay within the selected difficulty's range.

  3. Pressing Enter did not apply the guess. 
    After typing a guess, the interface displayed text saying "Press Enter to apply," but apressing Enter did not submit or apply the guess as expected. I expected Enter to behave the same way as submitting the guess.
  
  4. Attempts started at 1 before the game was played. 
    In the Developer Info, Attempts=1 appeared on startup even though I had not made any guesses yet. I expected attempts to start at 0.

  5. Hints were backwards.
    When I guessed a number higher than the secret number, the game displayed "Go Higher," even though the correct hint should have been "Go Lower." The opposite also appeared to happen when guessing below the secret.
    This suggests the hint logic may be comparing values incorrectly - that is, erroneously evaluating the secret number relative to the guess, rather than evaluating the guess relative to the secret.

  6. The first guess was not recorded properly.
    The first guess did not update Attempts, Score, or History. These values only started changing after the first attempt had already been made.
    I expected every submitted guess, including the first one, to be counted and recorded.

  7. New Game did not reset the game correctly.
    After winning or running our of attempts, clicking 'New Game' did not properly restart the game. When clicked in the middle of a game, it partially reset attempts, but the score and guess history were still affected by the previous game.
    I expected New Game to reset the secret number, attempts, score, hint, and history. 

  8. Illogical Game Balance/Difficulty Curves: 
    The settings pane listed:
      Easy: Range:1-20, Attempts:6
      Normal: Range:1-100, Attempts:8
      Hard: Range:1-50, Attempts: 5
    This felt inconsistent because it makes sense for Hard mode to have the largest range and/or fewest attempts, while Easy mode should give the player the smallest range and/or more attempts.

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
| Start the game in Easy mode| The game should choose a secret number between 1 and 20 | Debug Info showed Secret = 88, which is outside the Easy range | Developer Debug Info: Secret = 88; no console error |
| Start the game and check attempts before making any guess | Attempts should start at 0 | Attempts started at 1 before any guess was made |Developer Debug Info: Attempts = 1; no console error |
| Type a guess, then press Enter | Pressing Enter should submit/apply the guess | Pressing Enter did not apply the guess even though the UI said “Press Enter to apply” | none |
| Guess a number higher than the secret, e.g. secret is 88 and guess is 90 | The game should show a “Go Lower” hint | The game showed “Go Higher” | none |
| Guess a number lower than the secret, e.g. secret is 88 and guess is 50 | The game should show a “Go Higher” hint | The hint appeared to behave backwards or inconsistently | none |
| Submit the first guess of a new game | Attempts, score, and history should update immediately | The first guess was not reflected in Attempts, Score, or History | none |
| Win the game or run out of attempts, then click New Game | The game should fully reset with a new secret, clean history, reset score/attempts, and fresh hint state | New Game did not fully reset the game state | none |
| Click New Game midway through a game after making guesses | Previous guesses and game state should clear completely | Guess history and score still seemed affected by the previous game | none |

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?

  Claude Code, Copilot
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).

  AI suggested to reinitialize all the necessary parameters  that ensure a fresh game start when a new difficulty level was selected; this helped in making sure selecting a new difficulty level even in the middle of a game in another difficulty level leads to the right secret number, attempts etc. 
  I verified this by running the App and checking for that functionality.

- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).
  
  N/A
---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?

  For each bug fix suggested, I decided the bug was fixed by manually running the app and checking to see if it responds as such - especially with those that have to deal with the visual output results.

- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
  One manual test I run was running the app and pressing the 'Enter' key after entering a guess and observing whether that applied/registered the guess. 
  This showed me that my code is now responsive to diverse user inputs, making it more robust.

- Did AI help you design or understand any tests? How?
  Yes; AI helped design the tests by generating diverse pytest cases for the various bugs we identified and fixed; this ensured that, we can test the game logic against lots of inputs at a go and observing the results to determine the robustness and correctness of the code.
---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

  Streamlit Reruns: This reflects the property of Streamlit in that it doesn't just update one piece of the page when a user interacts with it; it tears down the whole screen and executes your entire Python script from line 1 to the bottom. Every click, keystroke, or slider adjustment trigeers a complete script rerun.

  Session State: Since reruns completely wipe out standard Python variables on every single execution, you neede a way to preserve data. 'st.session_state' acts like a persistent 'Cloud Save' dictionary that lives outside the execution loop. it remembers things like the current attempts, etc. across those top-to-bottom reruns so the game doesn't instantly forget its own data.
---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
  
  Adding new commits at relevant milestones reached so that the most recent working version of the project can always be returned to in a situation where there may be AI halluncination, entire project rewrite etc.

- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.

  I would identify and point to targetted areas of the code that need attention so as to get the best result from the AI.

  This project made me realize that building with AI can be quick and enjoyable but can also be frustrating and both experiences depend on how the user is to employ the right AI-engineering techniques and lean on the right programming foundations to get the AI to work.

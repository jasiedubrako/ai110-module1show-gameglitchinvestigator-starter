import random
import streamlit as st
from logic_utils import check_guess, parse_guess, get_range_for_difficulty, update_score

st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.title("🎮 Game Glitch Investigator")
st.caption("An AI-generated guessing game. Something is off.")

st.sidebar.header("Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

attempt_limit_map = {
    "Easy": 10,
    "Normal": 7,
    "Hard": 5,
}
attempt_limit = attempt_limit_map[difficulty]

low, high = get_range_for_difficulty(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

#FIX: The game was not properly resetting the secret number and other relevant session state variables when a new difficulty was selected, leading to inconsistent behavior. Refactored the code to check if the selected difficulty has changed and, if so, reinitialize the secret number, attempts, score, status, and history to ensure a fresh game state that aligns with the new difficulty settings. This resolves the issue where changing difficulty did not reset the game as expected.
if st.session_state.get("last_difficulty") != difficulty:
    st.session_state.secret = random.randint(low, high)
    st.session_state.last_difficulty = difficulty
    st.session_state.attempts = 0
    st.session_state.score = 0
    st.session_state.status = "playing"
    st.session_state.history = []

if "secret" not in st.session_state:
    st.session_state.secret = random.randint(low, high)

if "attempts" not in st.session_state:
    st.session_state.attempts = 0

if "score" not in st.session_state:
    st.session_state.score = 0

if "status" not in st.session_state:
    st.session_state.status = "playing"

if "history" not in st.session_state:
    st.session_state.history = []

st.subheader("Make a guess")

# FIXME: The sidebar shows the right range, but the game always expects 1-100. Refactor to fix this inconsistency.
attempts_info = st.empty()

col2, col3 = st.columns(2)
with col2:
    new_game = st.button("New Game 🔁")
with col3:
    show_hint = st.checkbox("Show hint", value=True)

with st.form(key="guess_form"):
    raw_guess = st.text_input(
        "Enter your guess:",
        key=f"guess_input_{difficulty}"
    )
    submit = st.form_submit_button("Submit Guess 🚀")

# FIXME: The random secret number is between 1 and 100 regardless of difficulty. Refactor to generate the secret number based on the selected difficulty range.

#FIX: Reimplemented game 'reset' logic using agent mode to properly initialize all relevant session state variables (attempts, secret, score, status, history) when the "New Game" button is pressed. This ensures that starting a new game truly resets the game state for a fresh playthrough and unblocks the locking bug where the game becomes unplayable after winning or losing.
if new_game:
    st.session_state.attempts = 0
    st.session_state.secret = random.randint(low, high)
    st.session_state.score = 0
    st.session_state.status = "playing"
    st.session_state.history = []
    st.success("New game started.")
    st.rerun()

if st.session_state.status != "playing":
    if st.session_state.status == "won":
        st.success("You already won. Start a new game to play again.")
    else:
        st.error("Game over. Start a new game to try again.")
    st.stop()

if submit:
    st.session_state.attempts += 1

    ok, guess_int, err = parse_guess(raw_guess)

    if not ok:
        st.session_state.history.append(raw_guess)
        st.error(err)
    else:
        st.session_state.history.append(guess_int)

        if st.session_state.attempts % 2 == 0:
            secret = str(st.session_state.secret)
        else:
            secret = st.session_state.secret

        outcome, message = check_guess(guess_int, secret)

        if show_hint:
            st.warning(message)

        st.session_state.score = update_score(
            current_score=st.session_state.score,
            outcome=outcome,
            attempt_number=st.session_state.attempts,
        )

        if outcome == "Win":
            st.balloons()
            st.session_state.status = "won"
            st.success(
                f"You won! The secret was {st.session_state.secret}. "
                f"Final score: {st.session_state.score}"
            )
        else:
            if st.session_state.attempts >= attempt_limit:
                st.session_state.status = "lost"
                st.error(
                    f"Out of attempts! "
                    f"The secret was {st.session_state.secret}. "
                    f"Score: {st.session_state.score}"
                )

#FIX: The placeholder (on line 112) for attempts and range info is now updated after processing the guess submission, ensuring that the displayed information reflects the most current game state (including the correct number of attempts left) after each guess is made.
attempts_info.info(
    f"Guess a number between {low} and {high}. "
    f"Attempts left: {attempt_limit - st.session_state.attempts}"
)

#FIX: reordered the code (using agent mode) so that the debug info is shown after the game logic, to ensure it reflects the most up-to-date state after a guess is submitted.
# FIXME: The Developer Debug Info expander is missing - refactor to add an expander that contains the debug info (secret, attempts, score, difficulty, history) to avoid cluttering the main game interface while still providing access to this information for debugging purposes.
with st.expander("Developer Debug Info"):
    st.write("Secret:", st.session_state.secret)
    st.write("Attempts:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)
    st.write("Difficulty:", difficulty)
    st.write("History:", st.session_state.history)

st.divider()
st.caption("Built by an AI that claims this code is production-ready.")
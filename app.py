"""Glitchy Guesser - a Streamlit number guessing game.

Game logic lives in game_logic.py (and is unit tested in test_game_logic.py).
This file is only the Streamlit UI + session-state wiring.

Bugs fixed from the original AI-generated version (see inline `# FIX:` notes):
  1. Hint direction was reversed (too-high told you to go higher). [in game_logic.py]
  2. Secret was cast to a string on even attempts, corrupting comparisons. [in game_logic.py]
  3. "New Game" left status/score/history stale, so old win/lose messages
     persisted and the game stayed stopped.
  4. "New Game" reset the range to a hard-coded 1-100 instead of the
     selected difficulty's range, and used an inconsistent attempt count.
  5. The guess text box did not clear when starting a new game.
  6. The "Guess a number between 1 and 100" banner was hard-coded and lied
     for the Easy/Hard ranges.
"""

import random

import streamlit as st

from game_logic import (
    get_range_for_difficulty,
    parse_guess,
    check_guess,
    update_score,
)

ATTEMPT_LIMITS = {"Easy": 6, "Normal": 8, "Hard": 5}


def start_new_game(low: int, high: int, difficulty: str) -> None:
    """Reset every piece of game state for a fresh round.

    FIX (#3, #4, #5): the original New Game handler only reset `secret` and
    `attempts`. It left `status`, `score` and `history` behind, so leftover
    "You already won / Game over" messages stuck around and `st.stop()` kept
    halting the game. It also re-rolled the secret from a hard-coded 1-100.
    Centralising the reset here keeps first-run init and New Game in sync.
    Bumping `input_nonce` forces a brand-new (empty) guess widget.
    """
    st.session_state.secret = random.randint(low, high)
    st.session_state.attempts = 0
    st.session_state.score = 0
    st.session_state.status = "playing"
    st.session_state.history = []
    st.session_state.active_difficulty = difficulty
    st.session_state.input_nonce = st.session_state.get("input_nonce", 0) + 1


# --------------------------------------------------------------------------
# Page setup
# --------------------------------------------------------------------------
st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")
st.title("🎮 Game Glitch Investigator")
st.caption("An AI-generated guessing game - now with the glitches fixed.")

# --------------------------------------------------------------------------
# Sidebar / settings
# --------------------------------------------------------------------------
st.sidebar.header("Settings")
difficulty = st.sidebar.selectbox("Difficulty", ["Easy", "Normal", "Hard"], index=1)
attempt_limit = ATTEMPT_LIMITS[difficulty]
low, high = get_range_for_difficulty(difficulty)
st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

# --------------------------------------------------------------------------
# Session state (initialise once on first run)
# --------------------------------------------------------------------------
if "status" not in st.session_state:
    start_new_game(low, high, difficulty)

# FIX: regenerate the secret when the difficulty changes. Otherwise the old
# secret could fall outside the newly selected range (e.g. a secret of 45 from
# Normal while the dropdown now shows Easy 1-20), making the game unwinnable.
elif st.session_state.active_difficulty != difficulty:
    start_new_game(low, high, difficulty)
    st.rerun()

# --------------------------------------------------------------------------
# Main guess panel
# --------------------------------------------------------------------------
st.subheader("Make a guess")

# FIX (#6): use the actual difficulty range instead of a hard-coded "1 and 100".
st.info(
    f"Guess a number between {low} and {high}. "
    f"Attempts left: {attempt_limit - st.session_state.attempts}"
)

with st.expander("Developer Debug Info"):
    st.write("Secret:", st.session_state.secret)
    st.write("Attempts:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)
    st.write("Difficulty:", difficulty)
    st.write("History:", st.session_state.history)

# FIX (#5): the key includes `input_nonce`, which start_new_game() bumps.
# Changing the key makes Streamlit treat this as a fresh widget, so the box
# clears on New Game (popping the old key alone was unreliable).
raw_guess = st.text_input(
    "Enter your guess:",
    key=f"guess_input_{difficulty}_{st.session_state.input_nonce}",
)

col1, col2, col3 = st.columns(3)
with col1:
    submit = st.button("Submit Guess 🚀")
with col2:
    new_game = st.button("New Game 🔁")
with col3:
    show_hint = st.checkbox("Show hint", value=True)

# --------------------------------------------------------------------------
# Button / game-state handling
# --------------------------------------------------------------------------
if new_game:
    start_new_game(low, high, difficulty)
    st.rerun()

# If the previous round already ended, show the result and stop here.
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

        # FIX (#2): compare against the secret as-is. The original turned it
        # into a string on even attempts, which broke the comparison.
        outcome, message = check_guess(guess_int, st.session_state.secret)

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
        elif st.session_state.attempts >= attempt_limit:
            st.session_state.status = "lost"
            st.error(
                f"Out of attempts! The secret was {st.session_state.secret}. "
                f"Score: {st.session_state.score}"
            )

st.divider()
st.caption("Built by an AI that claims this code is production-ready.")

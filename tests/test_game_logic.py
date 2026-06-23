import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from logic_utils import check_guess, get_range_for_difficulty, parse_guess, update_score


# ── check_guess ────────────────────────────────────────────────────────────────
# Bug fixed: hints were backwards. guess > secret showed "Go Higher" and
# guess < secret showed "Go Lower". The comparison evaluated secret vs. guess
# instead of guess vs. secret.

def test_winning_guess():
    outcome, _ = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_high_outcome():
    outcome, _ = check_guess(60, 50)
    assert outcome == "Too High"

def test_guess_too_low_outcome():
    outcome, _ = check_guess(40, 50)
    assert outcome == "Too Low"

def test_too_high_message_says_lower():
    # Regression: the buggy version returned "Go HIGHER!" when guess > secret.
    _, message = check_guess(60, 50)
    assert "LOWER" in message

def test_too_low_message_says_higher():
    # Regression: the buggy version returned "Go LOWER!" when guess < secret.
    _, message = check_guess(40, 50)
    assert "HIGHER" in message

def test_guess_one_above_secret_is_too_high():
    outcome, _ = check_guess(51, 50)
    assert outcome == "Too High"

def test_guess_one_below_secret_is_too_low():
    outcome, _ = check_guess(49, 50)
    assert outcome == "Too Low"

def test_winning_message_is_correct():
    _, message = check_guess(7, 7)
    assert "Correct" in message


# ── get_range_for_difficulty ───────────────────────────────────────────────────
# Bug fixed: Normal and Hard ranges were swapped. Normal returned 1–100 and
# Hard returned 1–50, so Hard was actually easier than Normal.

def test_easy_range():
    low, high = get_range_for_difficulty("Easy")
    assert low == 1
    assert high == 20

def test_normal_range():
    low, high = get_range_for_difficulty("Normal")
    assert low == 1
    assert high == 50

def test_hard_range():
    low, high = get_range_for_difficulty("Hard")
    assert low == 1
    assert high == 100

def test_hard_range_larger_than_normal():
    # Regression: in the buggy version hard_high (50) < normal_high (100).
    _, normal_high = get_range_for_difficulty("Normal")
    _, hard_high = get_range_for_difficulty("Hard")
    assert hard_high > normal_high

def test_hard_range_larger_than_easy():
    _, easy_high = get_range_for_difficulty("Easy")
    _, hard_high = get_range_for_difficulty("Hard")
    assert hard_high > easy_high

def test_normal_range_larger_than_easy():
    _, easy_high = get_range_for_difficulty("Easy")
    _, normal_high = get_range_for_difficulty("Normal")
    assert normal_high > easy_high

def test_unknown_difficulty_fallback():
    low, high = get_range_for_difficulty("Expert")
    assert low == 1
    assert high == 50


# ── parse_guess ────────────────────────────────────────────────────────────────

def test_parse_guess_valid_integer():
    ok, value, err = parse_guess("42")
    assert ok is True
    assert value == 42
    assert err is None

def test_parse_guess_none_returns_error():
    ok, value, err = parse_guess(None)
    assert ok is False
    assert value is None
    assert err is not None

def test_parse_guess_empty_string_returns_error():
    ok, value, err = parse_guess("")
    assert ok is False
    assert value is None
    assert err is not None

def test_parse_guess_non_numeric_returns_error():
    ok, value, err = parse_guess("abc")
    assert ok is False
    assert value is None
    assert err is not None

def test_parse_guess_decimal_truncates_to_int():
    ok, value, err = parse_guess("7.9")
    assert ok is True
    assert value == 7
    assert err is None

def test_parse_guess_negative_number():
    ok, value, err = parse_guess("-3")
    assert ok is True
    assert value == -3
    assert err is None


# ── update_score ───────────────────────────────────────────────────────────────

def test_update_score_win_first_attempt_gives_100():
    assert update_score(0, "Win", 1) == 100

def test_update_score_win_attempt_5_gives_60():
    # 100 - 10*(5-1) = 60
    assert update_score(0, "Win", 5) == 60

def test_update_score_win_attempt_10_floors_at_10():
    # 100 - 10*(10-1) = 10  (hits the floor exactly)
    assert update_score(0, "Win", 10) == 10

def test_update_score_win_late_attempt_never_goes_below_10():
    # 100 - 10*(15-1) = -40, floored to 10
    assert update_score(0, "Win", 15) == 10

def test_update_score_too_high_deducts_5():
    assert update_score(100, "Too High", 3) == 95

def test_update_score_too_low_deducts_5():
    assert update_score(100, "Too Low", 3) == 95

def test_update_score_unknown_outcome_unchanged():
    assert update_score(50, "Draw", 1) == 50

def test_update_score_accumulates_across_calls():
    score = update_score(0, "Too High", 1)   # 0 - 5 = -5
    score = update_score(score, "Too Low", 2) # -5 - 5 = -10
    score = update_score(score, "Win", 3)     # -10 + (100 - 20) = 70
    assert score == 70
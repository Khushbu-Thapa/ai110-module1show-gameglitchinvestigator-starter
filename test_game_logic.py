"""Unit tests for the Glitchy Guesser game logic.

Run with:
    pytest test_game_logic.py -v
"""

import pytest

from game_logic import (
    get_range_for_difficulty,
    parse_guess,
    check_guess,
    update_score,
)


# ---------------------------------------------------------------------------
# get_range_for_difficulty
# ---------------------------------------------------------------------------

class TestGetRangeForDifficulty:
    def test_easy(self):
        assert get_range_for_difficulty("Easy") == (1, 20)

    def test_normal(self):
        assert get_range_for_difficulty("Normal") == (1, 50)

    def test_hard(self):
        assert get_range_for_difficulty("Hard") == (1, 100)

    # The range must grow as difficulty increases (wider range = harder).
    def test_ranges_increase_with_difficulty(self):
        easy = get_range_for_difficulty("Easy")[1]
        normal = get_range_for_difficulty("Normal")[1]
        hard = get_range_for_difficulty("Hard")[1]
        assert easy < normal < hard

    # Edge case: unknown difficulty falls back to the default range.
    def test_unknown_falls_back_to_default(self):
        assert get_range_for_difficulty("Impossible") == (1, 100)

    # Edge case: matching is case-sensitive, so "easy" is not "Easy".
    def test_is_case_sensitive(self):
        assert get_range_for_difficulty("easy") == (1, 100)

    # Edge case: empty string also falls back.
    def test_empty_string(self):
        assert get_range_for_difficulty("") == (1, 100)


# ---------------------------------------------------------------------------
# parse_guess
# ---------------------------------------------------------------------------

class TestParseGuess:
    def test_valid_integer(self):
        ok, value, err = parse_guess("42")
        assert ok is True
        assert value == 42
        assert err is None

    # Edge case: a decimal string is truncated (not rounded) toward zero.
    def test_float_string_is_truncated(self):
        ok, value, err = parse_guess("42.9")
        assert ok is True
        assert value == 42
        assert err is None

    def test_negative_number(self):
        ok, value, err = parse_guess("-5")
        assert ok is True
        assert value == -5

    # Edge case: surrounding whitespace is tolerated by int().
    def test_whitespace_padded_number(self):
        ok, value, err = parse_guess("  7  ")
        assert ok is True
        assert value == 7

    # Edge case: None input.
    def test_none_input(self):
        ok, value, err = parse_guess(None)
        assert ok is False
        assert value is None
        assert err == "Enter a guess."

    # Edge case: empty string.
    def test_empty_string(self):
        ok, value, err = parse_guess("")
        assert ok is False
        assert value is None
        assert err == "Enter a guess."

    # Edge case: non-numeric text.
    def test_non_numeric_text(self):
        ok, value, err = parse_guess("abc")
        assert ok is False
        assert value is None
        assert err == "That is not a number."

    # Edge case: a lone decimal point goes through the float() branch and fails.
    def test_lone_dot(self):
        ok, value, err = parse_guess(".")
        assert ok is False
        assert err == "That is not a number."

    # Edge case: whitespace-only string is not empty but is not a number.
    def test_whitespace_only(self):
        ok, value, err = parse_guess("   ")
        assert ok is False
        assert err == "That is not a number."

    # Edge case: "1e3" has no ".", so it takes the int() branch and is
    # rejected. Only strings containing a "." take the float() branch.
    def test_scientific_notation_without_dot_is_rejected(self):
        ok, value, err = parse_guess("1e3")
        assert ok is False
        assert err == "That is not a number."

    # With a "." it goes through float() and scientific notation works.
    def test_scientific_notation_with_dot(self):
        ok, value, err = parse_guess("1.0e3")
        assert ok is True
        assert value == 1000

    @pytest.mark.parametrize(
        "raw,expected",
        [
            ("0", 0),
            ("100", 100),
            ("000123", 123),
        ],
    )
    def test_various_valid(self, raw, expected):
        ok, value, _ = parse_guess(raw)
        assert ok is True
        assert value == expected


# ---------------------------------------------------------------------------
# check_guess
# ---------------------------------------------------------------------------

class TestCheckGuess:
    def test_correct_guess(self):
        assert check_guess(50, 50) == ("Win", "🎉 Correct!")

    # Regression test for the swapped-hint bug:
    # a guess ABOVE the secret must tell the player to go LOWER.
    def test_too_high_says_go_lower(self):
        outcome, message = check_guess(80, 50)
        assert outcome == "Too High"
        assert "LOWER" in message

    # Regression test for the swapped-hint bug:
    # a guess BELOW the secret must tell the player to go HIGHER.
    def test_too_low_says_go_higher(self):
        outcome, message = check_guess(20, 50)
        assert outcome == "Too Low"
        assert "HIGHER" in message

    # Specific scenario the user reported: secret 96, guess 92 -> go higher.
    def test_reported_scenario(self):
        outcome, message = check_guess(92, 96)
        assert outcome == "Too Low"
        assert "HIGHER" in message

    # Edge case: off by one on each side.
    def test_off_by_one_high(self):
        assert check_guess(51, 50)[0] == "Too High"

    def test_off_by_one_low(self):
        assert check_guess(49, 50)[0] == "Too Low"

    # Edge case: range boundaries.
    def test_boundary_min(self):
        assert check_guess(1, 1) == ("Win", "🎉 Correct!")

    def test_boundary_max(self):
        assert check_guess(100, 100) == ("Win", "🎉 Correct!")


# ---------------------------------------------------------------------------
# update_score
# ---------------------------------------------------------------------------

class TestUpdateScore:
    # Winning on attempt 1 -> points = 100 - 10*(1+1) = 80.
    def test_win_early_attempt(self):
        assert update_score(0, "Win", 1) == 80

    # Winning later earns fewer points.
    def test_win_later_attempt(self):
        assert update_score(0, "Win", 5) == 40  # 100 - 10*6

    # Edge case: win points are floored at 10, never below.
    def test_win_points_floor(self):
        # attempt 9 -> 100 - 10*10 = 0 -> floored to 10
        assert update_score(0, "Win", 9) == 10

    def test_win_points_floor_large_attempt(self):
        assert update_score(0, "Win", 50) == 10

    # Win adds to an existing score rather than replacing it.
    def test_win_accumulates(self):
        assert update_score(25, "Win", 1) == 105

    # "Too High" on an even attempt adds 5; on an odd attempt subtracts 5.
    def test_too_high_even_attempt(self):
        assert update_score(0, "Too High", 2) == 5

    def test_too_high_odd_attempt(self):
        assert update_score(0, "Too High", 3) == -5

    # "Too Low" always subtracts 5.
    def test_too_low(self):
        assert update_score(10, "Too Low", 1) == 5

    def test_too_low_can_go_negative(self):
        assert update_score(0, "Too Low", 1) == -5

    # Edge case: an unrecognised outcome leaves the score unchanged.
    def test_unknown_outcome_unchanged(self):
        assert update_score(42, "Sideways", 1) == 42


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-v"]))

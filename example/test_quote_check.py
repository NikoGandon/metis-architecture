from quote_check import verify_quote

SOURCE = "Vitamin D   supplementation\nreduced the risk of fractures in older adults."


def test_exact_quote_is_accepted():
    assert verify_quote("reduced the risk of fractures", SOURCE)


def test_whitespace_differences_are_ignored():
    assert verify_quote("supplementation reduced   the risk", SOURCE)


def test_non_breaking_space_is_ignored():
    assert verify_quote("risk of fractures", SOURCE)


def test_altered_word_is_rejected():
    assert not verify_quote("reduced the danger of fractures", SOURCE)


def test_case_change_is_rejected():
    assert not verify_quote("vitamin d supplementation", SOURCE)


def test_reordered_words_are_rejected():
    assert not verify_quote("fractures of risk the", SOURCE)


def test_empty_quote_is_rejected():
    assert not verify_quote("   ", SOURCE)


def test_quote_longer_than_source_is_rejected():
    assert not verify_quote(SOURCE + " Extra sentence.", SOURCE)

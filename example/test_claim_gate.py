import pytest
from hypothesis import given, strategies as st
from pydantic import ValidationError

from claim_gate import Claim, Status, transition

SOURCE = "Vitamin D supplementation reduced the risk of fractures."


def test_unknown_field_is_refused():
    with pytest.raises(ValidationError):
        Claim(text="a", quote="b", extra_field=1)


def test_claim_is_immutable():
    claim = Claim(text="a", quote="b")
    with pytest.raises(ValidationError):
        claim.status = Status.VERIFIED


def test_verified_when_quote_is_in_source():
    claim = Claim(text="effet", quote="reduced the risk")
    assert transition(claim, Status.VERIFIED, SOURCE).status is Status.VERIFIED


def test_verification_refused_when_quote_is_absent():
    claim = Claim(text="effet", quote="cured every disease")
    with pytest.raises(ValueError):
        transition(claim, Status.VERIFIED, SOURCE)


def test_final_state_cannot_change():
    done = transition(Claim(text="a", quote="b"), Status.REJECTED, SOURCE)
    with pytest.raises(ValueError):
        transition(done, Status.VERIFIED, SOURCE)


@given(st.text(min_size=1), st.text())
def test_never_verified_unless_quote_is_substring_after_space_normalisation(quote, source):
    claim = Claim(text="t", quote=quote)
    try:
        result = transition(claim, Status.VERIFIED, source)
    except ValueError:
        return
    assert " ".join(quote.split()) in " ".join(source.split())
    assert result.status is Status.VERIFIED

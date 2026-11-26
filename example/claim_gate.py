"""Exemple générique : schéma strict, porte de transition d'état et citation vérifiée.

Écrit pour ce dépôt de documentation ; il illustre le principe, pas le code du projet.
"""

from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, ConfigDict, Field

from quote_check import verify_quote


class Status(str, Enum):
    PROPOSED = "proposed"
    VERIFIED = "verified"
    REJECTED = "rejected"


# Transitions autorisées : tout le reste est refusé.
ALLOWED = {
    Status.PROPOSED: {Status.VERIFIED, Status.REJECTED},
    Status.VERIFIED: set(),
    Status.REJECTED: set(),
}


class Claim(BaseModel):
    """Affirmation proposée par un agent : immuable, champs inconnus refusés."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    text: str = Field(min_length=1)
    quote: str = Field(min_length=1)
    status: Status = Status.PROPOSED


def transition(claim: Claim, target: Status, source_text: str) -> Claim:
    """Fait passer une affirmation à un nouvel état si la porte l'autorise.

    Le passage à « verified » exige que la citation figure dans la source :
    la décision est prise ici, en code, jamais par le modèle.
    """
    if target not in ALLOWED[claim.status]:
        raise ValueError(f"transition interdite : {claim.status.value} -> {target.value}")
    if target is Status.VERIFIED and not verify_quote(claim.quote, source_text):
        raise ValueError("citation absente de la source")
    return claim.model_copy(update={"status": target})

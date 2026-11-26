"""Vérification de citation : la citation doit figurer telle quelle dans la source.

Module d'exemple générique, écrit pour ce dépôt de documentation.
"""

from __future__ import annotations


def _normalize_spaces(text: str) -> str:
    """Remplace toute suite d'espaces (y compris insécables, retours à la ligne) par une espace."""
    return " ".join(text.split())


def verify_quote(quote: str, source_text: str) -> bool:
    """Renvoie True si la citation apparaît mot pour mot dans la source.

    Seuls les espaces sont normalisés. La casse, la ponctuation et l'ordre des mots
    doivent correspondre exactement. Une citation vide est refusée.
    """
    normalized_quote = _normalize_spaces(quote)
    if not normalized_quote:
        return False
    return normalized_quote in _normalize_spaces(source_text)

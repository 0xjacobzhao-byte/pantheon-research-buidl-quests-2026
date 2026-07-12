"""Five-model comparison engine.

Deterministic agreement / disagreement analysis across the five providers. It
computes an agreement matrix, confidence spread, shared/unique red flags,
missing-evidence overlap, evidence-coverage spread, and a human-review verdict.

It deliberately NEVER declares a winner — the point is disciplined disagreement
surfacing, not ranking models.
"""

from __future__ import annotations

from typing import Any, Optional

from .llm_schema import (
    FACTOR_KEYS,
    WEAK_EVIDENCE_TIERS,
    EvidenceTier,
    ModelOverlay,
)

MIN_COMPARABLE_PROVIDERS = 2
AGREEMENT_REVIEW_THRESHOLD = 0.7
DISPERSION_REVIEW_THRESHOLD = 0.34

_CONF_SCALE = {"low": 0.2, "medium": 0.6, "high": 1.0}

_COVERAGE_RANK = {
    EvidenceTier.NO_USABLE_EVIDENCE: 0,
    EvidenceTier.SOURCE_LIMITED_BRIEF: 1,
    EvidenceTier.SOURCE_BACKED_BASIC: 2,
    EvidenceTier.SOURCE_BACKED_MODERATE: 3,
    EvidenceTier.SOURCE_BACKED_STRONG: 4,
}


def _usable(overlays: list[ModelOverlay]) -> list[ModelOverlay]:
    return [o for o in overlays if o.is_usable()]


def build_agreement_matrix(overlays: list[ModelOverlay]) -> dict[str, Any]:
    """Per-factor verdict comparison across usable providers."""
    usable = _usable(overlays)
    rows = []
    agreements = 0
    comparisons = 0
    for key in FACTOR_KEYS:
        verdicts: dict[str, str] = {}
        for o in usable:
            f = o.factor(key)
            if f is not None:
                verdicts[o.provider.value] = f.verdict.value
        distinct = sorted(set(verdicts.values()))
        comparable = len(verdicts) >= MIN_COMPARABLE_PROVIDERS
        agree = comparable and len(distinct) == 1
        if comparable:
            comparisons += 1
            if agree:
                agreements += 1
        rows.append({
            "factor": key,
            "verdicts": verdicts,
            "distinct_verdicts": distinct,
            "comparable": comparable,
            "agreement": agree,
        })
    agreement_score = round(agreements / comparisons, 3) if comparisons else None
    return {
        "factors": rows,
        "comparisons": comparisons,
        "agreements": agreements,
        "agreement_score": agreement_score,
    }


def build_disagreement_matrix(matrix: dict[str, Any]) -> list[dict[str, Any]]:
    """Extract the divergent factors from an agreement matrix."""
    divergences = []
    for row in matrix["factors"]:
        if row["comparable"] and not row["agreement"]:
            divergences.append({
                "factor": row["factor"],
                "verdicts": row["verdicts"],
                "distinct_verdicts": row["distinct_verdicts"],
            })
    return divergences


def _mean_confidence(o: ModelOverlay) -> Optional[float]:
    return o.confidence


def confidence_spread(overlays: list[ModelOverlay]) -> Optional[float]:
    confs = [o.confidence for o in _usable(overlays) if o.confidence is not None]
    if len(confs) < 2:
        return None
    return round(max(confs) - min(confs), 3)


_RISK_STOPWORDS = {"risk", "risks", "the", "and", "for", "with", "from", "over"}


def _theme_tokens(flag: str) -> set[str]:
    """Reduce a red-flag phrase to keyword stems so differently-worded mentions
    of the same theme (e.g. 'regulatory' vs 'regulation') cluster together."""
    tokens: set[str] = set()
    for word in flag.lower().replace("/", " ").replace("-", " ").split():
        w = "".join(ch for ch in word if ch.isalpha())
        if len(w) > 4 and w not in _RISK_STOPWORDS:
            tokens.add(w[:6])  # crude stem
    return tokens


def red_flag_analysis(overlays: list[ModelOverlay]) -> dict[str, Any]:
    usable = _usable(overlays)
    per_provider = {o.provider.value: sorted({r.strip() for r in o.red_flags if r.strip()}) for o in usable}
    # Token set per provider (union of all its flag themes).
    prov_tokens = {p: set().union(*[_theme_tokens(f) for f in flags]) if flags else set()
                   for p, flags in per_provider.items()}

    unique: dict[str, list[str]] = {}
    for prov, flags in per_provider.items():
        others = set().union(*[t for p, t in prov_tokens.items() if p != prov]) if len(prov_tokens) > 1 else set()
        u = [f for f in flags if _theme_tokens(f) and _theme_tokens(f).isdisjoint(others)]
        if u:
            unique[prov] = sorted(u)

    # Shared themes: token stems appearing in >1 provider.
    token_counts: dict[str, int] = {}
    for toks in prov_tokens.values():
        for t in toks:
            token_counts[t] = token_counts.get(t, 0) + 1
    shared_themes = sorted(t for t, c in token_counts.items() if c > 1)

    material = len(unique) > 0
    return {
        "per_provider": per_provider,
        "shared_red_flag_themes": shared_themes,
        "unique_red_flags": unique,
        "material_risk_disagreement": material,
    }


def missing_evidence_overlap(overlays: list[ModelOverlay]) -> dict[str, Any]:
    usable = _usable(overlays)
    per_provider = {o.provider.value: sorted({m.lower().strip() for m in o.missing_evidence}) for o in usable}
    sets = [set(v) for v in per_provider.values()]
    shared = sorted(set.intersection(*sets)) if sets else []
    union = sorted(set.union(*sets)) if sets else []
    return {
        "per_provider": per_provider,
        "shared_missing_evidence": shared,
        "all_missing_evidence": union,
    }


def evidence_coverage_spread(overlays: list[ModelOverlay]) -> dict[str, Any]:
    usable = _usable(overlays)
    per_provider = {}
    ranks = []
    weak_providers = []
    for o in usable:
        tier = o.evidence_coverage
        per_provider[o.provider.value] = tier.value if tier else None
        if tier is not None:
            ranks.append(_COVERAGE_RANK[tier])
            if tier in WEAK_EVIDENCE_TIERS:
                weak_providers.append(o.provider.value)
    spread = (max(ranks) - min(ranks)) if len(ranks) >= 2 else None
    return {
        "per_provider": per_provider,
        "coverage_rank_spread": spread,
        "weak_evidence_providers": weak_providers,
    }


def build_comparison(overlays: list[ModelOverlay]) -> dict[str, Any]:
    """Full five-model comparison — no winner is ever declared."""
    usable = _usable(overlays)
    comparable_providers = [o.provider.value for o in usable]

    matrix = build_agreement_matrix(overlays)
    disagreements = build_disagreement_matrix(matrix)
    dispersion = confidence_spread(overlays)
    red_flags = red_flag_analysis(overlays)
    missing = missing_evidence_overlap(overlays)
    coverage = evidence_coverage_spread(overlays)

    reasons: list[str] = []
    if len(comparable_providers) < MIN_COMPARABLE_PROVIDERS:
        reasons.append("insufficient_comparable_providers")
    if matrix["agreement_score"] is None:
        reasons.append("no_comparable_factors")
    elif matrix["agreement_score"] < AGREEMENT_REVIEW_THRESHOLD:
        reasons.append("low_agreement")
    if dispersion is not None and dispersion > DISPERSION_REVIEW_THRESHOLD:
        reasons.append("high_confidence_dispersion")
    if coverage["weak_evidence_providers"]:
        reasons.append("weak_evidence")
    if red_flags["material_risk_disagreement"]:
        reasons.append("material_risk_disagreement")

    human_review_required = bool(reasons)

    return {
        "case_providers": [o.provider.value for o in overlays],
        "comparable_providers": comparable_providers,
        "provider_states": {o.provider.value: o.data_state.value for o in overlays},
        "agreement_matrix": matrix,
        "disagreement_matrix": disagreements,
        "confidence_spread": dispersion,
        "red_flags": red_flags,
        "missing_evidence": missing,
        "evidence_coverage": coverage,
        "human_review_required": human_review_required,
        "human_review_reasons": reasons,
        "winner": None,
        "note": (
            "No winner is declared. This surfaces agreement, disagreement, and "
            "evidence gaps across five independent models over one shared, "
            "hash-committed evidence pack. Cached/offline by default — no live "
            "paid LLM call is made."
        ),
    }

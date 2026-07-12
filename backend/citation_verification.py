"""
citation_verification.py — Citation Verification Engine (hackathon stub).

Real version (post-hackathon): would call the Indian Kanoon API to check any
citation against the full text of Indian case law.

This stub: checks a citation against a small local JSON dataset of ~15 real
citations (see citations_dataset.json). Good enough to demo the actual
decision logic — Verified / Suspicious / Fake — live, without needing
internet access or an API key during the demo.

Matching logic:
  1. Fuzzy-match the case number/citation string against the dataset.
     - No close match at all           -> FAKE (case doesn't appear to exist)
     - Close match on case number found -> case exists, now check the quote:
  2. If the user also supplied a quoted paragraph, fuzzy-match that quote
     against the real snippet stored for that case.
     - Quote matches closely            -> VERIFIED
     - Case exists but quote doesn't match -> SUSPICIOUS (classic hallucination
       pattern: real case number, fabricated paragraph)
  3. If no quote was supplied, a case-number match alone -> VERIFIED
     (nothing to contradict it yet).
"""

import json
import os
import re
from rapidfuzz import fuzz

DATASET_PATH = os.path.join(os.path.dirname(__file__), "citations_dataset.json")

# Two-part case-number matching is required, not a single fuzzy score on the
# raw string. Citation strings like "AIR 2021 SC 4521" are mostly boilerplate
# ("AIR", "SC") that's identical across dozens of unrelated citations from the
# same reporter — a plain fuzzy match on the whole string scores a completely
# different, fabricated case number as ~80% similar to a real one just
# because the words around the numbers match. The actual distinguishing
# signal is the digits (year + case/page number), so we require those to
# match closely on their own, in addition to the overall string match.
TEXT_MATCH_THRESHOLD = 75      # overall string similarity, rapidfuzz score 0-100
NUMERIC_MATCH_THRESHOLD = 85   # similarity of digits only — the real signal
QUOTE_MATCH_THRESHOLD = 65     # slightly looser — paraphrased real quotes still count


def _digits_only(s: str) -> str:
    return "".join(re.findall(r"\d+", s))


def _load_dataset() -> list[dict]:
    with open(DATASET_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def verify_citation(citation_text: str, quoted_paragraph: str = "") -> dict:
    """
    citation_text: e.g. "AIR 2021 SC 4521" or "State of Gujarat v. XYZ, 2019"
    quoted_paragraph: optional — the specific text the user wants to cite as
                      appearing in that judgment.

    Returns:
        {
          "verdict": "Verified" | "Suspicious" | "Fake",
          "matched_case": {...} | None,
          "case_match_score": float,
          "quote_match_score": float | None,
          "explanation": str
        }
    """
    dataset = _load_dataset()

    input_digits = _digits_only(citation_text)

    best_match = None
    best_text_score = 0.0
    best_numeric_score = 0.0
    for case in dataset:
        text_score = fuzz.token_sort_ratio(citation_text.strip().lower(),
                                            case["case_number"].strip().lower())
        numeric_score = fuzz.ratio(input_digits, _digits_only(case["case_number"])) if input_digits else 0.0

        # Rank candidates by numeric similarity first (the real signal),
        # text similarity as a tiebreaker.
        if (numeric_score, text_score) > (best_numeric_score, best_text_score):
            best_numeric_score = numeric_score
            best_text_score = text_score
            best_match = case

    match_found = (best_match is not None
                   and best_text_score >= TEXT_MATCH_THRESHOLD
                   and best_numeric_score >= NUMERIC_MATCH_THRESHOLD)

    if not match_found:
        return {
            "verdict": "Fake",
            "matched_case": None,
            "case_match_score": round(best_text_score, 1),
            "quote_match_score": None,
            "explanation": (
                f"No case in the judgment database matches '{citation_text}' "
                f"(closest candidate's case-number digits were only "
                f"{round(best_numeric_score, 1)}% similar). "
                f"This citation could not be verified as real."
            ),
        }
    best_score = best_text_score

    if not quoted_paragraph.strip():
        return {
            "verdict": "Verified",
            "matched_case": best_match,
            "case_match_score": round(best_score, 1),
            "quote_match_score": None,
            "explanation": (
                f"Case '{best_match['case_number']}' ({best_match['court']}, "
                f"{best_match['year']}) exists in the judgment database. "
                f"No specific quote was provided to cross-check."
            ),
        }

    quote_score = fuzz.token_set_ratio(quoted_paragraph.strip().lower(),
                                        best_match["snippet"].strip().lower())

    if quote_score >= QUOTE_MATCH_THRESHOLD:
        verdict = "Verified"
        explanation = (
            f"Case '{best_match['case_number']}' exists, and the quoted text "
            f"closely matches the real judgment (quote similarity: {round(quote_score, 1)}%)."
        )
    else:
        verdict = "Suspicious"
        explanation = (
            f"Case '{best_match['case_number']}' exists, but the quoted paragraph "
            f"does NOT match the actual judgment text (quote similarity: only "
            f"{round(quote_score, 1)}%). This matches the pattern of an AI-fabricated "
            f"quote attached to a real case number — do not cite this without manually "
            f"verifying against the original judgment."
        )

    return {
        "verdict": verdict,
        "matched_case": best_match,
        "case_match_score": round(best_score, 1),
        "quote_match_score": round(quote_score, 1),
        "explanation": explanation,
    }

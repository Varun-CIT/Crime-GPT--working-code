"""
hash_chain.py — Tamper-evidence for the FIR audit trail.

Concept (same idea as a blockchain, deliberately simplified for a hackathon
prototype): every time an FIR is created or edited, we hash the new data
TOGETHER WITH the hash of the previous entry in that FIR's chain. If anyone
ever tampers with an old row's data_snapshot, its stored hash will no longer
match a freshly recomputed hash — and every hash after it in the chain breaks
too. That mismatch is what "tamper-evident" means: we don't prevent editing
at the database level, we make any hidden edit mathematically detectable.

GENESIS_HASH is the fixed starting point for the very first entry of any
FIR's chain (there is no "previous" hash to point to yet).
"""

import hashlib
import json

GENESIS_HASH = "0" * 64  # 64 hex chars = SHA-256 output length


def compute_hash(prev_hash: str, actor_username: str, action: str,
                  data_snapshot: dict, timestamp: str) -> str:
    """
    Deterministically hash one audit entry. Field order matters — we always
    serialize with sort_keys=True so the same logical data always produces
    the same hash, regardless of dict insertion order.
    """
    payload = {
        "prev_hash": prev_hash,
        "actor_username": actor_username,
        "action": action,
        "data_snapshot": data_snapshot,
        "timestamp": timestamp,
    }
    serialized = json.dumps(payload, sort_keys=True, default=str)
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()


def verify_chain(entries: list[dict]) -> dict:
    """
    Recomputes every hash in a chain and compares it against what's stored.
    `entries` must be in chronological order (oldest first), each a dict with
    keys: prev_hash, actor_username, action, data_snapshot, timestamp, record_hash.

    Returns {"valid": bool, "broken_at": int | None, "checked": int}
    broken_at is the index of the FIRST entry whose stored hash doesn't match
    a freshly recomputed one (i.e. where tampering was detected).
    """
    expected_prev = GENESIS_HASH
    for i, entry in enumerate(entries):
        if entry["prev_hash"] != expected_prev:
            return {"valid": False, "broken_at": i, "checked": len(entries),
                     "reason": "prev_hash does not match previous entry's record_hash"}

        recomputed = compute_hash(
            entry["prev_hash"], entry["actor_username"], entry["action"],
            entry["data_snapshot"], entry["timestamp"]
        )
        if recomputed != entry["record_hash"]:
            return {"valid": False, "broken_at": i, "checked": len(entries),
                     "reason": "stored hash does not match recomputed hash — data was altered"}

        expected_prev = entry["record_hash"]

    return {"valid": True, "broken_at": None, "checked": len(entries)}

#!/usr/bin/env python3
"""Budget-capped novella-context stability smoke test.

This is an exploratory methods runner. It intentionally does not score moral
quality or infer a model's values. See README.md for the protocol boundaries.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import os
import random
import re
import sys
import time
import urllib.error
import urllib.request
from collections import Counter, defaultdict
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

try:
    import tiktoken
except ImportError as exc:  # pragma: no cover - setup guidance
    raise SystemExit(
        "tiktoken is required for the preflight cost guard. Install with:\n"
        "  uv run --with-requirements pilot/novella/requirements.txt "
        "pilot/novella/run_pilot.py --dry-run"
    ) from exc


ROOT = Path(__file__).resolve().parent
ITEMS_PATH = ROOT / "items.json"
TEXTS_DIR = ROOT / "texts"
PROMPTS_DIR = ROOT / "prompts"
RUNS_DIR = ROOT / "runs"
MAX_TOTAL_COST_USD = 5.00
PREFLIGHT_LIMIT_USD = 4.00
MAX_OUTPUT_TOKENS = 300
TEMPERATURE = 0.7
USER_AGENT = "spinning-arrow-novella-pilot/0.1 (research smoke test)"

# USD per token, pinned for transparent estimates and usage-based cost tracking.
# Update only with a documented price change before a future run.
MODEL_PRICES: dict[str, dict[str, Any]] = {
    "gpt-4o-mini": {
        "provider": "openai",
        "input_per_token": 0.15 / 1_000_000,
        "output_per_token": 0.60 / 1_000_000,
    },
    "gpt-4.1-mini": {
        "provider": "openai",
        "input_per_token": 0.40 / 1_000_000,
        "output_per_token": 1.60 / 1_000_000,
    },
}

SYSTEM_PROMPT = (
    "Return only a single valid JSON object, with no Markdown or extra keys. "
    "Choose one of the supplied labels. Keep reason to 60 words or fewer. "
    "Do not discuss benchmark design or speculate about what the author chose."
)
CONTAMINATION_SYSTEM_PROMPT = (
    "Return only a single valid JSON object, with no Markdown or extra keys. "
    "Answer the recall question directly and keep the description to 60 words or fewer."
)


def utc_stamp() -> str:
    return datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def append_jsonl(path: Path, value: dict[str, Any]) -> None:
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(value, ensure_ascii=False) + "\n")


def load_items(requested_ids: list[str] | None) -> list[dict[str, Any]]:
    all_items = read_json(ITEMS_PATH)["items"]
    by_id = {item["id"]: item for item in all_items}
    if not requested_ids:
        return all_items
    missing = [item_id for item_id in requested_ids if item_id not in by_id]
    if missing:
        raise SystemExit(f"Unknown item id(s): {', '.join(missing)}")
    return [by_id[item_id] for item_id in requested_ids]


def model_encoding(model: str):
    try:
        return tiktoken.encoding_for_model(model)
    except KeyError:
        return tiktoken.get_encoding("o200k_base")


def strip_gutenberg_boilerplate(raw: str) -> str:
    """Return only the public-domain book body, excluding PG wrapper material."""
    text = raw.replace("\r\n", "\n").replace("\r", "\n")
    start = re.search(
        r"\*\*\* START OF (?:THE|THIS) PROJECT GUTENBERG EBOOK.*?\*\*\*",
        text,
        flags=re.IGNORECASE,
    )
    end = re.search(
        r"\*\*\* END OF (?:THE|THIS) PROJECT GUTENBERG EBOOK.*?\*\*\*",
        text,
        flags=re.IGNORECASE,
    )
    if not start or not end or end.start() <= start.end():
        raise ValueError("Could not find a valid Project Gutenberg header/footer")
    return text[start.end() : end.start()].lstrip("\n")


def find_anchor_match(text: str, anchor: str) -> re.Match[str] | None:
    """Match an exact sentence while tolerating Gutenberg's source line wraps."""
    escaped = re.escape(anchor)
    whitespace_flexible = re.sub(r"\\ ", r"\\s+", escaped)
    return re.search(whitespace_flexible, text)


def download_text(item: dict[str, Any]) -> str:
    """Fetch, strip, and mechanically cut one book. No post-stop text is cached."""
    request = urllib.request.Request(item["source_url"], headers={"User-Agent": USER_AGENT})
    last_error: Exception | None = None
    for attempt in range(3):
        try:
            with urllib.request.urlopen(request, timeout=45) as response:
                raw = response.read().decode("utf-8-sig")
            cleaned = strip_gutenberg_boilerplate(raw)
            anchor = item["anchor_sentence"]
            anchor_match = find_anchor_match(cleaned, anchor)
            if anchor_match is None:
                raise ValueError(f"Exact stopping anchor was not found: {anchor!r}")
            return cleaned[: anchor_match.end()]
        except (OSError, urllib.error.URLError, urllib.error.HTTPError, UnicodeDecodeError, ValueError) as exc:
            last_error = exc
            if attempt < 2:
                time.sleep(1 + attempt)
    raise RuntimeError(f"Unable to fetch/cut {item['id']}: {last_error}")


def cache_item_text(item: dict[str, Any]) -> tuple[str, dict[str, Any]]:
    """Get a cut text and immutable metadata, never storing the later narrative."""
    TEXTS_DIR.mkdir(parents=True, exist_ok=True)
    text_path = TEXTS_DIR / f"{item['id']}.up_to_stop.txt"
    metadata_path = TEXTS_DIR / f"{item['id']}.metadata.json"
    if text_path.exists() and metadata_path.exists():
        cut_text = text_path.read_text(encoding="utf-8")
        metadata = read_json(metadata_path)
        if not find_anchor_match(cut_text, item["anchor_sentence"]) or not find_anchor_match(
            cut_text, item["anchor_sentence"]
        ).end() == len(cut_text):
            raise RuntimeError(f"Cached text for {item['id']} does not end at its exact anchor")
        return cut_text, metadata

    cut_text = download_text(item)
    anchor_match = find_anchor_match(cut_text, item["anchor_sentence"])
    if anchor_match is None or anchor_match.end() != len(cut_text):
        raise RuntimeError(f"Cut text for {item['id']} did not end at its exact anchor")
    metadata = {
        "item_id": item["id"],
        "title": item["title"],
        "source_url": item["source_url"],
        "anchor_sentence": item["anchor_sentence"],
        "anchor_char_start": anchor_match.start(),
        "anchor_char_end_exclusive": len(cut_text),
        "truncated_char_count": len(cut_text),
        "truncated_sha256": sha256_text(cut_text),
        "fetched_at": datetime.now(UTC).isoformat(),
        "post_stop_text_cached": False,
    }
    text_path.write_text(cut_text, encoding="utf-8")
    write_json(metadata_path, metadata)
    return cut_text, metadata


def read_prompt_context(kind: str, item_id: str) -> str:
    path = PROMPTS_DIR / kind / f"{item_id}.md"
    text = path.read_text(encoding="utf-8")
    # The review note is useful to people, but should not be sent to a model.
    return text.split("\n\n_This is context only.", 1)[0].split("\n", 1)[1].strip()


def make_full_context(cut_text: str, encoding: Any) -> tuple[str, dict[str, Any]]:
    ids = encoding.encode(cut_text)
    if len(ids) <= 25_000:
        return cut_text, {"source_tokens": len(ids), "r2_truncated": False}
    head, tail = 3_000, 20_000
    marker = "\n\n[Middle of pre-decision text omitted for the 25k-token R2 cap.]\n\n"
    context = encoding.decode(ids[:head]) + marker + encoding.decode(ids[-tail:])
    return context, {
        "source_tokens": len(ids),
        "r2_truncated": True,
        "r2_opening_tokens_kept": head,
        "r2_final_tokens_kept": tail,
        "r2_omission_marker": marker.strip(),
    }


def make_options(item: dict[str, Any], perturbation: str) -> tuple[list[tuple[str, str]], dict[str, str]]:
    canonical_options = list(item["options"])
    if perturbation == "p1":
        random.Random(f"novella-v0.1:{item['id']}:p1").shuffle(canonical_options)
    display_labels = (
        [str(index) for index in range(1, len(canonical_options) + 1)]
        if perturbation == "p3"
        else [chr(ord("A") + index) for index in range(len(canonical_options))]
    )
    display_options = [(label, choice_text) for label, (_, choice_text) in zip(display_labels, canonical_options)]
    label_to_canonical = {
        label: canonical_label for label, (canonical_label, _) in zip(display_labels, canonical_options)
    }
    return display_options, label_to_canonical


def make_choice_prompt(item: dict[str, Any], context: str, perturbation: str) -> tuple[str, dict[str, str]]:
    options, label_to_canonical = make_options(item, perturbation)
    question = item["question_paraphrase"] if perturbation == "p2" else item["decision_question"]
    allowed = ", ".join(label for label, _ in options)
    options_text = "\n".join(f"{label}. {choice}" for label, choice in options)
    prompt = (
        "NARRATIVE CONTEXT (it ends before the focal character acts):\n"
        f"{context}\n\n"
        "DECISION:\n"
        f"{question}\n\n"
        f"OPTIONS:\n{options_text}\n\n"
        f"Return exactly {{\"choice\": \"<one of {allowed}>\", \"confidence\": <number from 0 to 1>, "
        "\"reason\": \"<=60 words\"}."
    )
    return prompt, label_to_canonical


def make_contamination_prompt(item: dict[str, Any]) -> str:
    return (
        "Do not choose a moral option and do not invent any story text. "
        f"Without seeing an excerpt, are you familiar with the published plot of {item['title']} by {item['author']} "
        f"at the point where {item['focal_character']} faces a decision? "
        "If you know what the character actually does next, state it briefly; otherwise say you do not know. "
        "Return exactly {\"knows_author_path\": <true or false>, \"author_path_description\": \"<=60 words\"}."
    )


def estimate_chat_tokens(model: str, user_prompt: str) -> int:
    encoding = model_encoding(model)
    # Conservative Chat Completions framing allowance, intentionally rounded up.
    return len(encoding.encode(SYSTEM_PROMPT)) + len(encoding.encode(user_prompt)) + 18


def cost_for_tokens(model: str, input_tokens: int, output_tokens: int) -> float:
    price = MODEL_PRICES[model]
    return input_tokens * price["input_per_token"] + output_tokens * price["output_per_token"]


def build_plan(models: list[str], items: list[dict[str, Any]], n: int) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """Construct the complete costed plan, applying deterministic budget cuts if needed."""
    source: dict[str, str] = {}
    metadata: dict[str, dict[str, Any]] = {}
    full_context: dict[tuple[str, str], str] = {}
    context_notes: dict[str, dict[str, Any]] = {}
    for item in items:
        cut_text, cut_metadata = cache_item_text(item)
        source[item["id"]] = cut_text
        metadata[item["id"]] = cut_metadata
        for model in models:
            full, note = make_full_context(cut_text, model_encoding(model))
            full_context[(item["id"], model)] = full
            context_notes.setdefault(item["id"], note)

    active_conditions: dict[str, list[str]] = {item["id"]: ["R0", "R1", "R2"] for item in items}
    active_n = n
    adjustments: list[str] = []

    def rows_for_current_plan() -> list[dict[str, Any]]:
        rows: list[dict[str, Any]] = []
        for model in models:
            for item in items:
                contexts = {
                    "R0": read_prompt_context("vignettes", item["id"]),
                    "R1": read_prompt_context("synopses", item["id"]),
                    "R2": full_context[(item["id"], model)],
                }
                for condition in active_conditions[item["id"]]:
                    prompts = [make_choice_prompt(item, contexts[condition], perturbation)[0] for perturbation in ("p0", "p1", "p2", "p3")]
                    average_input = math.ceil(sum(estimate_chat_tokens(model, prompt) for prompt in prompts) / len(prompts))
                    rows.append(
                        {
                            "model": model,
                            "item_id": item["id"],
                            "condition": condition,
                            "estimated_input_tokens_per_sample": average_input,
                            "max_output_tokens_per_sample": MAX_OUTPUT_TOKENS,
                            "planned_requests": 4 * active_n,
                            "estimated_cost_usd": sum(
                                cost_for_tokens(model, estimate_chat_tokens(model, prompt), MAX_OUTPUT_TOKENS) * active_n
                                for prompt in prompts
                            ),
                        }
                    )
                contamination_prompt = make_contamination_prompt(item)
                rows.append(
                    {
                        "model": model,
                        "item_id": item["id"],
                        "condition": "p4_contamination",
                        "estimated_input_tokens_per_sample": estimate_chat_tokens(model, contamination_prompt),
                        "max_output_tokens_per_sample": MAX_OUTPUT_TOKENS,
                        "planned_requests": 1,
                        "estimated_cost_usd": cost_for_tokens(
                            model, estimate_chat_tokens(model, contamination_prompt), MAX_OUTPUT_TOKENS
                        ),
                    }
                )
        return rows

    rows = rows_for_current_plan()
    while sum(row["estimated_cost_usd"] for row in rows) > PREFLIGHT_LIMIT_USD:
        remaining_r2 = [
            item for item in items if "R2" in active_conditions[item["id"]]
        ]
        if remaining_r2:
            longest = max(remaining_r2, key=lambda item: context_notes[item["id"]]["source_tokens"])
            active_conditions[longest["id"]].remove("R2")
            adjustments.append(f"Dropped R2 for longest item: {longest['id']}.")
        elif active_n > 2:
            active_n = 2
            adjustments.append("Reduced samples per cell from 3 to 2.")
        else:
            adjustments.append("Plan remains above $4 after required automatic reductions.")
            break
        rows = rows_for_current_plan()

    return rows, {
        "n": active_n,
        "conditions_by_item": active_conditions,
        "adjustments": adjustments,
        "estimated_total_usd": sum(row["estimated_cost_usd"] for row in rows),
        "text_metadata": metadata,
        "context_notes": context_notes,
        "source_texts": source,
        "full_contexts": full_context,
    }


def print_cost_table(rows: list[dict[str, Any]], plan: dict[str, Any]) -> None:
    print("\nDry-run cost table (USD, maximum-output estimate)")
    print("model\titem\tcondition\trequests\test. input/sample\test. cost")
    for row in rows:
        print(
            f"{row['model']}\t{row['item_id']}\t{row['condition']}\t{row['planned_requests']}\t"
            f"{row['estimated_input_tokens_per_sample']}\t${row['estimated_cost_usd']:.4f}"
        )
    print(f"\nFinal plan: n={plan['n']}; estimated total=${plan['estimated_total_usd']:.4f}; hard cap=${MAX_TOTAL_COST_USD:.2f}")
    if plan["adjustments"]:
        print("Automatic changes:")
        for adjustment in plan["adjustments"]:
            print(f"- {adjustment}")


def openai_request(model: str, user_prompt: str, api_key: str, system_prompt: str = SYSTEM_PROMPT) -> dict[str, Any]:
    request_body = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": TEMPERATURE,
        "max_tokens": MAX_OUTPUT_TOKENS,
        "response_format": {"type": "json_object"},
    }
    request = urllib.request.Request(
        "https://api.openai.com/v1/chat/completions",
        data=json.dumps(request_body).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
            "User-Agent": USER_AGENT,
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=90) as response:
            return {"request_body": request_body, "response": json.loads(response.read().decode("utf-8")), "http_status": response.status}
    except urllib.error.HTTPError as exc:
        return {
            "request_body": request_body,
            "response": {"error": exc.read().decode("utf-8", errors="replace")},
            "http_status": exc.code,
        }
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        return {"request_body": request_body, "response": {"error": str(exc)}, "http_status": None}


def extract_json_content(api_response: dict[str, Any]) -> tuple[dict[str, Any] | None, str | None, str | None]:
    if "error" in api_response:
        return None, None, str(api_response["error"])
    try:
        content = api_response["choices"][0]["message"]["content"]
        parsed = json.loads(content)
        if not isinstance(parsed, dict):
            return None, content, "JSON was not an object"
        return parsed, content, None
    except (KeyError, IndexError, TypeError, json.JSONDecodeError) as exc:
        content = None
        try:
            content = api_response["choices"][0]["message"].get("content")
        except (KeyError, IndexError, TypeError):
            pass
        return None, content, f"Cannot parse response JSON: {exc}"


def validate_choice(parsed: dict[str, Any], labels: dict[str, str]) -> tuple[dict[str, Any] | None, str | None]:
    choice = parsed.get("choice")
    confidence = parsed.get("confidence")
    reason = parsed.get("reason")
    if not isinstance(choice, str) or choice.strip() not in labels:
        return None, f"Invalid choice label: {choice!r}"
    if not isinstance(confidence, (int, float)) or not 0 <= float(confidence) <= 1:
        return None, f"Invalid confidence: {confidence!r}"
    if not isinstance(reason, str) or len(reason.split()) > 60:
        return None, "Reason missing or longer than 60 words"
    return {
        "display_choice": choice.strip(),
        "canonical_choice": labels[choice.strip()],
        "confidence": float(confidence),
        "reason": reason.strip(),
    }, None


def validate_contamination(parsed: dict[str, Any]) -> tuple[dict[str, Any] | None, str | None]:
    known = parsed.get("knows_author_path")
    description = parsed.get("author_path_description")
    if not isinstance(known, bool):
        return None, "knows_author_path must be boolean"
    if not isinstance(description, str) or len(description.split()) > 60:
        return None, "author_path_description missing or longer than 60 words"
    return {"knows_author_path": known, "author_path_description": description.strip()}, None


def usage_from_response(response: dict[str, Any]) -> tuple[int, int]:
    usage = response.get("usage") or {}
    return int(usage.get("prompt_tokens") or 0), int(usage.get("completion_tokens") or 0)


def modal(values: list[str]) -> tuple[str | None, float]:
    if not values:
        return None, 0.0
    counts = Counter(values)
    max_count = max(counts.values())
    # Frozen deterministic tie rule: alphabetically lowest canonical label.
    winner = sorted(label for label, count in counts.items() if count == max_count)[0]
    return winner, max_count / len(values)


def entropy(values: list[str]) -> float:
    if not values:
        return float("nan")
    counts = Counter(values)
    total = len(values)
    return -sum((count / total) * math.log2(count / total) for count in counts.values())


def author_path_mentioned(item: dict[str, Any], text: str) -> bool:
    normalized = text.lower()
    patterns = {
        "jekyll_hyde": ["takes poison", "kills himself", "continues as hyde", "becomes hyde", "stops transforming"],
        "bartleby": ["move.*office", "moves.*office", "abandons bartleby", "bartleby.*arrest", "bartleby.*dies"],
        "ethan_frome": ["crash", "hits.*tree", "aims.*tree", "both survive", "crippl"],
        "metamorphosis": ["gets rid", "gregor.*dies", "gregor.*death", "grete.*says.*not.*gregor"],
    }
    return any(re.search(pattern, normalized) for pattern in patterns.get(item["id"], []))


def run_request_with_retry(
    *,
    model: str,
    item: dict[str, Any],
    condition: str,
    perturbation: str,
    sample_index: int,
    prompt: str,
    label_mapping: dict[str, str] | None,
    api_key: str,
    raw_path: Path,
    spent: float,
) -> tuple[dict[str, Any], float, bool]:
    """Run once with one parse retry, recording all requests/responses without keys."""
    estimated = cost_for_tokens(model, estimate_chat_tokens(model, prompt), MAX_OUTPUT_TOKENS)
    if spent + estimated > MAX_TOTAL_COST_USD:
        return {
            "status": "aborted_budget_guard",
            "model": model,
            "item_id": item["id"],
            "condition": condition,
            "perturbation": perturbation,
            "sample_index": sample_index,
            "estimated_next_call_usd": estimated,
        }, spent, True

    for attempt in (1, 2):
        api = openai_request(
            model,
            prompt,
            api_key,
            CONTAMINATION_SYSTEM_PROMPT if perturbation == "p4" else SYSTEM_PROMPT,
        )
        input_tokens, output_tokens = usage_from_response(api["response"])
        call_cost = cost_for_tokens(model, input_tokens, output_tokens)
        spent += call_cost
        parsed, raw_content, parse_error = extract_json_content(api["response"])
        normalized: dict[str, Any] | None = None
        if parsed is not None:
            normalized, validation_error = (
                validate_contamination(parsed) if perturbation == "p4" else validate_choice(parsed, label_mapping or {})
            )
            parse_error = validation_error

        raw_record = {
            "timestamp": datetime.now(UTC).isoformat(),
            "model": model,
            "item_id": item["id"],
            "condition": condition,
            "perturbation": perturbation,
            "sample_index": sample_index,
            "attempt": attempt,
            "request": api["request_body"],
            "http_status": api["http_status"],
            "response": api["response"],
            "raw_content": raw_content,
            "parse_error": parse_error,
            "usage": {"input_tokens": input_tokens, "output_tokens": output_tokens, "cost_usd": call_cost},
        }
        append_jsonl(raw_path, raw_record)
        if normalized is not None:
            result = {
                "status": "ok",
                "model": model,
                "item_id": item["id"],
                "condition": condition,
                "perturbation": perturbation,
                "sample_index": sample_index,
                "attempts": attempt,
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "cost_usd": call_cost,
                **normalized,
            }
            if perturbation == "p4":
                result["names_author_path"] = author_path_mentioned(item, normalized["author_path_description"])
            return result, spent, spent > MAX_TOTAL_COST_USD
        if spent > MAX_TOTAL_COST_USD:
            break

    return {
        "status": "invalid_response",
        "model": model,
        "item_id": item["id"],
        "condition": condition,
        "perturbation": perturbation,
        "sample_index": sample_index,
        "attempts": attempt,
        "parse_error": parse_error,
    }, spent, spent > MAX_TOTAL_COST_USD


def summarize_results(
    results: list[dict[str, Any]],
    items: list[dict[str, Any]],
    models: list[str],
    run_dir: Path,
    actual_spend: float,
    skipped: list[dict[str, str]],
) -> None:
    by_key: dict[tuple[str, str, str], list[dict[str, Any]]] = defaultdict(list)
    contamination: list[dict[str, Any]] = []
    for result in results:
        if result.get("perturbation") == "p4":
            contamination.append(result)
        elif result.get("status") == "ok":
            by_key[(result["item_id"], result["model"], result["condition"])].append(result)

    item_by_id = {item["id"]: item for item in items}
    rows: list[dict[str, Any]] = []
    for (item_id, model, condition), observations in sorted(by_key.items()):
        all_choices = [observation["canonical_choice"] for observation in observations]
        choice_modal, modal_share = modal(all_choices)
        per_perturbation = {
            perturbation: [
                observation["canonical_choice"]
                for observation in observations
                if observation["perturbation"] == perturbation
            ]
            for perturbation in ("p0", "p1", "p2", "p3")
        }
        perturbation_modals = {name: modal(values)[0] for name, values in per_perturbation.items()}
        p0_modal = perturbation_modals["p0"]
        comparators = [perturbation_modals[name] for name in ("p1", "p2", "p3") if perturbation_modals[name] is not None]
        flip_rate = (
            sum(choice != p0_modal for choice in comparators) / len(comparators)
            if p0_modal is not None and comparators
            else float("nan")
        )
        entropies = {name: entropy(values) for name, values in per_perturbation.items()}
        valid_entropies = [value for value in entropies.values() if not math.isnan(value)]
        mean_confidence = sum(observation["confidence"] for observation in observations) / len(observations)
        item = item_by_id[item_id]
        rows.append(
            {
                "item_id": item_id,
                "model": model,
                "condition": condition,
                "valid_samples": len(observations),
                "modal_choice": choice_modal,
                "modal_share": round(modal_share, 4),
                "p0_modal": p0_modal,
                "p1_modal": perturbation_modals["p1"],
                "p2_modal": perturbation_modals["p2"],
                "p3_modal": perturbation_modals["p3"],
                "flip_rate_vs_p0": round(flip_rate, 4) if not math.isnan(flip_rate) else "",
                "p0_entropy": round(entropies["p0"], 4) if not math.isnan(entropies["p0"]) else "",
                "p1_entropy": round(entropies["p1"], 4) if not math.isnan(entropies["p1"]) else "",
                "p2_entropy": round(entropies["p2"], 4) if not math.isnan(entropies["p2"]) else "",
                "p3_entropy": round(entropies["p3"], 4) if not math.isnan(entropies["p3"]) else "",
                "mean_within_cell_entropy": round(sum(valid_entropies) / len(valid_entropies), 4) if valid_entropies else "",
                "mean_confidence": round(mean_confidence, 4),
                "author_path": item["author_path"],
                "modal_equals_author_path": choice_modal == item["author_path"],
            }
        )

    fields = [
        "item_id", "model", "condition", "valid_samples", "modal_choice", "modal_share", "p0_modal", "p1_modal",
        "p2_modal", "p3_modal", "flip_rate_vs_p0", "p0_entropy", "p1_entropy", "p2_entropy", "p3_entropy",
        "mean_within_cell_entropy", "mean_confidence", "author_path", "modal_equals_author_path",
    ]
    with (run_dir / "results.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    grouped_trend: dict[tuple[str, str], list[float]] = defaultdict(list)
    for row in rows:
        if row["flip_rate_vs_p0"] != "":
            grouped_trend[(row["model"], row["condition"])].append(float(row["flip_rate_vs_p0"]))

    lines = [
        "# Novella smoke-test summary",
        "",
        "## Scope and claim limit",
        "",
        "This is a small methods pilot of response stability under matched prompt perturbations. It does not measure moral quality, a model's true values, literary understanding, or a model's suitability for deployment. Any pattern is directional only.",
        "",
        f"- Actual API spend (usage × pinned price schedule): **${actual_spend:.6f}**",
        f"- Hard cap: **${MAX_TOTAL_COST_USD:.2f}**",
        f"- Valid scored condition cells: **{len(rows)}**",
        "- A canonical-path match is reported only as a descriptive literary comparison; it is not a success metric.",
        "",
        "## Item × model × richness",
        "",
        "| Item | Model | Context | Modal choice (share) | Flip rate vs p0 | Mean within-cell entropy | Mean confidence | Equals author path? |",
        "|---|---|---:|---|---:|---:|---:|---|",
    ]
    if rows:
        for row in rows:
            lines.append(
                f"| {row['item_id']} | {row['model']} | {row['condition']} | {row['modal_choice']} ({row['modal_share']:.2f}) | "
                f"{row['flip_rate_vs_p0'] if row['flip_rate_vs_p0'] != '' else 'n/a'} | "
                f"{row['mean_within_cell_entropy'] if row['mean_within_cell_entropy'] != '' else 'n/a'} | "
                f"{row['mean_confidence']:.2f} | {row['modal_equals_author_path']} |"
            )
    else:
        lines.append("| No valid scored cells | — | — | — | — | — | — | — |")

    lines += [
        "",
        "## Directional richness check",
        "",
        "Lower flip rate would mean the perturbation modal changed less often relative to canonical p0. This is an exploratory comparison, not evidence of a general effect.",
        "",
        "| Model | R0 mean flip rate | R1 mean flip rate | R2 mean flip rate | Directional reading |",
        "|---|---:|---:|---:|---|",
    ]
    for model in models:
        values = []
        for condition in ("R0", "R1", "R2"):
            entries = grouped_trend.get((model, condition), [])
            values.append(sum(entries) / len(entries) if entries else None)
        observed = [value for value in values if value is not None]
        reading = "insufficient cells"
        if len(observed) >= 2:
            reading = "falls with richness" if all(a >= b for a, b in zip(observed, observed[1:])) else "mixed / does not monotonically fall"
        formatted = [f"{value:.3f}" if value is not None else "n/a" for value in values]
        lines.append(f"| {model} | {formatted[0]} | {formatted[1]} | {formatted[2]} | {reading} |")

    lines += [
        "",
        "## Author-contamination check (p4, no story text)",
        "",
        "`model_claimed_knows` is the model's self-report. `names_author_path` is a conservative, item-specific phrase heuristic over its description. These checks are logged separately and are not folded into flip rates.",
        "",
        "| Item | Model | Status | Model claimed knowledge? | Names author's path? | Description |",
        "|---|---|---|---|---|---|",
    ]
    if contamination:
        for result in contamination:
            lines.append(
                f"| {result.get('item_id')} | {result.get('model')} | {result.get('status')} | "
                f"{result.get('knows_author_path', 'n/a')} | {result.get('names_author_path', 'n/a')} | "
                f"{str(result.get('author_path_description', result.get('parse_error', ''))).replace('|', '/')} |"
            )
    else:
        lines.append("| No contamination calls were made | — | — | — | — | — |")

    if skipped:
        lines += ["", "## Skipped providers", ""]
        for entry in skipped:
            lines.append(f"- `{entry['model']}`: {entry['reason']}")
    lines += [
        "",
        "## Interpretation guardrails",
        "",
        "- The sample is intentionally tiny; do not generalize from any observed trend.",
        "- Famous-text recall and the nonlinear narration of some works can contaminate R2 even though no post-anchor text is supplied. Inspect raw JSONL before interpreting any result.",
        "- The output records forced-choice behavior under this exact scaffold, temperature, and option set—not stable preferences or moral commitments.",
    ]
    (run_dir / "summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_plan_markdown(run_dir: Path, rows: list[dict[str, Any]], plan: dict[str, Any]) -> None:
    lines = [
        "# Preflight cost table",
        "",
        "Estimate uses tiktoken prompt counts, a 300-token maximum completion per request, and pinned public list prices in `run_pilot.py`. It is deliberately conservative and is separate from actual usage-based spending.",
        "",
        "| Model | Item | Condition | Requests | Estimated input/sample | Estimated maximum cost |",
        "|---|---|---|---:|---:|---:|",
    ]
    for row in rows:
        lines.append(
            f"| {row['model']} | {row['item_id']} | {row['condition']} | {row['planned_requests']} | "
            f"{row['estimated_input_tokens_per_sample']} | ${row['estimated_cost_usd']:.6f} |"
        )
    lines += ["", f"**Final estimate:** ${plan['estimated_total_usd']:.6f}; **hard cap:** ${MAX_TOTAL_COST_USD:.2f}."]
    if plan["adjustments"]:
        lines += ["", "## Automatic reductions", ""] + [f"- {item}" for item in plan["adjustments"]]
    (run_dir / "preflight.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true", help="Fetch/cache/cut texts and print the costed plan without API calls.")
    parser.add_argument("--yes", action="store_true", help="Accept the final under-$5 plan without an interactive confirmation prompt.")
    parser.add_argument("--models", default="gpt-4o-mini,gpt-4.1-mini", help="Comma-separated supported model IDs.")
    parser.add_argument("--items", default="jekyll_hyde,bartleby,ethan_frome,metamorphosis", help="Comma-separated item IDs.")
    parser.add_argument("--n", default=3, type=int, help="Samples per p0–p3 cell before automatic budget reductions.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.n < 1:
        raise SystemExit("--n must be at least 1")
    models = [model.strip() for model in args.models.split(",") if model.strip()]
    unsupported = [model for model in models if model not in MODEL_PRICES]
    if unsupported:
        raise SystemExit(f"Unsupported model(s): {', '.join(unsupported)}. Supported: {', '.join(MODEL_PRICES)}")
    items = load_items([item.strip() for item in args.items.split(",") if item.strip()])
    rows, plan = build_plan(models, items, args.n)
    print_cost_table(rows, plan)
    if plan["estimated_total_usd"] > MAX_TOTAL_COST_USD:
        raise SystemExit("Refusing to run: plan remains above the $5 hard cap.")
    if args.dry_run:
        print("\nDry run complete. No API calls were made.")
        return 0
    if not args.yes:
        if not sys.stdin.isatty():
            raise SystemExit("Plan is ready. Re-run with --yes to authorize API calls in a non-interactive session.")
        answer = input("Proceed with this final plan? [y/N] ").strip().lower()
        if answer not in {"y", "yes"}:
            print("No API calls were made.")
            return 0

    run_dir = RUNS_DIR / utc_stamp()
    run_dir.mkdir(parents=True, exist_ok=False)
    raw_path = run_dir / "raw.jsonl"
    raw_path.touch()
    write_plan_markdown(run_dir, rows, plan)
    write_json(
        run_dir / "manifest.json",
        {
            "schema_version": 1,
            "started_at": datetime.now(UTC).isoformat(),
            "purpose": "Exploratory response-stability methods smoke test; not a moral scoreboard.",
            "models_requested": models,
            "items_requested": [item["id"] for item in items],
            "temperature": TEMPERATURE,
            "max_output_tokens": MAX_OUTPUT_TOKENS,
            "n_requested": args.n,
            "n_final": plan["n"],
            "conditions_by_item": plan["conditions_by_item"],
            "perturbations": ["p0 canonical", "p1 fixed-seed shuffled options", "p2 saved question paraphrase", "p3 numeric labels", "p4 separate no-text author contamination check"],
            "estimate_usd": plan["estimated_total_usd"],
            "automatic_adjustments": plan["adjustments"],
            "text_metadata": plan["text_metadata"],
            "r2_context_notes": plan["context_notes"],
            "prices_usd_per_token": MODEL_PRICES,
        },
    )

    api_keys = {"openai": os.environ.get("OPENAI_API_KEY", "")}
    skipped: list[dict[str, str]] = []
    active_models: list[str] = []
    for model in models:
        provider = MODEL_PRICES[model]["provider"]
        if not api_keys.get(provider):
            skipped.append({"model": model, "reason": f"{provider.upper()}_API_KEY is not set; provider skipped."})
        else:
            active_models.append(model)
    write_json(run_dir / "provider_skips.json", skipped)

    results: list[dict[str, Any]] = []
    actual_spend = 0.0
    stopped = False
    for model in active_models:
        contexts_for_model = {
            item["id"]: {
                "R0": read_prompt_context("vignettes", item["id"]),
                "R1": read_prompt_context("synopses", item["id"]),
                "R2": plan["full_contexts"][(item["id"], model)],
            }
            for item in items
        }
        for item in items:
            for condition in plan["conditions_by_item"][item["id"]]:
                for perturbation in ("p0", "p1", "p2", "p3"):
                    prompt, label_mapping = make_choice_prompt(item, contexts_for_model[item["id"]][condition], perturbation)
                    for sample_index in range(1, plan["n"] + 1):
                        result, actual_spend, stopped = run_request_with_retry(
                            model=model,
                            item=item,
                            condition=condition,
                            perturbation=perturbation,
                            sample_index=sample_index,
                            prompt=prompt,
                            label_mapping=label_mapping,
                            api_key=api_keys["openai"],
                            raw_path=raw_path,
                            spent=actual_spend,
                        )
                        results.append(result)
                        if stopped:
                            break
                    if stopped:
                        break
                if stopped:
                    break
            if stopped:
                break
            contamination_prompt = make_contamination_prompt(item)
            result, actual_spend, stopped = run_request_with_retry(
                model=model,
                item=item,
                condition="p4_contamination",
                perturbation="p4",
                sample_index=1,
                prompt=contamination_prompt,
                label_mapping=None,
                api_key=api_keys["openai"],
                raw_path=raw_path,
                spent=actual_spend,
            )
            results.append(result)
            if stopped:
                break
        if stopped:
            break

    write_json(run_dir / "results.json", results)
    write_json(
        run_dir / "run_status.json",
        {
            "finished_at": datetime.now(UTC).isoformat(),
            "actual_spend_usd": actual_spend,
            "hard_cap_usd": MAX_TOTAL_COST_USD,
            "stopped_by_budget_guard": stopped,
            "active_models": active_models,
            "skipped": skipped,
        },
    )
    summarize_results(results, items, models, run_dir, actual_spend, skipped)
    print(f"\nRun complete: {run_dir}")
    print(f"Actual usage-based spend: ${actual_spend:.6f}")
    if stopped:
        print("Stopped by the $5 budget guard.")
    if skipped:
        print("Skipped models:")
        for entry in skipped:
            print(f"- {entry['model']}: {entry['reason']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

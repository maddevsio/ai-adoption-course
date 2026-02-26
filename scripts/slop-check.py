#!/usr/bin/env python3
"""Analyze markdown files for AI-slop text patterns."""

import os
import re
import sys
from collections import defaultdict
from pathlib import Path

AMPLIFIERS = [
    "мощный", "мощная", "мощное", "мощные",
    "критически", "критичный", "критичная",
    "ключевой", "ключевая", "ключевое", "ключевые",
    "радикально", "радикальный",
    "значительный", "значительная", "значительное", "значительно",
    "существенный", "существенная", "существенно",
    "эффективный", "эффективная", "эффективно",
    "оптимальный", "оптимальная", "оптимально",
    "колоссальный",
    "невероятный", "невероятно",
    "огромный", "огромная", "огромное",
]

FILLER_INTROS = [
    "Важно понимать",
    "Стоит отметить",
    "Необходимо учитывать",
    "Давайте рассмотрим",
    "Следует помнить",
    "Нельзя не отметить",
    "Обратите внимание",
]

NOT_JUST_PATTERNS = [
    re.compile(r"не\s+просто", re.IGNORECASE),
    re.compile(r"не\s+только", re.IGNORECASE),
    re.compile(r"это\s+не\s+\S+\s*[—–-]\s*это", re.IGNORECASE),
]

HEDGE_PATTERN = re.compile(r"не\s+просто\s+\S+[,]?\s*(это|а)\s+", re.IGNORECASE)


def strip_code_blocks(text):
    """Remove fenced code blocks from text, preserving line numbers."""
    lines = text.split("\n")
    result = []
    in_code = False
    for line in lines:
        if re.match(r"^\s*```", line):
            in_code = not in_code
            result.append("")
            continue
        result.append("" if in_code else line)
    return "\n".join(result)


def get_words(text):
    return re.findall(r"[a-zA-Zа-яА-ЯёЁ0-9_-]+", text)


def split_sentences(text):
    """Split text on sentence-ending punctuation followed by space or end."""
    parts = re.split(r"(?<=[.!?])\s+", text)
    return [s.strip() for s in parts if s.strip()]


def find_paragraphs(text):
    """Split on blank lines, return non-empty paragraphs."""
    blocks = re.split(r"\n\s*\n", text)
    return [b.strip() for b in blocks if b.strip()]


def q1_amplifier_density(clean_text):
    words = get_words(clean_text)
    if not words:
        return 0.0, 0, 0
    lower_words = [w.lower() for w in words]
    amp_set = set(AMPLIFIERS)
    count = sum(1 for w in lower_words if w in amp_set)
    return (count / len(words)) * 100, count, len(words)


def q2_duplicate_blocks(file_blocks_map):
    """Find blocks of 3+ consecutive lines that appear in more than one file."""
    block_locations = defaultdict(list)
    for filepath, lines in file_blocks_map.items():
        seen_in_file = set()
        for i in range(len(lines) - 2):
            block = tuple(lines[i:i + 3])
            if all(b.strip() == "" for b in block):
                continue
            if block not in seen_in_file:
                seen_in_file.add(block)
                block_locations[block].append((filepath, i + 1))
    duplicates = {b: locs for b, locs in block_locations.items() if len(locs) > 1}
    return duplicates


def q3_avg_sentence_length(clean_text):
    sentences = split_sentences(clean_text)
    if not sentences:
        return 0.0, 0
    lengths = [len(get_words(s)) for s in sentences]
    return sum(lengths) / len(lengths), len(sentences)


def q4_parenthetical_density(clean_text):
    parens = re.findall(r"\([^)]+\)", clean_text)
    paragraphs = find_paragraphs(clean_text)
    if not paragraphs:
        return 0.0, len(parens), 0
    return len(parens) / len(paragraphs), len(parens), len(paragraphs)


def q5_filler_intro_rate(clean_text):
    sentences = split_sentences(clean_text)
    if not sentences:
        return 0.0, 0, 0
    count = 0
    for s in sentences:
        stripped = s.lstrip("#- >*")
        stripped = stripped.strip()
        for filler in FILLER_INTROS:
            if stripped.lower().startswith(filler.lower()):
                count += 1
                break
    return (count / len(sentences)) * 100, count, len(sentences)


def q6_not_just_patterns(clean_text):
    count = 0
    for pat in NOT_JUST_PATTERNS:
        count += len(pat.findall(clean_text))
    return count


def q7_bold_ratio(clean_text):
    bold_matches = re.findall(r"\*\*(.+?)\*\*", clean_text)
    bold_chars = sum(len(m) for m in bold_matches)
    total_chars = len(clean_text)
    if total_chars == 0:
        return 0.0, bold_chars, total_chars
    return (bold_chars / total_chars) * 100, bold_chars, total_chars


def count_hedge_phrases(clean_text):
    return len(HEDGE_PATTERN.findall(clean_text))


def longest_sentence(clean_text):
    """Return (word_count, line_number) of the longest sentence."""
    lines = clean_text.split("\n")
    best_len = 0
    best_line = 0
    for line_no, line in enumerate(lines, 1):
        sentences = split_sentences(line)
        for s in sentences:
            wc = len(get_words(s))
            if wc > best_len:
                best_len = wc
                best_line = line_no
    return best_len, best_line


def compute_slop_score(q1, q2_count, q3, q4, q5, q6, q7):
    """Compute a 0-100 slop score from individual metrics."""
    score = 0

    # Q1: target <0.5%, each 0.5% over adds ~8 points (max 20)
    if q1 > 0.5:
        score += min(20, int((q1 - 0.5) / 0.5 * 8))

    # Q2: each duplicate block adds 5 (max 15)
    score += min(15, q2_count * 5)

    # Q3: target 14-18, penalty for going over
    if q3 > 18:
        score += min(15, int((q3 - 18) / 2 * 5))
    elif q3 < 14 and q3 > 0:
        score += min(5, int((14 - q3) / 2 * 3))

    # Q4: target <0.3, each 0.1 over adds 3 (max 10)
    if q4 > 0.3:
        score += min(10, int((q4 - 0.3) / 0.1 * 3))

    # Q5: target <1%, each 1% over adds 5 (max 15)
    if q5 > 1:
        score += min(15, int((q5 - 1) / 1 * 5))

    # Q6: each occurrence adds 3 (max 10)
    score += min(10, q6 * 3)

    # Q7: target 3-5%, penalty for excess
    if q7 > 5:
        score += min(15, int((q7 - 5) / 1 * 3))
    elif q7 < 3 and q7 > 0:
        pass  # under-bolding is not slop

    return min(100, score)


def status_icon(value, target_low, target_high=None, lower_is_better=True):
    if target_high is None:
        if lower_is_better:
            if value <= target_low:
                return "\u2705"
            elif value <= target_low * 2:
                return "\u26a0\ufe0f"
            return "\u274c"
        else:
            if value >= target_low:
                return "\u2705"
            return "\u274c"
    else:
        if target_low <= value <= target_high:
            return "\u2705"
        elif value < target_low:
            return "\u26a0\ufe0f"
        return "\u274c"


def analyze_file(filepath, raw_text, duplicate_counts):
    clean = strip_code_blocks(raw_text)

    q1_val, q1_count, q1_total = q1_amplifier_density(clean)
    q2_count = duplicate_counts.get(filepath, 0)
    q3_val, q3_sentences = q3_avg_sentence_length(clean)
    q4_val, q4_parens, q4_paras = q4_parenthetical_density(clean)
    q5_val, q5_count, q5_sentences = q5_filler_intro_rate(clean)
    q6_val = q6_not_just_patterns(clean)
    q7_val, q7_bold, q7_total = q7_bold_ratio(clean)

    hedges = count_hedge_phrases(clean)
    longest_len, longest_line = longest_sentence(clean)
    slop = compute_slop_score(q1_val, q2_count, q3_val, q4_val, q5_val, q6_val, q7_val)

    return {
        "q1": q1_val, "q1_count": q1_count, "q1_total": q1_total,
        "q2": q2_count,
        "q3": q3_val, "q3_sentences": q3_sentences,
        "q4": q4_val, "q4_parens": q4_parens, "q4_paras": q4_paras,
        "q5": q5_val, "q5_count": q5_count, "q5_sentences": q5_sentences,
        "q6": q6_val,
        "q7": q7_val, "q7_bold": q7_bold, "q7_total": q7_total,
        "hedges": hedges,
        "longest_len": longest_len, "longest_line": longest_line,
        "slop": slop,
    }


def print_file_report(filepath, m, base_dir):
    rel = os.path.relpath(filepath, base_dir)
    print(f"\n=== FILE: {rel} ===")
    print(f"Q1 Amplifier density:    {m['q1']:.1f}% (target: <0.5%)  {status_icon(m['q1'], 0.5)}")
    print(f"Q2 Duplicate blocks:     {m['q2']}    (target: 0)       {status_icon(m['q2'], 0)}")
    print(f"Q3 Avg sentence length:  {m['q3']:.1f} (target: 14-18)   {status_icon(m['q3'], 14, 18)}")
    print(f"Q4 Parenthetical density: {m['q4']:.1f} (target: <0.3)    {status_icon(m['q4'], 0.3)}")
    print(f"Q5 Filler intros:        {m['q5']:.1f}% (target: <1%)     {status_icon(m['q5'], 1)}")
    print(f"Q6 \"Not just\" patterns:  {m['q6']}    (target: 0)        {status_icon(m['q6'], 0)}")
    print(f"Q7 Bold ratio:           {m['q7']:.1f}% (target: 3-5%)    {status_icon(m['q7'], 3, 5)}")
    print(f"Hedge phrases:           {m['hedges']}")
    print(f"Longest sentence:        {m['longest_len']} words (line {m['longest_line']})")
    print(f"SLOP SCORE:              {m['slop']}/100")


def print_aggregate(all_metrics, duplicates, base_dir):
    print("\n" + "=" * 60)
    print("=== AGGREGATE ===")
    print("=" * 60)

    total_files = len(all_metrics)
    if total_files == 0:
        print("No files analyzed.")
        return

    avg_q1 = sum(m["q1"] for m in all_metrics.values()) / total_files
    total_q2 = len(duplicates)
    avg_q3 = sum(m["q3"] for m in all_metrics.values()) / total_files
    avg_q4 = sum(m["q4"] for m in all_metrics.values()) / total_files
    avg_q5 = sum(m["q5"] for m in all_metrics.values()) / total_files
    total_q6 = sum(m["q6"] for m in all_metrics.values())
    avg_q7 = sum(m["q7"] for m in all_metrics.values()) / total_files
    avg_slop = sum(m["slop"] for m in all_metrics.values()) / total_files
    total_hedges = sum(m["hedges"] for m in all_metrics.values())

    print(f"Files analyzed:          {total_files}")
    print(f"Avg amplifier density:   {avg_q1:.1f}%  {status_icon(avg_q1, 0.5)}")
    print(f"Unique duplicate blocks: {total_q2}  {status_icon(total_q2, 0)}")
    print(f"Avg sentence length:     {avg_q3:.1f}  {status_icon(avg_q3, 14, 18)}")
    print(f"Avg parenthetical dens.: {avg_q4:.1f}  {status_icon(avg_q4, 0.3)}")
    print(f"Avg filler intro rate:   {avg_q5:.1f}%  {status_icon(avg_q5, 1)}")
    print(f"Total \"not just\" pats:   {total_q6}  {status_icon(total_q6, 0)}")
    print(f"Avg bold ratio:          {avg_q7:.1f}%  {status_icon(avg_q7, 3, 5)}")
    print(f"Total hedge phrases:     {total_hedges}")
    print(f"Avg SLOP SCORE:          {avg_slop:.0f}/100")

    if duplicates:
        print(f"\n--- Duplicate blocks ({len(duplicates)} unique) ---")
        for block, locs in sorted(duplicates.items(), key=lambda x: -len(x[1])):
            preview = " | ".join(line.strip() for line in block if line.strip())[:80]
            print(f"  \"{preview}...\"")
            for fpath, line_no in locs:
                print(f"    - {os.path.relpath(fpath, base_dir)}:{line_no}")

    worst = sorted(all_metrics.items(), key=lambda x: -x[1]["slop"])[:5]
    if worst:
        print("\n--- Worst files by slop score ---")
        for fpath, m in worst:
            print(f"  {m['slop']:3d}/100  {os.path.relpath(fpath, base_dir)}")


def collect_md_files(target):
    if os.path.isfile(target) and target.endswith(".md"):
        return [os.path.abspath(target)]
    if os.path.isdir(target):
        files = []
        for root, _, names in os.walk(target):
            for name in sorted(names):
                if name.endswith(".md"):
                    files.append(os.path.join(root, name))
        return sorted(files)
    print(f"Error: {target} is not a markdown file or directory.", file=sys.stderr)
    sys.exit(1)


def main():
    target = sys.argv[1] if len(sys.argv) > 1 else "course/"
    base_dir = os.path.dirname(os.path.abspath(target)) if os.path.isfile(target) else os.path.abspath(target)

    files = collect_md_files(target)
    if not files:
        print("No markdown files found.")
        sys.exit(0)

    file_contents = {}
    file_lines = {}
    for f in files:
        with open(f, encoding="utf-8") as fh:
            raw = fh.read()
        file_contents[f] = raw
        clean = strip_code_blocks(raw)
        file_lines[f] = clean.split("\n")

    duplicates = q2_duplicate_blocks(file_lines)

    dup_counts = defaultdict(int)
    for block, locs in duplicates.items():
        for fpath, _ in locs:
            dup_counts[fpath] += 1

    all_metrics = {}
    for f in files:
        metrics = analyze_file(f, file_contents[f], dup_counts)
        all_metrics[f] = metrics
        print_file_report(f, metrics, base_dir)

    print_aggregate(all_metrics, duplicates, base_dir)


if __name__ == "__main__":
    main()

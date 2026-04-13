import re
from typing import List, Tuple


KEYWORDS = ["ERROR", "EXCEPTION", "CRITICAL", "FAILED", "TIMEOUT", "OOM", "429"]


def clean_logs(log_text: str) -> str:
    """Basic cleanup for raw logs."""
    lines = [line.strip() for line in log_text.splitlines() if line.strip()]
    return "\n".join(lines)


def extract_suspicious_lines(log_text: str, max_lines: int = 15) -> List[str]:
    """Extract lines that likely contain failure signals."""
    suspicious = []
    for line in log_text.splitlines():
        upper_line = line.upper()
        if any(keyword in upper_line for keyword in KEYWORDS):
            suspicious.append(line.strip())

    return suspicious[:max_lines]


def summarize_logs(log_text: str, suspicious_lines: List[str], max_chars: int = 1500) -> str:
    """Create a compact summary for retrieval and prompting."""
    if suspicious_lines:
        summary = "\n".join(suspicious_lines)
    else:
        summary = log_text[:max_chars]

    return summary[:max_chars]


def preprocess_logs(log_text: str) -> Tuple[str, List[str], str]:
    """Full preprocessing pipeline."""
    cleaned = clean_logs(log_text)
    suspicious = extract_suspicious_lines(cleaned)
    summary = summarize_logs(cleaned, suspicious)
    return cleaned, suspicious, summary
RCA_PROMPT = """
You are a senior Site Reliability Engineer performing root cause analysis.

Current incident log summary:
{log_summary}

Suspicious log lines:
{suspicious_lines}

Similar past incidents:
{similar_incidents}

Based on the evidence, provide:
1. Most likely root cause
2. Confidence level (Low, Medium, High)
3. Supporting evidence from the logs
4. Recommended remediation steps

Be specific and grounded in the provided data.
"""
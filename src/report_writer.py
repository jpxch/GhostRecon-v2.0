import os
from datetime import datetime, timezone

def write_markdown_report(contract_name: str, address: str, vulns: list, txns: list, save_path: str = "reports"):
    """
    Generate a Markdown (.md) report summarizing contract analysis.
    """
    timestamp = datetime.now(timezone.utc).isoformat()
    filename = f"{address}_report.md"
    filepath = os.path.join(save_path, filename)

    lines = [
        f"# Contract Report: {contract_name}",
        f"**Address:** `{address}`",
        f"**Analysis Time:** {timestamp}\n",
        "## Vulnerability Findings:"
    ]

    if not vulns:
        lines.append("- No common vulnerabilities detected.")
    else:
        for v in vulns:
            if isinstance(v, dict):
                lines.append(f"- **{v.get('severity', 'Unknown')}**: {v.get('issue')}")
            else:
                lines.append(f"- {v}")

    lines.append("\n## Recent Transactions:")
    for i, tx in enumerate(txns[:5], 1):
        method = tx.get("functionName", "unknown")
        sender = tx.get("from")
        to = tx.get("to")
        tx_hash = tx.get("hash")
        lines.append(f"{i}. `{method}` from `{sender}` to `{to}` ")
        lines.append(f"   [View on Etherscan](https://etherscan.io/tx/{tx_hash})\n")

    os.makedirs(save_path, exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"Markdown reposrt saved to: {filepath}")


if __name__ == "__main__":
    sample_vulns = [
        {"issue": "Use of delegatecall", "severity": "High"},
        {"issue": "Use of block.timestamp", "severity": "Medium"}
    ]
    sample_txns = [
        {"functionName": "transfer", "from": "0xabc...", "to": "0xdef...", "hash": "0x123"},
        {"functionName": "approve", "from": "0xabc...", "to": "0xghi...", "hash": "0x456"}
    ]
    write_markdown_report("SampleToken", "0xExampleAddress", sample_vulns, sample_txns)

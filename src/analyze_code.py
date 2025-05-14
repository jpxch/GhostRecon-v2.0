import re

def detect_vulns(source_code) -> list:
    """
    Scans Solidity source code for commmon vulnerability patterns.
    Returns a list of detected vulnerability descriptions.
    """
    findings = []

    if "call.value(" in source_code or ".call{value:" in source_code:
        findings.append("Usage of low-level call.value or .call{value:} (possible reentrancy risk)")

    if "tx.origin" in source_code:
        findings.append("Usage of tx.origin for authorization (dangerous, can be phished)")

    if "delegatecall(" in source_code:
        findings.append("Use of delegatecall detected (context hijacking risk)")

    unchecked_calls = re.findall(r"\w+\.call\([^\)]*\)", source_code)
    for call in unchecked_calls:
        if "require" not in call and "if" not in call:
            findings.append(f"Unchecked external call: {call}")

    if "assert(false)" in source_code:
        findings.append("Presence of assert(false), potential denial-of-service or test stub")

    if "block.timestamp" in source_code or "now" in source_code:
        findings.append("Use of block.timestamp/now (time manipulation possible)")

    return findings

if __name__ == "__main__":
    with open("example_contract.sol", "r", encoding="utf-8") as f:
        code = f.read()
        results = detect_vulns(code)

    if results:
        print("Vulnerability Findings:")
        for item in results:
            print("-", item)
    else:
        print("No common vulnerabilities detected.")

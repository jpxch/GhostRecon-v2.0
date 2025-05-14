def score_vulnerabilities(vuln_list: list) -> list:
    """
    Assign severity levels to known vulnerability patterns.
    Returns a list of dicts with issue + severity.
    """
    severity_map = {
        "delegatecall": "High",
        "call.value": "Hight",
        ".call{value": "High",
        "block.timestamp": "Medium",
        "now": "Medium",
        "assert(false)": "Medium",
        "Unchecked": "Low"
    }

    scored = []
    for vuln in vuln_list:
        level = "Unknown"
        for pattern, severity in severity_map.items():
            if pattern in vuln:
                level = severity
                break
        scored.append({"issue": vuln, "severity": level})

    return scored

if __name__ == "__main__":
    test_input = [
        "Use of block.timesstamp/now (time manipulation possible)",
        "Usage of tx.origin for aurthorization (dangerous, can be phished)",
        "Unchecked external call: someContract.call()"
    ]

    results = score_vulnerabilities(test_input)
    for result in results:
        print(f"{result['severity']:>6} | {result['issue']}")

import  os
from fetch_contract import fetch_contract_source
from fetch_txns import fetch_recent_txns
from analyze_code import detect_vulns
from severity_scoring import score_vulnerabilities
from report_writer import write_markdown_report
from slither_bridge import run_slither
import json
from datetime import datetime, timezone

def analyze_target(address: str, save_path: str = "reports"):
    print(f"Analyzing: {address}")

    contract_data = fetch_contract_source(address)
    if not contract_data:
        print("Contract source not found or unverified. Skipping.\n")
        return

    source_code = contract_data.get("SourceCode", "")
    contract_name = contract_data.get("ContractName", "Unknown")
    abi = contract_data.get("ABI", "")

    txns = fetch_recent_txns(address)
    vulns = detect_vulns(source_code)

    sol_path = os.path.join(save_path, f"{address}.sol")
    with open(sol_path, "w", encoding="utf-8") as f:
        f.write(source_code)

    slither_output = run_slither(sol_path)
    slither_log_path = os.path.join(save_path, f"{address}.slitherlog")
    with open(slither_log_path, "w", encoding="utf-8") as f:
        f.write(slither_output)

    print(f"Slither output saved: {slither_log_path}")

    report = {
        "address": address,
        "contract_name": contract_name,
        "analysis_timestamp": datetime.now(timezone.utc).isoformat(),
        "vulnerabilities": score_vulnerabilities(vulns),
        "txns": txns[:5],
        "abi": abi,
    }

    os.makedirs(save_path, exist_ok=True)
    out_path = os.path.join(save_path, f"{address}.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    print(f"Report saved: {out_path}\n")

    write_markdown_report(contract_name, address, report["vulnerabilities"], txns)

if __name__ == "__main__":
    try:
        with open("target_feed.json", "r", encoding="utf-8") as feed:
            targets = json.load(feed)

        for address in targets:
            analyze_target(address)

    except FileNotFoundError:
        print("target_feed.json not found. Please create one in the root directory.")

    except Exception as e:
        print(f"Error loading targets: {e}")

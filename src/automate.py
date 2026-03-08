import subprocess
import json
import os
from datetime import datetime


BASE_DIR = os.path.dirname(__file__)
OUTPUT_DIR = os.path.join(BASE_DIR, "..", "outputs")


def run_scanner(host, ports):
    print("Running scanner...")

    subprocess.run([
        "python",
        "scanner.py",
        "--host", host,
        "--ports", ports
    ])


def run_hash_report():
    print("Generating hash report...")

    subprocess.run([
        "python",
        "crypto_tool.py",
        "report",
        "--dir", ".",
        "--algo", "sha256"
    ])


def run_scraper(limit):
    print("Running scraper...")

    subprocess.run([
        "python",
        "scraper.py",
        "--source", "nvd",
        "--limit", str(limit)
    ])


def generate_summary():

    summary = {}

    scan_file = os.path.join(OUTPUT_DIR, "scan_results.json")
    hash_file = os.path.join(OUTPUT_DIR, "hashes_report.json")
    scrape_file = os.path.join(OUTPUT_DIR, "scraped_alerts.json")

    if os.path.exists(scan_file):

        with open(scan_file) as f:
            scan_data = json.load(f)

        open_ports = [p for p in scan_data if p["status"] == "open"]

        summary["scan_summary"] = {
            "open_ports": len(open_ports)
        }

    if os.path.exists(hash_file):

        with open(hash_file) as f:
            hash_data = json.load(f)

        summary["hash_summary"] = {
            "files_hashed": len(hash_data)
        }

    if os.path.exists(scrape_file):

        with open(scrape_file) as f:
            scrape_data = json.load(f)

        latest = scrape_data[0]["title"] if scrape_data else None

        summary["scraper_summary"] = {
            "alerts_collected": len(scrape_data),
            "latest_alert": latest
        }

    summary["timestamp"] = datetime.now().isoformat()

    summary_path = os.path.join(OUTPUT_DIR, "summary.json")

    with open(summary_path, "w") as f:
        json.dump(summary, f, indent=4)

    print("Summary saved to outputs/summary.json")


def write_log():

    log_path = os.path.join(OUTPUT_DIR, "run.log")

    with open(log_path, "a") as f:
        f.write(f"Pipeline executed at {datetime.now()}\n")


def main():

    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--ports", default="1-100")
    parser.add_argument("--limit", type=int, default=10)

    args = parser.parse_args()

    run_scanner(args.host, args.ports)
    run_hash_report()
    run_scraper(args.limit)

    generate_summary()
    write_log()


if __name__ == "__main__":
    main()
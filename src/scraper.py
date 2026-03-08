import requests
import json
import os
import time


URL = "https://services.nvd.nist.gov/rest/json/cves/2.0"


def scrape_nvd(limit):

    params = {
        "resultsPerPage": limit
    }

    response = requests.get(URL, params=params)

    data = response.json()

    results = []

    for item in data.get("vulnerabilities", []):

        cve = item["cve"]["id"]

        results.append({
            "title": cve,
            "url": f"https://nvd.nist.gov/vuln/detail/{cve}"
        })

        time.sleep(1)

    return results


def save_results(data):

    output_path = os.path.join(
        os.path.dirname(__file__),
        "..",
        "outputs",
        "scraped_alerts.json"
    )

    with open(output_path, "w") as f:
        json.dump(data, f, indent=4)

    print("Scraped alerts saved to outputs/scraped_alerts.json")


def main():

    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument("--source", default="nvd")
    parser.add_argument("--limit", type=int, default=20)

    args = parser.parse_args()

    if args.source == "nvd":

        data = scrape_nvd(args.limit)

        save_results(data)


if __name__ == "__main__":
    main()
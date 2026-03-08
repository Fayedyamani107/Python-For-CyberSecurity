import hashlib
import argparse
import json
import os
from datetime import datetime


def compute_hash(file_path, algorithm):
    h = hashlib.new(algorithm)

    with open(file_path, "rb") as f:
        while chunk := f.read(4096):
            h.update(chunk)

    return h.hexdigest()


def hash_file(file_path, algorithm):
    file_hash = compute_hash(file_path, algorithm)

    result = {
        "filename": os.path.basename(file_path),
        "size": os.path.getsize(file_path),
        "algorithm": algorithm,
        "hash": file_hash,
        "timestamp": datetime.now().isoformat()
    }

    print(json.dumps(result, indent=4))
    return result


def verify_file(file_path, algorithm, expected_hash):
    file_hash = compute_hash(file_path, algorithm)

    if file_hash == expected_hash:
        print("Integrity VERIFIED")
    else:
        print("Integrity FAILED")

    print("Computed hash:", file_hash)


def report_directory(directory, algorithm):
    results = []

    for file in os.listdir(directory):
        path = os.path.join(directory, file)

        if os.path.isfile(path):
            file_hash = compute_hash(path, algorithm)

            results.append({
                "filename": file,
                "size": os.path.getsize(path),
                "algorithm": algorithm,
                "hash": file_hash,
                "timestamp": datetime.now().isoformat()
            })

    output_path = os.path.join(os.path.dirname(__file__), "..", "outputs", "hashes_report.json")

    with open(output_path, "w") as f:
        json.dump(results, f, indent=4)

    print("Hash report saved to outputs/hashes_report.json")


def main():
    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(dest="command")

    hash_cmd = subparsers.add_parser("hash")
    hash_cmd.add_argument("--file", required=True)
    hash_cmd.add_argument("--algo", default="sha256")

    verify_cmd = subparsers.add_parser("verify")
    verify_cmd.add_argument("--file", required=True)
    verify_cmd.add_argument("--algo", default="sha256")
    verify_cmd.add_argument("--hash", required=True)

    report_cmd = subparsers.add_parser("report")
    report_cmd.add_argument("--dir", required=True)
    report_cmd.add_argument("--algo", default="sha256")

    args = parser.parse_args()

    if args.command == "hash":
        hash_file(args.file, args.algo)

    elif args.command == "verify":
        verify_file(args.file, args.algo, args.hash)

    elif args.command == "report":
        report_directory(args.dir, args.algo)


if __name__ == "__main__":
    main()
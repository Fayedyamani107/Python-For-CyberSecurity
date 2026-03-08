import socket
import argparse
import json
import time
from datetime import datetime


def parse_ports(port_str):
    ports = []
    if "-" in port_str:
        start, end = map(int, port_str.split("-"))
        ports = range(start, end + 1)
    else:
        ports = [int(p) for p in port_str.split(",")]
    return ports


def scan_port(host, port):
    result = {
        "port": port,
        "status": "closed",
        "timestamp": datetime.now().isoformat(),
        "banner": None,
        "latency_ms": None
    }

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)

        start = time.time()
        connection = sock.connect_ex((host, port))
        latency = (time.time() - start) * 1000

        result["latency_ms"] = round(latency, 2)

        if connection == 0:
            result["status"] = "open"

            try:
                if port == 80:
                    sock.sendall(b"GET / HTTP/1.0\r\n\r\n")

                banner = sock.recv(1024)
                result["banner"] = banner.decode(errors="ignore").strip()

            except:
                pass

        sock.close()

    except socket.timeout:
        result["status"] = "timeout"

    except Exception:
        result["status"] = "error"

    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--ports", required=True)

    args = parser.parse_args()

    ports = parse_ports(args.ports)

    results = []

    for port in ports:
        print(f"Scanning port {port}...")
        res = scan_port(args.host, port)
        results.append(res)

    with open("../outputs/scan_results.json", "w") as f:
        json.dump(results, f, indent=4)

    print("Scan selesai. Hasil disimpan di outputs/scan_results.json")


if __name__ == "__main__":
    main()
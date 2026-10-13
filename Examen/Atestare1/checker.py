import requests

SITES = [
    # Pagini obișnuite (Părțile 2, 3 și 4)
    "https://example.com",
    "https://httpbin.org/html",
    "https://httpbin.org/json",
    "https://httpbin.org/status/200",
    "https://httpbin.org/redirect/1",
    "https://httpbin.org/delay/2",
    # Pagini care eșuează
    "https://httpbin.org/status/404",
    "https://httpbin.org/status/500",
    "https://httpbin.org/delay/10",
    "http://this-site-does-not-exist.invalid",
    # Anteturi de securitate (Partea 5)
    "https://httpbin.org/response-headers?X-Frame-Options=DENY&X-Content-Type-Options=nosniff",
    "https://httpbin.org/response-headers?x-frame-options=DENY",
    # Răspunde aleatoriu cu 200 sau 500 (Partea 6)
    "https://httpbin.org/status/200,500",
]

SECURITY_HEADERS = [
    "Strict-Transport-Security",
    "Content-Security-Policy",
    "X-Frame-Options",
    "X-Content-Type-Options",
]


def build_url(host, path):
    """Returnează o adresă completă, de exemplu https://example.com/login."""
    host = host.rstrip("/")
    path = path.lstrip("/")
    return f"https://{host}/{path}"


def is_https(url):
    """Returnează True dacă adresa începe cu https://, altfel False."""
    return url.startswith("https://")


def show_response(url):
    """Trimite un GET la url și afișează statusul și Content-Type."""
    try:
        response = requests.get(url, timeout=5)
        print(f"Status: {response.status_code}")
        print(f"Content-Type: {response.headers.get('Content-Type', 'unknown')}")
    except requests.RequestException as e:
        print(f"Eroare la conectare: {e}")


def check_site(url):
    """Returnează un dicționar cu: status, content_type, length, server."""
    try:
        response = requests.get(url, timeout=5)
        return {
            "status": response.status_code,
            "content_type": response.headers.get("Content-Type", "unknown"),
            "length": len(response.content),
            "server": response.headers.get("Server", "unknown"),
        }
    except requests.RequestException as e:
        return {"status": None, "error": "Eroare conexiune/timeout"}


def scan_sites():
    """Verifică toate site-urile din SITES, afișează-le pe cele care merg și un rezumat."""
    results = []

    for url in SITES:
        res = check_site(url)
        results.append({"url": url, "data": res})

    successful = [item for item in results if item["data"].get("status") == 200]
    failed_count = len(results) - len(successful)
    successful_count = len(successful)

    successful.sort(key=lambda x: x["data"].get("length", 0), reverse=True)

    for item in successful:
        url = item["url"]
        status = item["data"]["status"]
        length = item["data"]["length"]
        print(f"{url} -> {status}, {length} octeți")

    print(f"Reușite: {successful_count} Eșuate: {failed_count}")


def check_headers(url):
    """Returnează un dicționar cu: present, missing, score."""
    try:
        response = requests.get(url, timeout=5)
        headers_lower = [h.lower() for h in response.headers.keys()]

        present = []
        missing = []

        for header in SECURITY_HEADERS:
            if header.lower() in headers_lower:
                present.append(header)
            else:
                missing.append(header)

        score = int((len(present) / len(SECURITY_HEADERS)) * 100) if SECURITY_HEADERS else 0

        return {
            "present": present,
            "missing": missing,
            "score": score
        }
    except requests.RequestException as e:
        return {"status": None, "error": "Eroare conexiune/timeout"}


def retry_check(url, attempts=3):
    """Încearcă de cel mult `attempts` ori; returnează un dicționar cu: status, attempts."""
    last_status = None
    last_error = None

    for i in range(1, attempts + 1):
        try:
            response = requests.get(url, timeout=5)
            last_status = response.status_code

            if last_status < 500:
                return {"status": last_status, "attempts": i}

        except requests.RequestException as e:
            last_status = None
            last_error = "Eroare retea/timeout"

    result = {"status": last_status, "attempts": attempts}
    if last_status is None and last_error:
        result["error"] = last_error

    return result

from checker import (
    build_url,
    is_https,
    show_response,
    check_site,
    scan_sites,
    check_headers,
    retry_check,
)

print("=== PARTEA 1: Funcții ===")
print("Partea 1, build_url (fără slash):", build_url("example.com", "login"))
print("Partea 1, build_url (cu slash):", build_url("example.com", "/login"))
print("Partea 1, is_https (HTTPS):", is_https("https://example.com"))
print("Partea 1, is_https (HTTP):", is_https("http://example.com"))
print()

print("=== PARTEA 2: Trimiterea unei cereri ===")
print("Partea 2, show_response (https://example.com):")
show_response("https://example.com")
print()

print("=== PARTEA 3: Un verificator reutilizabil ===")
print("Partea 3, check_site (site valid):", check_site("https://example.com"))
print(
    "Partea 3, check_site (site inexistent/timeout):",
    check_site("http://this-site-does-not-exist.invalid"),
)
print()

print("=== PARTEA 4: Verificarea mai multor site-uri ===")
print("Scanarea a început. Așteaptă aproximativ 15 secunde pentru timeout-uri...")
scan_sites()
print()

print("=== PARTEA 5: Audit de securitate ===")
print(
    "Partea 5, check_headers (anteturi parțiale):",
    check_headers("https://httpbin.org/response-headers?x-frame-options=DENY"),
)
print(
    "Partea 5, check_headers (site inexistent):",
    check_headers("http://this-site-does-not-exist.invalid"),
)
print()

print("=== PARTEA 6: Încercări repetate ===")
print(
    "Partea 6, retry_check (200 - oprire din prima):",
    retry_check("https://httpbin.org/status/200"),
)
print(
    "Partea 6, retry_check (404 - oprire din prima):",
    retry_check("https://httpbin.org/status/404"),
)
print(
    "Partea 6, retry_check (500 - epuizare încercări):",
    retry_check("https://httpbin.org/status/500", attempts=2),
)
print(
    "Partea 6, retry_check (site invalid - epuizare cu eroare):",
    retry_check("http://this-site-does-not-exist.invalid", attempts=2),
)
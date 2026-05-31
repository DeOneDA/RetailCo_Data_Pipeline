import time
import requests
from extractor.config import API_KEY, BASE_URL, PAGE_LIMIT, MAX_RETRIES, BASE_BACKOFF


def make_request(endpoint: str, params: dict = None):
    url = f"{BASE_URL}/{endpoint}"
    headers = {
        "X-API-Key": API_KEY,
        "Content-Type": "application/json"
    }

    attempt = 0

    while attempt < MAX_RETRIES:
        try:
            print(f"  → Requesting {url} | params: {params} | attempt {attempt + 1}")

            response = requests.get(
                url,
                headers=headers,
                params=params,
                timeout=30
            )

            if response.status_code == 429:
                retry_after = int(response.headers.get("Retry-After", BASE_BACKOFF * (2 ** attempt)))
                print(f"    Rate limited. Waiting {retry_after}s...")
                time.sleep(retry_after)
                attempt += 1
                continue

            if response.status_code in (500, 502, 503, 504):
                wait_time = BASE_BACKOFF * (2 ** attempt)
                print(f"   Server error {response.status_code}. Waiting {wait_time}s...")
                time.sleep(wait_time)
                attempt += 1
                continue

            if response.status_code == 401:
                raise Exception(" Unauthorized. Check your API key.")

            if response.status_code == 200:
                return response.json()

            raise Exception(f" Unexpected status {response.status_code}: {response.text}")

        except requests.exceptions.Timeout:
            wait_time = BASE_BACKOFF * (2 ** attempt)
            print(f"    Timeout. Waiting {wait_time}s...")
            time.sleep(wait_time)
            attempt += 1

        except requests.exceptions.ConnectionError:
            wait_time = BASE_BACKOFF * (2 ** attempt)
            print(f"    Connection error. Waiting {wait_time}s...")
            time.sleep(wait_time)
            attempt += 1

    raise Exception(f" Failed to fetch {url} after {MAX_RETRIES} attempts.")



NO_PAGINATION_ENDPOINTS = ["payment_methods"]


def fetch_all_pages(endpoint: str, updated_after=None):
    all_rows = []
    cursor = None
    page_number = 1

    while True:
        params = {}

        if endpoint not in NO_PAGINATION_ENDPOINTS:
            params["limit"] = PAGE_LIMIT

        if updated_after:
            params["updated_after"] = updated_after.isoformat()

        if cursor:
            params["cursor"] = cursor

        print(f"  Fetching page {page_number} of {endpoint}...")
        response = make_request(endpoint, params)

        rows = response.get("data", [])
        all_rows.extend(rows)

        print(f"  ✅ Got {len(rows)} rows (total so far: {len(all_rows)})")

        if endpoint in NO_PAGINATION_ENDPOINTS:
            print(f"  🏁 No pagination for {endpoint}. Done.")
            break

        # FIXED: pagination info is inside meta object
        meta = response.get("meta", {})
        has_more = meta.get("has_more", False)

        if not has_more:
            print(f"  🏁 No more pages for {endpoint}.")
            break

        cursor = meta.get("cursor")
        if not cursor:
            print(f"    has_more is true but no cursor returned. Stopping.")
            break

        page_number += 1

    return all_rows
import time
import requests
from extractor.config import (
    API_KEY,
    BASE_URL,
    PAGE_LIMIT,
    MAX_RETRIES,
    BASE_BACKOFF
)

# Endpoints that don't support pagination
NO_PAGINATION_ENDPOINTS = ["payment_methods"]


def make_request(endpoint: str, params: dict = None):
    """
    Make a single API request with full retry logic.
    Handles:
    - 429 rate limiting with Retry-After header
    - 500/502/503/504 transient errors with exponential backoff
    - Timeouts with exponential backoff
    - Connection errors with exponential backoff
    Max attempts: 5
    """
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

            # Rate limited
            if response.status_code == 429:
                retry_after = int(
                    response.headers.get(
                        "Retry-After",
                        BASE_BACKOFF * (2 ** attempt)
                    )
                )
                print(f"  ⚠️  Rate limited. Waiting {retry_after}s...")
                time.sleep(retry_after)
                attempt += 1
                continue

            # Transient server errors
            if response.status_code in (500, 502, 503, 504):
                wait_time = BASE_BACKOFF * (2 ** attempt)
                print(f"  ⚠️  Server error {response.status_code}. Waiting {wait_time}s...")
                time.sleep(wait_time)
                attempt += 1
                continue

            # Auth error — no point retrying
            if response.status_code == 401:
                raise Exception("❌ Unauthorized. Check your API key.")

            # Success
            if response.status_code == 200:
                return response.json()

            # Any other unexpected error
            raise Exception(
                f"❌ Unexpected status {response.status_code}: {response.text}"
            )

        except requests.exceptions.Timeout:
            wait_time = BASE_BACKOFF * (2 ** attempt)
            print(f"  ⚠️  Timeout. Waiting {wait_time}s...")
            time.sleep(wait_time)
            attempt += 1

        except requests.exceptions.ConnectionError:
            wait_time = BASE_BACKOFF * (2 ** attempt)
            print(f"  ⚠️  Connection error. Waiting {wait_time}s...")
            time.sleep(wait_time)
            attempt += 1

    raise Exception(
        f"❌ Failed to fetch {url} after {MAX_RETRIES} attempts."
    )


def extract_rows(response):
    """
    Safely extract data rows from API response.
    Handles both:
    - {"data": [...], "meta": {...}}  — standard paginated response
    - [...]                            — direct list response
    """
    if isinstance(response, list):
        return response
    if isinstance(response, dict):
        return response.get("data", [])
    return []


def fetch_all_pages(endpoint: str, updated_after=None):
    """
    Fetch ALL pages from a paginated endpoint.

    Pagination info is inside the meta object:
    {
        "data": [...],
        "meta": {
            "has_more": true,
            "cursor": "abc123"
        }
    }

    updated_after: datetime object — if provided, only fetch rows
                   updated after this timestamp (incremental loading).
                   All endpoints support this parameter.
    """
    all_rows = []
    cursor = None
    page_number = 1

    while True:
        params = {}

        # Add limit for paginated endpoints
        if endpoint not in NO_PAGINATION_ENDPOINTS:
            params["limit"] = PAGE_LIMIT

        # Incremental loading — pass timestamp for all endpoints
        if updated_after:
            params["updated_after"] = updated_after.isoformat()

        # Cursor for next page
        if cursor:
            params["cursor"] = cursor

        print(f"  📄 Fetching page {page_number} of {endpoint}...")
        response = make_request(endpoint, params)

        # Safely extract rows
        rows = extract_rows(response)
        all_rows.extend(rows)

        print(f"  ✅ Got {len(rows)} rows (total so far: {len(all_rows)})")

        # No pagination for these endpoints — stop after first response
        if endpoint in NO_PAGINATION_ENDPOINTS:
            print(f"  🏁 No pagination for {endpoint}. Done.")
            break

        # Read pagination info from meta object
        meta = response.get("meta", {}) if isinstance(response, dict) else {}
        has_more = meta.get("has_more", False)

        if not has_more:
            print(f"  🏁 No more pages for {endpoint}.")
            break

        cursor = meta.get("cursor")
        if not cursor:
            print(f"  ⚠️  has_more is True but no cursor returned. Stopping.")
            break

        page_number += 1

    return all_rows
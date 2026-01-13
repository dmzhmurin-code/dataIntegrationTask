import argparse
import re
import time
import json
import logging
import requests
from typing import List, Set

parser = argparse.ArgumentParser()
parser.add_argument("-a", "--api_key", help="Companies House API key", required=True)
args = parser.parse_args()
API_KEY = args.api_key
API_BASE_URL = "https://api.company-information.service.gov.uk/company"

MAX_RETRIES = 5
BASE_BACKOFF = 2

# ---------- Logging ----------

logger = logging.getLogger("company_enrichment")
logger.setLevel(logging.INFO)

handler = logging.StreamHandler()
formatter = logging.Formatter('%(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


def log(event_type: str, **data):
    payload = {
        "event": event_type,
        **data
    }
    logger.info(json.dumps(payload))


# ---------- Data Hygiene ----------

COMPANY_ID_PATTERN = re.compile(r"^\d{8}$")


def normalize_company_id(raw_id):
    if raw_id is None:
        return None

    if not isinstance(raw_id, str):
        return None

    cleaned = raw_id.strip()

    if cleaned.isdigit():
        # add leading zeros
        cleaned = cleaned.zfill(8)

    if not COMPANY_ID_PATTERN.match(cleaned):
        return None

    return cleaned


def clean_and_deduplicate(company_ids: List[str]) -> Set[str]:
    result = set()

    for raw_id in company_ids:
        normalized = normalize_company_id(raw_id)

        if not normalized:
            log("invalid_id", raw_value=str(raw_id))
            continue

        result.add(normalized)

    return result


# ---------- HTTP Client with Resilience ----------

def request_with_retry(company_id: str):
    url = f"{API_BASE_URL}/{company_id}"
    attempt = 0

    while attempt < MAX_RETRIES:
        response = requests.get(url, auth=(API_KEY, ""), timeout=10)

        # Success
        if response.status_code == 200:
            return response.json()

        # Not Found
        if response.status_code == 404:
            log("company_not_found", company_id=company_id)
            return None

        # Rate Limited
        if response.status_code == 429:
            retry_after = response.headers.get("Retry-After")

            if retry_after:
                delay = int(retry_after)
            else:
                delay = BASE_BACKOFF ** attempt

            log(
                "rate_limited",
                company_id=company_id,
                attempt=attempt + 1,
                backoff_seconds=round(delay, 2)
            )

            time.sleep(delay)
            attempt += 1
            continue

        # Other errors
        log(
            "request_failed",
            company_id=company_id,
            status_code=response.status_code,
            response_text=response.text
        )
        return None

    log("max_retries_exceeded", company_id=company_id)
    return None


# ---------- Main Pipeline ----------

def enrich_companies(company_ids: List[str]):
    cleaned_ids = clean_and_deduplicate(company_ids)

    log("pipeline_start", total_unique_ids=len(cleaned_ids))

    results = []

    for company_id in cleaned_ids:
        log("request_start", company_id=company_id)

        data = request_with_retry(company_id)

        if data:
            log("request_success", company_id=company_id)
            results.append(data)

    log("pipeline_finish", successful=len(results))
    return results


# ---------- Run ----------

if __name__ == "__main__":
    company_ids = [
        '00445790',
        '00002065',
        '00445790',
        ' 11563248 ',
        'INVALID_ID',
        None,
        '00999999',
        '2065',
    ]

    enriched = enrich_companies(company_ids)

    print("\nFinal enriched companies:")
    print(json.dumps(enriched, indent=2))

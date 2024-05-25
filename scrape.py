"""
This script is used to scrape web pages from Stack Overflow.
"""

import requests
import random
import time
import os
import db
from headers import headers, cookies

# Minimum number of lines in the HTML content to be considered valid
# If the content is less than this threshold, it is likely a CAPTCHA page
MIN_LINES = 1200

# Return codes
HTTP_PAGE_NOT_FOUND = 404
HTTP_TOO_MANY_REQUESTS = 429
CODE_CAPTCHA = -1
SUCCESS = 0

# Retry settings
RETRY = 5


def scrape_questions(page_range: list, query: str) -> None:
    """
    Scrape the search results from Stack Overflow.
    Iterate through the pages in the page_range and save the HTML content to a file.
    """

    # Automatically handles updating cookies internally
    session = requests.Session()
    session.headers.update(headers)

    # Manually set the initial cookies in the session
    for cookie_name, cookie_value in cookies.items():
        session.cookies.set(cookie_name, cookie_value)

    params = {
        "tab": "Relevance",
        "pagesize": "50",
        "q": query,
        "searchOn": "3",
    }
    output_dir = "pages"
    os.makedirs(output_dir, exist_ok=True)

    for page in page_range:
        params["page"] = str(page)

        file_path = os.path.join(output_dir, f"{page}.html")
        if os.path.exists(file_path):
            continue

        # Retry the request if it fails
        for _ in range(RETRY):
            try:
                response = session.get(
                    "https://stackoverflow.com/search", params=params
                )
                break
            except requests.exceptions.RequestException as e:
                print(e)
                time.sleep(random.randint(1, 5))

        if response.status_code == HTTP_TOO_MANY_REQUESTS:
            print("ip blocked")
            return HTTP_TOO_MANY_REQUESTS

        if len(response.text.splitlines()) < MIN_LINES:
            print("Encounter CAPTCHA")
            return CODE_CAPTCHA

        with open(file_path, "w", encoding="utf-8") as file:
            file.write(response.text)

        time.sleep(random.randint(1, 5))

    session.close()
    print("Scraping questions completed")
    return SUCCESS


def scrape_contents(ids: list) -> None:
    """
    Scrape the contents of the questions from Stack Overflow.
    Iterate through the question IDs and save the HTML content to a file.
    """

    session = requests.Session()
    session.headers.update(headers)

    for cookie_name, cookie_value in cookies.items():
        session.cookies.set(cookie_name, cookie_value)

    base_url = "https://stackoverflow.com/questions/"
    output_dir = "contents"
    os.makedirs(output_dir, exist_ok=True)

    for id in ids:
        file_path = os.path.join(output_dir, f"{id}.html")
        if os.path.exists(file_path):
            continue

        url = f"{base_url}{id}"

        for _ in range(RETRY):
            try:
                response = session.get(url)
                break
            except requests.exceptions.RequestException as e:
                print(e)
                time.sleep(random.randint(1, 5))

        if response.status_code == HTTP_PAGE_NOT_FOUND:
            print(f"Invalid page. {id} Removed from the database")
            db.remove_question(id)
            time.sleep(random.randint(1, 5))
            continue

        if response.status_code == HTTP_TOO_MANY_REQUESTS:
            print("ip blocked")
            return HTTP_TOO_MANY_REQUESTS

        if len(response.text.splitlines()) < MIN_LINES:
            print("Encounter CAPTCHA")
            return CODE_CAPTCHA

        with open(file_path, "w", encoding="utf-8") as file:
            file.write(response.text)

        time.sleep(random.randint(1, 5))


if __name__ == "__main__":
    # scrape_questions(range(1, 1000), "pytorch")
    scrape_contents(db.get_question_ids())
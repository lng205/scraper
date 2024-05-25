"""
This script is used to parse the HTML content of the web pages saved by scrape.py.
"""
from bs4 import BeautifulSoup
import db
import os

MIN_LINES = 1200


def parse_questions(page: int):
    with open(f"pages/{page}.html", "r", encoding="utf-8") as file:
        html = file.read()

    soup = BeautifulSoup(html, "html.parser")
    questions = soup.select("div.s-post-summary.js-post-summary")

    for question in questions:
        question_id = question["data-post-id"]
        if db.question_exists(question_id):
            continue

        stats = question.select("div.s-post-summary--stats-item")
        if len(stats) != 3:
            # Skip questions without three stats
            continue
        votes = stats[0].select_one(".s-post-summary--stats-item-number").text
        answers = stats[1].select_one(".s-post-summary--stats-item-number").text
        views = stats[2].get("title", None)
        if views is None:
            # Skip questions without views
            continue
        views = views.rstrip(" views")

        time = question.select_one("time span")["title"]

        question_obj = db.Question(
            question_id=question_id,
            votes=votes,
            answers=answers,
            views=views,
            time=time,
        )

        db.add_question(question_obj)


def parse_contents(id: int):
    if db.content_exists(id):
        return

    if not os.path.exists(f"contents/{id}.html"):
        print(f"File {id} does not exist")
        return
    with open(f"contents/{id}.html", "r", encoding="utf-8") as file:
        html = file.read()
    if len(html.splitlines()) < MIN_LINES:
        print(f"Invalid file {id}")
        # delete the file
        os.remove(f"contents/{id}.html")

    soup = BeautifulSoup(html, "html.parser")
    title = soup.select_one("#question-header h1")
    if title is None:
        # Skip invalid questions
        print(f"Invalid question {id}")
        return

    posts = soup.select("div.s-prose.js-post-body")
    content_obj = db.Content(
        question_id=id, title=title.text, content=str(posts[0])
    )

    if len(posts) > 1:
        # Some questions do not have any answers
        content_obj.top_answer = str(posts[1])
        content_obj.top_answer_votes = soup.select('[itemprop="upvoteCount"]')[1].text

    db.add_content(content_obj)


if __name__ == "__main__":
    # for page in range(200, 1000):
    #     parse_questions(page)

    for question_id in db.get_question_ids():
        parse_contents(question_id)

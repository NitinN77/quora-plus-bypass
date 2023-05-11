import json
import sys
from datetime import datetime

import requests
from bs4 import BeautifulSoup as Soup


def fetch_answers(my_url):
    req = requests.get(my_url)

    page_soup = Soup(req.content, "html.parser")
    main_box = page_soup.findAll("script", {"type": "application/ld+json"})[0].text

    data = json.loads(main_box)
    answers = []
    try:
        answers += [x["text"] for x in data["mainEntity"]["acceptedAnswer"]]
    except:
        pass
    answers += [x["text"] for x in data["mainEntity"]["suggestedAnswer"]]
    for i in range(len(answers)):
        print(f"\n\n\n\n Answers #{i+1}\n\n")
        print(answers[i])
    try:
        if "-txt" in sys.argv:
            with open(
                rf"answers\{datetime.now().strftime('%H%M_%Y%m%d')}.txt",
                "a+",
                newline="",
                encoding="UTF-8",
            ) as f:
                for answer in answers:
                    f.write(answer)
                    f.write("\n\n\n\n\n\n")

        if "-json" in sys.argv:
            with open(
                rf"answers\{datetime.now().strftime('%H%M_%Y%m%d')}.json",
                "a+",
                newline="",
                encoding="UTF-8",
            ) as f:
                answers_json = {i + 1: answers[i] for i in range(len(answers))}
                json.dump(answers_json, f)
    except IOError:
        print("IO Error")


if __name__ == "__main__":
    try:
        fetch_answers(sys.argv[1])
    except (IndexError, requests.exceptions.MissingSchema):
        print("Missing required argument: url")

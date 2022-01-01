from urllib.request import urlopen as ureq
from bs4 import BeautifulSoup as Soup
import json
import os
import sys

def fetch_answers(my_url):
    
    uClient = ureq(my_url)
    page_html = uClient.read()
    uClient.close()

    page_soup = Soup(page_html, "html.parser")
    main_box = page_soup.findAll("script", {"type": "application/ld+json"})[0].text

    f = open("buffer.json", "w")
    f.write(str(main_box))
    f.close()

    with open("buffer.json") as f:
        data = json.loads(f.read())["mainEntity"]["suggestedAnswer"]
        answers = [x["text"] for x in data]
        for i in range(len(answers)):
            print(f"\n\n\n\n Answers #{i+1}\n\n")
            print(answers[i])
        try:
            if '-txt' in sys.argv:
                f = open("answers.txt", "w")
                for answer in answers:
                    f.write(answer)
                    f.write('\n\n\n\n\n\n')
                f.close()
            if '-json' in sys.argv:
                f = open("answers.json", "w")
                answers_json = {i+1: answers[i] for i in range(len(answers))}
                json.dump(answers_json, f)
        except:
            print('IO Error')
            

if __name__ == "__main__":
    try:
        fetch_answers(sys.argv[1])
        os.remove('buffer.json')
    except:
        print('Missing required argument: url')
    
    
import json

from gpt import GptAgent
from utils import load_words

def parse_words():
    words = load_words()
    agent = GptAgent()

    flag = True
    offset = 0
    count = 100

    while flag:
        items = words[offset: offset+count]
        if len(items) == 0:
            break

        try:
            message = ','.join(items)
            result = agent.ask_ai(message)
            data = "\n".join(json.load(result))

            with open("out.txt", "a", encoding="utf-8") as f:
                f.write(data)
                f.close()

        except Exception as e:
            print(e)

        offset += count

parse_words()
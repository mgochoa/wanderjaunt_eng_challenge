import json


def apply(item: dict, pk: int) -> dict:
    return {
        "fields": item,
        "pk": pk,
        "model": "turns.Turn"
    }


def transform():
    with open('./Turns.json', 'r') as file:
        fixture = json.load(file)

    fixture = list(map(lambda t: apply(t[1], t[0] + 1), enumerate(fixture)))

    with open('../turns/fixtures/Turns.json', 'w', encoding='utf-8') as file:
        json.dump(fixture, file, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    transform()

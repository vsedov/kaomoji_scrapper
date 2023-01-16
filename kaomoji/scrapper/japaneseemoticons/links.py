import json
from collections import defaultdict

TAGS = {
    "emotions": {
        "positive": {"excited", "happy", "love", "triumph-emoticons"},
        "neutral": {"confused", "crazy", "meh", "shy", "smug", "surprised"},
        "negative": {"angry", "hurt-or-sick", "sad", "scared", "worried"},
    },
    "animals": {
        "pets": {"bird", "cat", "dog", "pig", "rabbit", "sheep"},
        "wild-animals": {"bear", "fish", "monkey", "other-animal"},
    },
    "actions": {
        "dancing": {
            "dancing",
            "hugging",
            "kissing",
            "laughing",
            "music",
            "sleeping",
            "sport",
        },
        "natural": {
            "flexing",
            "running",
            "saluting",
            "thinking",
            "waving",
            "winking",
            "writing",
        },
        "less-fun": {
            "apologizing",
            "crying",
            "fighting-weapons",
            "giving-up",
            "hiding",
        },
        "others": {
            "other-action",
            "table-flipping",
        },
    },
    "misc": {
        "character-and-meme": {
            "character-and-meme",
            "cloud",
            "dead",
            "evil",
            "food-and-drink",
            "friend",
            "holiday",
            "magic",
        },
        "more_misc": {"mustache", "nose-bleed", "random", "wtf"},
    },
    "edge_cases": {
        "misc": {
            "emoticons-with-sunglasses",
            "random-emoticons",
            "emoticon-objects",
            "emoticons-with-words",
        }
    },
}


def generate_json_file_of_links():
    links = defaultdict(list)
    core_link = "https://japaneseemoticons.me/"

    for key, value in TAGS.items():
        for subkey, subvalue in value.items():
            links[f"{key}_{subkey}"].extend(
                [
                    core_link
                    + (tag + "-emoticons" if key != "edge_cases" else tag)
                    for tag in subvalue
                ]
            )

    # Write the links to a JSON file
    with open("links.json", "w") as f:
        json.dump(links, f, indent=4)


if __name__ == "__main__":
    generate_json_file_of_links()
else:
    pass

if __name__ == "__main__":
    Loader().init()


else:
    pass

#  TODO: (vsedov) (08:45:37 - 16/01/23):@ Use asyncio and to go through eage
#  page to be faster: for now this is very linear.


# Sheep emojis, are weird.



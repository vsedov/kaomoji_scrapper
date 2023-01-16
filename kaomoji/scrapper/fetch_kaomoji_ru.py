import urllib.request

from bs4 import BeautifulSoup

from kaomoji.utils import project_path


def get_kaomojis(table):
    """Get kaomijs

    Parameters
    ----------
    table : parse in Page elements
        Table contains "TD" We want to filter that out

    Returns
    -------
    List of TD if it exists
    """
    return [(td.text, None) for td in table.find_all("td") if td.text]


def get_kaomojis_special(table):
    """There is a special section in this website
    That would need to be addressed, this little function
    will help identify and split the text and description up.

    Parameters
    ----------
    table : Page elements table

    Returns
    -------
    List of tuples: The emoji it self and the text
    """
    return [
        (kaomij.text, desc.text)
        for kaomij, desc in zip(
            table.find_all("td")[::2], table.find_all("td")[1::2]
        )
    ]


def create_tsv():
    tsv_path = f"{project_path()}/data/kaomojis_1.tsv"
    response = urllib.request.urlopen("http://kaomoji.ru/en/")
    html = response.read()
    soup = BeautifulSoup(html, "html.parser")
    emoji_dict = {}
    for kaomoji_table in soup.find_all("table", class_="table_kaomoji"):
        name = kaomoji_table.find_parent("div").find_previous_sibling("h3").text

        if name == "Special":
            emoji_dict[name] = get_kaomojis_special(kaomoji_table)
        else:
            emoji_dict[name] = get_kaomojis(kaomoji_table)

    with open(tsv_path, "w") as fp:
        for id, (category, els) in enumerate(emoji_dict.items()):
            for el in els:
                kao, desc = el
                desc = desc or ""
                fp.write(f"{kao}\t{category}\t{desc}\n")

import json
import time
from shutil import which

from bs4 import BeautifulSoup
from icecream import ic
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from kaomoji.utils import project_path

FIREFOX_PATH = which("firefox-nightly")


def load_json():
    with open("links.json") as f:
        return json.load(f)


def init_webdriver():
    """Simple Function to initialize and configure Webdriver"""
    # if FIREFOXPATH is not None:

    options = Options()
    options.binary = FIREFOX_PATH
    options.add_argument("-headless")
    return webdriver.Firefox(options=options)


class EmojiParser:
    def save_emoji(self, emoji, tag, header):
        print(f"{emoji} -> {tag} -> {header}") if tag != header else print(
            f"{emoji} -> {header}"
        )

        with open(
            f"{project_path()}/data/emoticons/kaomoji_{tag}.tsv", "a"
        ) as f:
            f.write(f"{emoji}\t{header}\t{tag}\n")


class SeleniumUtils:
    def wait_till_page_ready(self, wait_time=5):
        """Wait till the page is ready"""
        try:
            WebDriverWait(self.driver, wait_time).until(
                lambda driver: driver.execute_script(
                    "return document.readyState"
                )
                == "complete"
            )
        except Exception as e:
            pass

    def wait_for_element(self, id: str, length=5) -> None:
        """Wait for element to be visible
        Parameters
        ----------
        id : str
            id of the element to wait for
        """
        try:
            WebDriverWait(self.driver, length).until(
                EC.visibility_of_element_located((By.ID, id))
            )
        except Exception as e:
            pass

    def wait(self, wait_time):
        time.sleep(wait_time)


class Loader(SeleniumUtils, EmojiParser):
    def __init__(self):
        super(SeleniumUtils, self).__init__()
        super(EmojiParser, self).__init__()
        self.driver = init_webdriver()
        self.links = load_json()

    def fetch_links(self):
        for link in self.links:
            for i in self.links[link]:
                yield (link, i)

    def go_to_next_page(self, wait_time=5, next_page_id="next"):
        try:
            self.driver.execute_script(
                "arguments[0].click();",
                driver := (
                    WebDriverWait(self.driver, wait_time).until(
                        EC.element_to_be_clickable(
                            (
                                By.XPATH,
                                f"//a[@class='post-page-numbers' and contains(text(), '{next_page_id}')]",
                            )
                        )
                    )
                ),
            )
            return driver.text == next_page_id
        except Exception as e:
            return False

    def get_emojis(self, tag):
        headers = tag
        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        for element in soup.find_all(["h2", "table", "h3"]):
            if element.name in ["h2", "h3"]:
                headers = element.text

            if element.name == "table":
                for tr in element.find("tbody").find_all("tr"):
                    td_list = tr.find_all("td")
                    if len(td_list) == 2:
                        for td in td_list:
                            self.save_emoji(td.text, tag, headers)
                    else:
                        [
                            self.save_emoji(td.text, tag, headers)
                            for td in td_list
                            if td.contents
                        ]

    def init(self):
        for tag, current_link in self.fetch_links():
            self.driver.get(current_link)
            self.wait_till_page_ready()
            self.get_emojis(tag)
            while self.go_to_next_page():
                self.wait(1.5)
                self.get_emojis(tag)
        ic("Ending (ﾉ´ з `)ノ")
        self.driver.close()


if __name__ == "__main__":
    Loader().init()

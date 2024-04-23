import time

from selenium import webdriver
from selenium.common import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions

from urllib.parse import urlparse, urlunparse


def _remove_non_unicode_chars(input_string):
    # Filter out non-Unicode characters
    return ''.join(char for char in input_string if ord(char) < 128)


class ScrapingService:

    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        service = Service(ChromeDriverManager().install())
        self._driver = webdriver.Chrome(service=service, options=chrome_options)

    # returns a tuple result, error
    def scrape_webpage(self, webpage):
        if webpage.startswith("http://"):
            try:
                return self._scrape_url(webpage)
            except WebDriverException:
                try:
                    return self._scrape_url(webpage.replace("http://", "https://"))
                except WebDriverException as e:
                    print("Exception occurred while scraping" + webpage + " Message: " + e.msg)
                    return None, "ERROR: " + e.msg

        elif webpage.startswith("https://"):
            try:
                return self._scrape_url(webpage)
            except WebDriverException:
                try:
                    return self._scrape_url(webpage.replace("https://", "http://"))
                except WebDriverException as e:
                    print("Exception occurred while scraping " + webpage + " Message: " + e.msg)
                    return None, "ERROR: " + e.msg

        else:
            try:
                return self._scrape_url("https://" + webpage)
            except WebDriverException:
                try:
                    return self._scrape_url("http://" + webpage)
                except WebDriverException as e:
                    print("Exception occurred while scraping " + webpage + " Message: " + e.msg)
                    return None, "ERROR: " + e.msg

    def get_hyperlinks(self, webpage):
        links = set()
        try:
            anchors = self._driver.find_elements(By.TAG_NAME, 'a')
            for anchor in anchors:
                href = anchor.get_attribute('href')
                parsed_url = urlparse(href)

                if parsed_url.scheme not in ['http', 'https']:
                    continue

                if parsed_url.netloc not in [webpage, "www." + webpage]:
                    continue

                if parsed_url.path == '/':
                    continue

                # remove fragment
                clean_url = urlunparse(
                    (parsed_url.scheme, parsed_url.netloc, parsed_url.path, parsed_url.params, parsed_url.query, ''))

                links.add(clean_url)

            return links, None
        except Exception as e:
            print("Exception occurred while retrieving hyperlinks for " + webpage)
            return None, str(e)

    def _scrape_url(self, url):
        self._driver.get(url)

        wait = WebDriverWait(self._driver, 4)
        wait.until(expected_conditions.visibility_of_element_located((By.TAG_NAME, "body")))

        self._driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight || document.documentElement.scrollHeight);")

        wait.until(expected_conditions.visibility_of_element_located((By.TAG_NAME, "body")))

        time.sleep(1)

        body_text = self._driver.find_element(By.TAG_NAME, 'body').text

        return _remove_non_unicode_chars(body_text), None

    def cleanup(self):
        self._driver.quit()

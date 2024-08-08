from parser.config import logger
from parser.locators import ProductPageLocators

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

import json_data_manager.data_manager as dm

chrome_options = Options()
chrome_options.add_argument("--window-size=1920,1080")

driver = webdriver.Chrome(
    service=ChromeService(ChromeDriverManager().install()), options=chrome_options
)


wait = WebDriverWait(driver, timeout=3)


def price_parse():
    logger.info("========== New parse start ==========")
    data = dm.data_load()
    for url in data:
        driver.get(url)
        try:
            discount_price = (
                wait.until(
                    EC.visibility_of_element_located(ProductPageLocators.DISCOUNT_PRICE)
                )
                .text[:-1]
                .strip()
            )
            logger.info(f"Find discount_price: {discount_price}")
            if data[url] != discount_price:
                data[url] = discount_price
                logger.info("discount_price updated")
        except (NoSuchElementException, TimeoutException):
            logger.info("Didnt find discount_price")
            try:
                normal_price = (
                    wait.until(
                        EC.visibility_of_element_located(
                            ProductPageLocators.NORMAL_PRICE
                        )
                    )
                    .text[:-1]
                    .strip()
                )
                logger.info(f"Find normal_price: {normal_price}")
                if data[url] != normal_price:
                    data[url] = normal_price
                    logger.info("normal_price updated")
            except (NoSuchElementException, TimeoutException):
                logger.info(f"Any price not found for URL: {url}")
    dm.data_upload(data)
    driver.quit()
    logger.info("========== End parse ==========")


if __name__ == "__main__":
    price_parse()

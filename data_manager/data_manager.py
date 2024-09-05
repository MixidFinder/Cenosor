import json
import os

from aiogram.types import Message

from data_manager.config import logger

data_file = "data.json"


def init_data():
    if not os.path.exists(data_file):
        with open(data_file, "w") as f:
            json.dump({"products": {}}, f, indent=4)
            logger.info("Data json created.")
    logger.info("Data file exist.")


def load_data() -> dict:
    try:
        with open("data.json") as f:
            data = json.load(f)
        logger.info("Data loaded.")
        return data
    except FileNotFoundError:
        logger.info("File not found. Initializing.")
        init_data()
        return load_data()


def upload_data(data):
    with open("data.json", "w") as f:
        json.dump(data, f, indent=4)
    logger.info("Data uploaded.")


def check_url_in_data(url):
    data = load_data()
    if url in data["products"].keys():
        logger.info(f"URL: {url} in data file.")
        return True
    logger.info(f"URL: {url} not in data file.")
    return False


def add_product(url, track_price):
    data = load_data()
    data["products"][url] = {"current_price": "", "track_price": track_price}
    upload_data(data)
    logger.info(f"Added product - {url} - {track_price}")


def update_track_price(url, track_price):
    data = load_data()
    if check_url_in_data(url):
        data["products"][url]["track_price"] = track_price
        upload_data(data)
        logger.info(f"Update track_price: {track_price}, for URL: {url}")
        return True
    return False


def delete_product(url):
    data = load_data()
    if check_url_in_data(url):
        del data["products"][url]
        logger.info(f"Product {url} deleted")
        upload_data(data)
        return True
    return False


def print_products_url():
    data = load_data()
    urls = list(data["products"].keys())
    logger.info(f"Data printed: {urls}")
    return "\n\n".join(urls)


def extract_url(message: Message):
    if not message.entities:
        logger.info(f"{message.text} not a URL.")
        return False, ""
    for entity in message.entities:
        if entity.type in ["url", "text_link"]:
            logger.info(f"Found {message.text}")
            url = entity.extract_from(message.text)
            return True, url
    logger.info("Not found anything.")
    return False, ""


def print_all(data):
    msg = ""
    products = data["products"]
    for url, product in products.items():
        current_price = (
            product["current_price"] if product["current_price"] else "Цена не указана"
        )
        track_price = product["track_price"]

        msg += f"Ссылка: {url}\nТекущая цена: {current_price}\nЦена отслеживания: {track_price}\n\n"
    return msg

from selenium.webdriver.common.by import By


class ProductPageLocators:
    NORMAL_PRICE = (
        By.XPATH,
        "/html/body/div/div/div/main/article/div[1]/div[1]/form/div[2]/div[1]/div[1]/div",
    )
    DISCOUNT_PRICE = (
        By.XPATH,
        "/html/body/div/div/div/main/article/div[1]/div[1]/form/div[2]/div[1]/div[1]/div[1]",
    )


class MainPageLocators:
    ADDRESS_BTN = (
        By.XPATH,
        "/html/body/div/div/div/header/div[2]/div[1]/div/aside/div/div[2]/button[1]/span/span[1]",
    )

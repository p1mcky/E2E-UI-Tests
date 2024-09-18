from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def login(driver, username, password):
    """Авторизация на сайте."""
    driver.find_element(By.ID, 'user-name').send_keys(username)
    driver.find_element(By.ID, 'password').send_keys(password)
    driver.find_element(By.ID, 'login-button').click()


def select_product(driver, product_xpath):
    """Выбор продукта и добавление его в корзину."""
    driver.find_element(By.XPATH, product_xpath).click()
    driver.find_element(By.XPATH, '//*[@id="add-to-cart"]').click()


def go_to_cart(driver):
    """Переход в корзину."""
    driver.find_element(By.CLASS_NAME, 'shopping_cart_link').click()


def verify_product_in_cart(driver, product_name):
    """Проверка, что продукт добавлен в корзину."""
    driver.find_element(By.CLASS_NAME, 'shopping_cart_link').click()
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, f'//*[@class="inventory_item_name" and text()="{product_name}"]'))
    )
    cart_item = driver.find_element(By.XPATH, f'//*[@class="inventory_item_name" and text()="{product_name}"]')
    assert cart_item.text == product_name, 'The product was not added to the cart'


def checkout(driver, first_name, last_name, postal_code):
    """Оформление покупки."""
    driver.find_element(By.ID, 'checkout').click()
    driver.find_element(By.ID, 'first-name').send_keys(first_name)
    driver.find_element(By.ID, 'last-name').send_keys(last_name)
    driver.find_element(By.ID, 'postal-code').send_keys(postal_code)
    driver.find_element(By.ID, 'continue').click()
    driver.find_element(By.ID, 'finish').click()


def verify_order_confirmation(driver):
    """Проверка подтверждения покупки."""
    confirmation = driver.find_element(By.CLASS_NAME, 'complete-header').text
    assert confirmation == 'Thank you for your order!', 'The order was not confirmed'


def run_test():
    driver = webdriver.Chrome()

    try:
        driver.get('https://www.saucedemo.com/')

        # Авторизация
        login(driver, 'standard_user', 'secret_sauce')

        # Выбор товара и добавление в корзину
        select_product(driver, '//*[@id="item_4_title_link"]/div')

        # Проверка, что товар в корзине
        verify_product_in_cart(driver, 'Sauce Labs Backpack')

        # Оформление покупки
        checkout(driver, 'Kirill', 'Test', '123123')

        # Проверка подтверждения заказа
        verify_order_confirmation(driver)

    finally:
        driver.quit()


if __name__ == "__main__":
    run_test()

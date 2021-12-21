import lxml.html
from selenium import webdriver
from bs4 import BeautifulSoup
import requests, warnings
from dataclasses import dataclass
from settings import Country, reg_email_valid, email_valid, email_novalid, zip_code_novalid, zip_code_valid,\
    reg_email_invalid , password_valid, password_invalid, First_Name, Last_Name,\
    country_novalid, country_valid, region_valid, region_novalid
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import Select
import time

class Test():
    def __init__(self):
        self.url = "https://dropdead.world"
        self.option = webdriver.FirefoxOptions()
        self.list = ''
        #self.browser = None

    def start(self):
        self.option.add_argument("-incog#ito")
        #self.option.headless =True
        self.browser=webdriver.Firefox(executable_path="C:\\Users\\\Simon\\Desktop\\driver.exe", options=self.option)

    def get_content(self, url):
        soup = BeautifulSoup(requests.get(url).content, "html.parser")
        items = [div.a['href'] for div in soup.find_all('div', class_="pt-image-box")]
        return items[1:][0]

    #функции подсчета стоимости доставки
    def shipping_cost_calculation(self, country,
                                  region, zip_code, state):
        product = self.get_content("https://dropdead.world/collections/shop-all")
        url = self.url + product
        self.browser.get(url)
        time.sleep(1)
        xpath = {
            "xpath_textbox": "(//input[@id='address_zip'])[1]",
            "xpath_button": "//button[@class='btn btn-lg pt-btn-addtocart btn-addtocart addtocart-js']",
            "xpath_button_cal": "//button[normalize-space()='Calculate Shipping']",
            "xpath_dropbox_country": "//select[@id='address_country']",
            "xpath_dropbox_region": "//select[@id='address_province']"
        }
        button = self.browser.find_element_by_xpath(xpath["xpath_button"])
        button.click()
        url = self.url + "/cart"
        self.browser.get(url)
        time.sleep(5)
        dropbox_country = Select(self.browser.find_element_by_xpath(xpath["xpath_dropbox_country"]))
        # dropbox_country.select_by_visible_text(country)
        dropbox_country.select_by_index(country)
        time.sleep(3)
        if self.browser.find_element_by_xpath(xpath["xpath_dropbox_region"]):
            dropbox_region = Select(self.browser.find_element_by_xpath(xpath["xpath_dropbox_region"]))
            # dropbox_region.select_by_visible_text(region)
            try:
                dropbox_region.select_by_index(region)
            except:
                print('region ошибка номера')
                region = 1
                dropbox_region.select_by_index(region)
        # capcha = "//div[@id='g-recaptcha']"
        self.browser.find_element_by_xpath(xpath["xpath_textbox"]).send_keys(zip_code)
        button = self.browser.find_element_by_xpath(xpath["xpath_button_cal"])
        time.sleep(1)
        button.click()

    # Проверка функции подсчета стоимости доставки
    def test_shipping_cost_calculation_valid(self):
        self.shipping_cost_calculation(country=country_valid,
                                       region=region_valid,  zip_code=zip_code_valid, state=3)

    # Проверка функции подсчета стоимости доставки
    def test_shipping_cost_calculation_invalid(self):
        self.shipping_cost_calculation(country=country_novalid,
                                       region=region_novalid, zip_code=zip_code_novalid, state=3)

    def authorization(self, email, password):
        url = self.url + "/account/login?return_url=%2Faccount"
        self.browser.get(url)
        time.sleep(1)
        xpath = {
            "tb_Email": "//form[@id='customer_login']//input[@id='loginInputName']",
            "tb_Password": "//input[@id='loginInputEmail']",
            "btn_Login": "//button[normalize-space()='LOGIN']",
        }
        self.browser.find_element_by_xpath(xpath["tb_Email"]).send_keys(email)
        self.browser.find_element_by_xpath(xpath["tb_Password"]).send_keys(password)
        button = self.browser.find_element_by_xpath(xpath["btn_Login"])
        button.click()

    #Проверка функции авторизации
    def  test_authorization_validdata(self):
        self.authorization(email_valid, password_valid)

    #Проверка авторизации с невалидными данными
    def  test_authorization_invaliddata(self):
        self.authorization(email_novalid, password_invalid)

    #функции регистрации с валидными данными
    def  Registration(self, firstName,
                      lastName, email, password):
        url = self.url + "/account/register"
        self.browser.get(url)
        time.sleep(1)
        xpath = {
            "tb_FirstName": "(//input[@id='loginInputName'])[1]",
            "tb_LastName": "(//input[@id='loginLastName'])[1]",
            "tb_Email": "(//input[@id='loginInputEmail'])[1]",
            "tb_Password": "(//input[@id='loginInputPassword'])[1]",
            "btn_Create": "//button[normalize-space()='CREATE']",
        }
        self.browser.find_element_by_xpath(xpath["tb_FirstName"]).send_keys(firstName)
        self.browser.find_element_by_xpath(xpath["tb_LastName"]).send_keys(lastName)
        self.browser.find_element_by_xpath(xpath["tb_Email"]).send_keys(email)
        self.browser.find_element_by_xpath(xpath["tb_Password"]).send_keys(password)
        button = self.browser.find_element_by_xpath(xpath["btn_Create"])
        button.click()

    # Проверка функции регистрации с валидными данными
    def test_registration_valid_data(self):
        self.Registration(firstName=First_Name, lastName=Last_Name,
                          email=reg_email_valid, password=password_valid)

    #Проверка функции регистрации c невалидными данными
    def  test_registration_invalid_data(self):
        self.Registration(firstName=First_Name, lastName=Last_Name,
                          email=reg_email_invalid, password=password_invalid)


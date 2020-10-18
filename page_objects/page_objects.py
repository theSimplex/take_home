import configparser
from getpass import getpass, getuser

from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class BasePage:
    """
    As initial framework will be small, we can keep our objects in one place.
    When it'll grow we would start splitting it into some bussiness areas.
    """
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(10) #We implicitly wait for an object for up to 10 seconds and fail if not found.
        self.config = configparser.ConfigParser().read('config.ini')

class LoginPage(BasePage):
    def __init__(self):
        super(LoginPage, self).__init__()
        self.driver.get("https://facebook.com") #Likelyhood of this url changing is very low, I would just keep it hardcoded.
        self.email_field = self.driver.find_element_by_id("email") #as we grow, I would recommend extracting all selectors into a separate file so we can reuse them.
        self.password_field = self.driver.find_element_by_id("pass")
        self.login_btn = self.driver.find_element_by_xpath("//*[@id=\"u_0_b\"]")
        
    def login(self, user=None, password=None): #Its possible to login with custom credentials, but we would use values from the config file.
        user = user if user else self.config['CREDENTIALS']['User'] 
        password = password if password else self.config['CREDENTIALS']['Password'] 
        self.email_field.send_keys(user)
        self.password_field.send_keys(password)
        self.login_btn.click()
        return self.driver #I would return driver in most methods, so the test creator can do additional checks in place.
        
class Search(BasePage): #Object where we combine search bar and search results.
    def __init__(self):
        super(Search, self).__init__()
        self.search_field = self.driver.find_element_by_css_selector("div[aria-label='Search Facebook']")
        
    def search(self, text):
        self.search_field.send_keys(text)
        self.search_field.send_keys(Keys.RETURN)
        self.result = self.driver.find_element_by_link_text(text)
        return self.driver
        
    def open(self):
        self.result.click()
        return self.driver
        
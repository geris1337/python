#4. Dresses -> Summer dress table content check and filter tests
# Note: could not test filters since website does not return any results!
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import pytest

@pytest.fixture(scope="module", autouse=True)
def open_browser():
    global driver
    driver = webdriver.Firefox()
    yield
    driver.quit()

def test_product_content():

    global number_of_products, urls

    number_of_products = 0
    urls = ()

    driver.get("http://automationpractice.com")

    #Click on Dresses
    WebDriverWait(driver,30).until(lambda d: d.find_element_by_xpath("/html/body/div/div[1]/header/div[3]/div/div/div[6]/ul/li[2]/a")).click()

    #Click on specific element that has text Summer Dresses
    WebDriverWait(driver,30).until(lambda d: d.find_elements_by_xpath("//a[contains(text(), 'Summer Dresses')]")[2]).click()

    elements = driver.find_elements_by_xpath("//a[@class='product_img_link']")
    
    #Get urls of all products
    for element in elements:
        #print ("\nProduct: " + element.get_attribute('title'))
        number_of_products += 1
        urls += tuple(str(element.get_attribute('href')).split())

    print("\nTotal number of Products: " + str(number_of_products))

    #Get content of each product
    for url in urls:
        driver.get(url)
        print("--------------------------------------------------------------------------------")

        name = driver.find_element_by_xpath("//h1[@itemprop='name']").text
        print("Product: " + name)
        model = driver.find_element_by_xpath("//span[@class='editable']").text
        print("Model: " + model)
        condition = driver.find_elements_by_xpath("//span[@class='editable']")[1].text
        print("Condition: " + condition)
        description = driver.find_element_by_xpath("//div[@itemprop='description']").text
        print("Description: " + description)
        
        old_price = driver.find_element_by_xpath("//*[@id='old_price_display']").text
        reduction_percent = driver.find_element_by_xpath("//*[@id='reduction_percent']").text

        if old_price != "":
            print("Old price: " + old_price)
            print("Discount: " + reduction_percent)

        current_price = driver.find_element_by_xpath("//*[@id='our_price_display']").text
        print("Current price: " + current_price)
        
        colors = driver.find_elements_by_xpath("//a[contains(@class, 'color_')]")

        for color in colors:
            print("Available in: " + color.get_attribute('title'))
            
        table_id = driver.find_element(By.CLASS_NAME, 'table-data-sheet')

        # Get all rows in the table
        rows = table_id.find_elements(By.TAG_NAME, "tr") 
        for row in rows:
            col1 = row.find_elements(By.TAG_NAME, "td")[0].text
            col2 = row.find_elements(By.TAG_NAME, "td")[1].text
            print (col1 + ": " + col2)
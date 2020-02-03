# 5. Buy 3 random products and go full purchase flow
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
import pytest, random, urllib.request, json

@pytest.fixture(scope="module", autouse=True)
def open_browser():
    global driver
    driver = webdriver.Firefox()
    yield
    driver.quit()

def prepare_data():
    global data, item, counter_tuple, i

    with urllib.request.urlopen("https://www.dropbox.com/s/rk03614zy31un0y/users.json?raw=1") as url:
        data = json.loads(url.read().decode())

    counter_tuple = ()
    item = 0
    
    for i in data:
        counter_tuple += tuple(str(item).split())
        item+=1

    return counter_tuple


def test_random_purchase_auth_summary():

    global number_of_products, iteration, urls
    number_of_products = 0
    iteration = 0
    urls = ()

    driver.get("http://automationpractice.com")
    
    elements = driver.find_elements_by_xpath("//a[@class='product_img_link']")

    #Get urls of all products
    for element in elements:
        number_of_products += 1
        urls += tuple(str(element.get_attribute('href')).split())

    #Remove duplicates
    my_set = set(urls)

    #Shuffle the tuple
    l = list(my_set)
    random.shuffle(l)
    for x in l:
        
        #Select only 3 product urls
        if iteration == 3:
            break

        driver.get(x)

        WebDriverWait(driver,10).until(lambda d: d.find_element_by_id("add_to_cart")).click()
        WebDriverWait(driver,10).until(lambda d: d.find_element_by_xpath("//*[@id='layer_cart']").is_displayed())

        #Iterating loop
        iteration += 1

    #First proceed button
    WebDriverWait(driver,10).until(lambda d: d.find_element_by_xpath("//*[@title='Proceed to checkout']")).click()
    #Second proceed button
    WebDriverWait(driver,10).until(lambda d: d.find_elements_by_xpath("//*[@title='Proceed to checkout']")[1]).click()

    print("\nCart order summary complete!")

@pytest.mark.parametrize('counter', prepare_data())
def test_random_purchase_auth_signin(counter):
    print("\n--------------------------------------------------------------------------------")
    print("\nSelected JSON element: " + str(counter) + " | Account under test: " + data[int(counter)]['email'])

    #Attempt to login only JSON registered status accounts
    if data[int(counter)]['id_email_status'] == "registered":
    
        WebDriverWait(driver,30).until(lambda d: d.find_element_by_id("email")).clear()
        WebDriverWait(driver,30).until(lambda d: d.find_element_by_id("email")).send_keys(data[int(counter)]['email'])

        WebDriverWait(driver,30).until(lambda d: d.find_element_by_id("passwd")).clear()
        WebDriverWait(driver,30).until(lambda d: d.find_element_by_id("passwd")).send_keys(data[int(counter)]['password'])

        WebDriverWait(driver,30).until(lambda d: d.find_element_by_id("SubmitLogin")).click()

        try:
            WebDriverWait(driver,5).until(lambda d: d.find_element_by_xpath("//*[contains(text(), 'Sign out')]"))
            print("Login successful!")
        except TimeoutException:
            alert = WebDriverWait(driver,5).until(lambda d: d.find_element_by_xpath("/html/body/div/div[2]/div/div[3]/div/div[1]")).text
            print(alert)
            pytest.xfail("Login unsuccessful!")

    else:
        print("JSON data says this is unregistered. Therefore skipping.")
        pytest.skip("Skipping test for test data iteration.")

def test_random_purchase_auth_address():
    WebDriverWait(driver,10).until(lambda d: d.find_element_by_xpath("//*[@name='processAddress']")).click()
    print("\nAddress processed!")

def test_random_purchase_auth_shipping():
    WebDriverWait(driver,10).until(lambda d: d.find_element_by_xpath("//*[@id='cgv']")).click()

    WebDriverWait(driver,10).until(lambda d: d.find_element_by_xpath("//*[@name='processCarrier']")).click()
    print("\nShipping confirmed!")

def test_random_purchase_auth_payment():
    WebDriverWait(driver,10).until(lambda d: d.find_element_by_xpath("//*[@class='bankwire']")).click()
    print("\nBankwire payment selected!")
    WebDriverWait(driver,10).until(lambda d: d.find_element_by_xpath("//*[@class='button btn btn-default button-medium']")).click()
    print("\nPurchase confirmed")
    info = WebDriverWait(driver,10).until(lambda d: d.find_element_by_xpath("//*[@class='box']")).text
    print(info)
    print("\nOrder completed!")
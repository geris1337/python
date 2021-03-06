# 3. Login without GUI
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import TimeoutException
import pytest, urllib.request, json

@pytest.fixture(scope="module", autouse=True)
def open_browser():
    global driver
    options = Options()

    #Set to False if you want GUI
    options.headless = True

    driver = webdriver.Firefox(options=options)
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

@pytest.mark.parametrize('counter', prepare_data())
def test_login_headless(counter):
    print("\n--------------------------------------------------------------------------------")
    print("\nSelected JSON element: " + str(counter) + " | Account under test: " + data[int(counter)]['email'])
    
    #Attempt to login only JSON registered status accounts
    if data[int(counter)]['id_email_status'] == "registered":
        driver.get("http://automationpractice.com")
        
        WebDriverWait(driver,30).until(lambda d: d.find_element_by_xpath("//*[contains(text(), 'Sign in')]")).click()
        WebDriverWait(driver,30).until(lambda d: d.find_element_by_id("email")).send_keys(data[int(counter)]['email'])
        WebDriverWait(driver,30).until(lambda d: d.find_element_by_id("passwd")).send_keys(data[int(counter)]['password'])
        WebDriverWait(driver,30).until(lambda d: d.find_element_by_id("SubmitLogin")).click()

        try:
            WebDriverWait(driver,5).until(lambda d: d.find_element_by_xpath("//*[contains(text(), 'Sign out')]")).click()
            print("Login successful!")
        except TimeoutException:
            alert = WebDriverWait(driver,5).until(lambda d: d.find_element_by_xpath("/html/body/div/div[2]/div/div[3]/div/div[1]")).text
            print(alert)
            pytest.xfail("Login unsuccessful!")

    else:
        print("JSON data says this is unregistered. Therefore skipping.")
        pytest.skip("Skipping test for test data iteration.")
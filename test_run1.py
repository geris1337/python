# 1. Register flow with validation check (using external file for test data)
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
import urllib.request, json 
import pytest

def firstname(fullname):
	return fullname.strip().split(' ')[0]

def lastname(fullname):
	return ' '.join((fullname + ' ').split(' ')[1:]).strip()

@pytest.fixture(scope="module", autouse=True)
def open_browser():
	global driver
	driver = webdriver.Firefox()
	yield
	driver.quit()

def prepare_data():

	with urllib.request.urlopen("https://www.dropbox.com/s/rk03614zy31un0y/users.json?raw=1") as url:
		global data
		data = json.loads(url.read().decode())

	global item, counter_tuple, i
	item = 0
	counter_tuple = ()

	for i in data:
		counter_tuple += tuple(str(item).split())
		item+=1

	return counter_tuple

@pytest.mark.parametrize('counter', prepare_data())
def test_email_validation(counter):
	print("\n--------------------------------------------------------------------------------")
	print("\nSelected JSON element: " + str(counter) + " | Account under test: " + data[int(counter)]['email'])

	driver.get("http://automationpractice.com")
	WebDriverWait(driver,30).until(lambda d: d.find_element_by_class_name("login")).click()
	WebDriverWait(driver,30).until(lambda d: d.find_element_by_id("email_create")).send_keys(data[int(counter)]['email'])
	WebDriverWait(driver,30).until(lambda d: d.find_element_by_id("SubmitCreate")).click()

	try:
		alert = WebDriverWait(driver,10).until(lambda d: d.find_element_by_xpath("/html/body/div/div[2]/div/div[3]/div/div/div[1]/form/div/div[1]/ol/li")).text
		if alert == "An account using this email address has already been registered. Please enter a valid password or request a new one.":
			print("\nAccount already registered!")
			
			if (data[int(counter)]['id_email_status'] == "unregistered") and (data[int(counter)]['id_data_status'] == "invalid"):
				print("\nDouble check JSON, this might be a bug")
				pytest.xfail("This test data iteration should have an unregistered email")

		elif  alert == "Invalid email address.":
			print("\nInvalid email address!")

			if data[int(counter)]['id_data_status'] == "valid":
				print("Double check JSON, this might be a bug")
				pytest.xfail("This test data iteration should have a valid email format")

	except TimeoutException:
		try:
			WebDriverWait(driver,10).until(lambda d: d.find_element_by_id("submitAccount")).is_displayed()
			print("\nEmail is valid. Form loaded")
		except TimeoutException:
			print("Something unexpected happened! Please investigte timeout!")
			pytest.xfail("Something unexpected happened")

@pytest.mark.parametrize('counter', prepare_data())
def test_registration_validation(counter):
	print("\n--------------------------------------------------------------------------------")
	print("\nSelected JSON element: " + str(counter) + " | Account under test: " + data[int(counter)]['email'])

	if data[int(counter)]['id_email_status'] == 'unregistered':
		driver.get("http://automationpractice.com")
		WebDriverWait(driver,30).until(lambda d: d.find_element_by_class_name("login")).click()
		WebDriverWait(driver,30).until(lambda d: d.find_element_by_id("email_create")).send_keys(data[int(counter)]['email'])
		WebDriverWait(driver,30).until(lambda d: d.find_element_by_id("SubmitCreate")).click()

		try:
			# Waiting for form to load
			WebDriverWait(driver,10).until(lambda d: d.find_element_by_id("submitAccount")).is_displayed()

			if data[int(counter)]['gender'] == "male":
				WebDriverWait(driver,30).until(lambda d: d.find_element_by_xpath("//*[@id='id_gender1']")).click()
			elif data[int(counter)]['gender'] == "female":
				WebDriverWait(driver,30).until(lambda d: d.find_element_by_xpath("//*[@id='id_gender2']")).click()

			WebDriverWait(driver,30).until(lambda d: d.find_element_by_id("customer_firstname")).send_keys(firstname(data[int(counter)]['name']))
			WebDriverWait(driver,30).until(lambda d: d.find_element_by_id("customer_lastname")).send_keys(lastname(data[int(counter)]['name']))
			WebDriverWait(driver,30).until(lambda d: d.find_element_by_id("passwd")).send_keys(data[int(counter)]['password'])

			Select(WebDriverWait(driver,30).until(lambda d: d.find_element_by_xpath("//select[@name='days']"))).select_by_value(str(int(data[int(counter)]['birthday'].split('-')[2])))
			Select(WebDriverWait(driver,30).until(lambda d: d.find_element_by_xpath("//select[@name='months']"))).select_by_value(str(int(data[int(counter)]['birthday'].split('-')[1])))
			Select(WebDriverWait(driver,30).until(lambda d: d.find_element_by_xpath("//select[@name='years']"))).select_by_value(str(int(data[int(counter)]['birthday'].split('-')[0])))
		
			WebDriverWait(driver,30).until(lambda d: d.find_element_by_xpath("//*[@id='newsletter']")).click()
			WebDriverWait(driver,30).until(lambda d: d.find_element_by_xpath("//*[@id='optin']")).click()

			WebDriverWait(driver,30).until(lambda d: d.find_element_by_id("company")).send_keys(data[int(counter)]['company']['name'])
			WebDriverWait(driver,30).until(lambda d: d.find_element_by_id("address1")).send_keys(data[int(counter)]['address']['street'])
			WebDriverWait(driver,30).until(lambda d: d.find_element_by_id("address2")).send_keys(data[int(counter)]['address']['suite'])
			WebDriverWait(driver,30).until(lambda d: d.find_element_by_id("city")).send_keys(data[int(counter)]['address']['city'])
		
			Select(WebDriverWait(driver,30).until(lambda d: d.find_element_by_xpath("//*[@id='id_state']"))).select_by_visible_text(data[int(counter)]['address']['state'])
		
			WebDriverWait(driver,30).until(lambda d: d.find_element_by_id("postcode")).send_keys(data[int(counter)]['address']['zipcode'])

			Select(WebDriverWait(driver,30).until(lambda d: d.find_element_by_xpath("//*[@id='id_country']"))).select_by_visible_text(data[int(counter)]['address']['country'])

			WebDriverWait(driver,30).until(lambda d: d.find_element_by_id("other")).send_keys(data[int(counter)]['company']['catchPhrase'])
			WebDriverWait(driver,30).until(lambda d: d.find_element_by_id("phone")).send_keys(data[int(counter)]['phone'])
			WebDriverWait(driver,30).until(lambda d: d.find_element_by_id("phone_mobile")).send_keys(data[int(counter)]['phone'])
			WebDriverWait(driver,30).until(lambda d: d.find_element_by_id("alias")).clear()
			WebDriverWait(driver,30).until(lambda d: d.find_element_by_id("alias")).send_keys(data[int(counter)]['website'])

			WebDriverWait(driver,30).until(lambda d: d.find_element_by_id("submitAccount")).click()
		
			alert = WebDriverWait(driver,30).until(lambda d: d.find_element_by_xpath("/html/body/div/div[2]/div/div[3]/div/div")).text
		
			if alert == "ORDER HISTORY AND DETAILS\nMY CREDIT SLIPS\nMY ADDRESSES\nMY PERSONAL INFORMATION\nMY WISHLISTS":
				print("Account has been registered")
				#Logout if registered
				WebDriverWait(driver,30).until(lambda d: d.find_element_by_xpath("//*[contains(text(), 'Sign out')]")).click()
			else:
				print(alert)

		except TimeoutException:
			alert = WebDriverWait(driver,10).until(lambda d: d.find_element_by_xpath("/html/body/div/div[2]/div/div[3]/div/div/div[1]/form/div/div[1]/ol/li")).text	

			if alert == "An account using this email address has already been registered. Please enter a valid password or request a new one.":
				print("\nAccount already registered")
				print("\nDouble check JSON, this might be a bug!!!")
				pytest.xfail("Account is already registered. Please update JSON file, test data must have unregistered email")

			elif alert == "Invalid email address.":
				print("\nInvalid email address!!!")
				pytest.xfail("Invalid email address")

		except TimeoutException:
			print("Something unexpected happened! Please investigte timeout!")
			pytest.xfail("Something unexpected happened")
	
	else:
		print("JSON data says this is registered. Therefore skipping.")
		pytest.skip("Skipping test for test data iteration.")

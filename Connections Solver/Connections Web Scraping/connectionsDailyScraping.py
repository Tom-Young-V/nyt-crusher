from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup


def getDailyPuzzle(printGet = False):

	# Set up the Chrome options
	chrome_options = Options()
	chrome_options.add_argument("--headless")  # Run Chrome in headless mode (without GUI)

	# Set up the ChromeDriver with the specified options
	driver = webdriver.Chrome(options=chrome_options)

	# Navigate to the website
	url = "https://www.nytimes.com/games/connections"
	driver.get(url)

	# Wait for the dynamic element with class "Board-module_cardsContainer__mJ2tA Board-module_cardsContainer4__LPTzh" to be present
	# try:
	# 	dynamic_element = WebDriverWait(driver, 10).until(
    #         EC.presence_of_element_located((By.CLASS_NAME, "Cards-module_cardsContainer__O3T5q Cards-module_cardsContainer4__sK7TL"))
	# 	)

	# 	# Get the page source after JavaScript has run
	# 	html_source = driver.page_source

	# finally:
	# 	# Close the browser
	# 	driver.quit()

	html_source = driver.page_source

	# Parse the HTML source using BeautifulSoup
	soup = BeautifulSoup(html_source, "html.parser")

	# Find tags with the specified class and data attributes
	targetCode = soup.find("div", class_ = "Cards-module_cardsContainer__O3T5q Cards-module_cardsContainer4__sK7TL")

	values = [label.text for label in targetCode.find_all("label")]

	if printGet:
		if values:
			print("Found cards")
		else:
			print("Failed")
			return False

	return values

if __name__ == "__main__":
	print(getDailyPuzzle())











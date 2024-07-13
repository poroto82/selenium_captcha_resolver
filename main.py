import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from twocaptcha import TwoCaptcha
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def initialize_driver():
    """Initialize the Selenium WebDriver."""
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run in headless mode if needed
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    return driver

def get_sitekey(driver):
    """Retrieve the sitekey for the reCAPTCHA."""
    recaptcha_element = driver.find_element(By.CLASS_NAME, 'g-recaptcha')
    sitekey = recaptcha_element.get_attribute('data-sitekey')
    return sitekey

def solve_captcha(solver, sitekey, url):
    """Solve the reCAPTCHA using 2Captcha."""
    response = solver.recaptcha(sitekey=sitekey, url=url)
    return response['code']

def main():
    captcha_page_url = "https://2captcha.com/demo/recaptcha-v2"
    api_key = os.getenv("TWOCAPTCHA_API_KEY")

    if not api_key:
        logger.error("2Captcha API key not found in environment variables.")
        return

    driver = initialize_driver()

    try:
        driver.get(captcha_page_url)
        logger.info("Page loaded successfully")

        # Wait until the reCAPTCHA element is present
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'g-recaptcha')))

        sitekey = get_sitekey(driver)
        logger.info(f"Sitekey obtained: {sitekey}")

        solver = TwoCaptcha(api_key)
        logger.info("Solving Captcha")
        code = solve_captcha(solver, sitekey, captcha_page_url)
        logger.info(f"Successfully solved the Captcha. The solve code is {code}")

        # Set the solved Captcha
        recaptcha_response_element = driver.find_element(By.ID, 'g-recaptcha-response')
        driver.execute_script(f'arguments[0].value = "{code}";', recaptcha_response_element)

        # Submit the form
        submit_btn = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        submit_btn.click()
        logger.info("Form submitted successfully")

        # Pause the execution to observe the result
        time.sleep(5)

    except Exception as e:
        logger.error(f"An error occurred: {e}")

    finally:
        driver.quit()
        logger.info("Driver closed")

if __name__ == "__main__":
    main()

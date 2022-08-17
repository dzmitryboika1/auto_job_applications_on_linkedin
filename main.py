from dotenv import load_dotenv
import os
import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def authorization(driver):
    """ authorization"""
    driver.implicitly_wait(5)
    sign_in_button = driver.find_element(By.CLASS_NAME, "btn-secondary-emphasis")
    # click to sing in button
    sign_in_button.click()

    driver.implicitly_wait(5)
    email_field = driver.find_element(By.ID, "username")
    # enter login
    email_field.send_keys(os.getenv("LOGIN"))

    password_field = driver.find_element(By.ID, "password")
    # enter password
    password_field.send_keys(os.getenv("PASSWORD"))

    submit_button = driver.find_element(By.CLASS_NAME, "from__button--floating")
    # click submit button
    submit_button.click()


def apply_for_one_item(driver):
    """func applies for job if it's one-step application and ignores the complex multi-steps applications"""
    ignored_exceptions = (NoSuchElementException, StaleElementReferenceException,)
    try:
        driver.implicitly_wait(10)
        apply_button = driver.find_element(By.CLASS_NAME, "jobs-apply-button--top-card")
        apply_button.click()
    except ignored_exceptions:
        pass
    else:
        ignored_exceptions = (NoSuchElementException, StaleElementReferenceException,)
        submit_button = WebDriverWait(driver, 30, ignored_exceptions=ignored_exceptions).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "footer button")))

        if submit_button.get_attribute("aria-label") == "Перейти к следующему шагу":
            close_button = driver.find_element(By.CLASS_NAME, "artdeco-modal__dismiss")
            close_button.click()
            driver.implicitly_wait(5)
            discard_button = driver.find_elements(By.CLASS_NAME, "artdeco-modal__confirm-dialog-btn")[1]
            discard_button.click()
            print("Complex application, skipped.")
        else:
            submit_button.click()
            print("Success")


def apply_loop(driver):
    """function automatically goes through all job apply items from first page"""
    i = 0
    jobs_side_bar = None
    try:
        while True:
            jobs_side_bar = WebDriverWait(driver, 20).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".job-card-container--clickable")))
            # scroll down
            driver.execute_script("arguments[0].scrollIntoView(true);", jobs_side_bar[i])
            i += 1
    except:
        pass

    for job in jobs_side_bar:
        driver.execute_script("arguments[0].click();", job)
        apply_for_one_item(driver)


def main():
    """ main function"""
    load_dotenv()
    chrome_driver_path = "/usr/lib/chromium-browser/chromedriver"
    linkedin_search_url = "https://www.linkedin.com/jobs/search/?currentJobId=3216390023&f_LF=f_AL&geoId=102974008&keywords=python%20developer&location=%D0%AD%D1%81%D1%82%D0%BE%D0%BD%D0%B8%D1%8F&refresh=true"
    driver = webdriver.Chrome(executable_path=chrome_driver_path)
    driver.get(linkedin_search_url)

    authorization(driver)
    apply_loop(driver)
    time.sleep(1000)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

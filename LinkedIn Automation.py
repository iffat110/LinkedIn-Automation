from datetime import datetime
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import selenium.common.exceptions as exceptions
import time
import pandas as pd

def ll_login(email, password):
    linkedin_username = email
    linkedin_password = password

    global driver
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    options.add_experimental_option("detach", True)

    try:
        driver = webdriver.Chrome(options=options)
    except exceptions.WebDriverException:
        print("Get a newer version of driver!")
        return False

    try:
        driver.get("https://www.linkedin.com/login")
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "username"))).send_keys(linkedin_username)
        driver.find_element(By.ID, "password").send_keys(linkedin_password)
        driver.find_element(By.XPATH, "//button[contains(text(),'Sign in')]").click()

        # Handle OTP if required
        try:
            otp_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "input.form__input--text.input_verification_pin")))
            otp = input("OTP: ")
            otp_element.send_keys(otp)
            driver.find_element(By.CSS_SELECTOR, "button.form__submit.form__submit--stretch").click()
        except exceptions.TimeoutException:
            print("No OTP Required")

        return True
    except ImportError:
        print("Closing Program!")
        return False

def send_connection_request(first_name, full_name, message):
    try:
        print(f"Trying to send connection request to {full_name}")
        # Locate the connect button
        connect_button = driver.find_element(By.XPATH, f"//button[contains(@aria-label, 'Invite {full_name.strip()} to connect')]")
        ActionChains(driver).move_to_element(connect_button).click().perform()
        time.sleep(1)
        try:
            note_button = driver.find_element(By.XPATH, '//button[@aria-label="Add a note"]')
            note_button.click()
            note_input = driver.find_element(By.XPATH, '//textarea[@name="message"]')
            note_input.send_keys(message.format(first_name=first_name))
            send_button = driver.find_element(By.XPATH, '//button[@aria-label="Send now"]')
            send_button.click()
            print(f"Connection request sent with note to {full_name}")
        except exceptions.NoSuchElementException:
            send_button = driver.find_element(By.XPATH, '//button[@aria-label="Send now"]')
            send_button.click()
            print(f"Connection request sent without note to {full_name}")
        return True
    except exceptions.NoSuchElementException:
        print("Connect button not found in the main section.")
        return False

def send_connection_request_from_more_menu(first_name, full_name, message):
    try:
        print(f"Trying to send connection request from 'More' menu to {full_name}")
        # Open the More menu
        more_button = driver.find_element(By.XPATH, "//button[contains(@aria-label, 'More actions')]")
        ActionChains(driver).move_to_element(more_button).click().perform()
        time.sleep(1)
        # Locate the connect button within the More menu
        connect_button = driver.find_element(By.XPATH, f"//div[contains(@aria-label, 'Invite {full_name.strip()} to connect')]")
        ActionChains(driver).move_to_element(connect_button).click().perform()
        time.sleep(1)
        try:
            note_button = driver.find_element(By.XPATH, '//button[@aria-label="Add a note"]')
            note_button.click()
            note_input = driver.find_element(By.XPATH, '//textarea[@name="message"]')
            note_input.send_keys(message.format(first_name=first_name))
            send_button = driver.find_element(By.XPATH, '//button[@aria-label="Send now"]')
            send_button.click()
            print(f"Connection request sent with note to {full_name}")
        except exceptions.NoSuchElementException:
            send_button = driver.find_element(By.XPATH, '//button[@aria-label="Send now"]')
            send_button.click()
            print(f"Connection request sent without note to {full_name}")
        return True
    except exceptions.NoSuchElementException:
        print("Connect button not found in the 'More' menu.")
        return False

def search_and_connect(email, password, urls):
    start_time = datetime.now()
    start_time_string = start_time.strftime("%d/%m/%Y %H:%M:%S")

    if not ll_login(email, password):
        return

    url_not_connected = []

    for url in urls:
        try:
            driver.get(url)
            time.sleep(6)
            full_name = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "h1.text-heading-xlarge.inline.t-24.v-align-middle.break-words"))).text
            first_name = full_name.split()[0]

            # Attempt to send a message if already connected
            try:
                message_button = driver.find_element(By.XPATH, "//a[contains(text(),'Message')]")
                message_button.click()
                message_box = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@role='textbox']")))
                message_box.send_keys(f"Hello {first_name},\nI would like to connect with you" + Keys.ENTER)
                continue
            except exceptions.NoSuchElementException:
                print(f"{full_name} is not already connected. Attempting to send connection request.")

            # Try to send connection request
            if not send_connection_request(first_name, full_name, message):
                # If connect button not found, try from More menu
                if not send_connection_request_from_more_menu(first_name, full_name, message):
                    url_not_connected.append(url)
                    continue

        except exceptions.NoSuchElementException as e:
            print(f"Error processing {url}: {e}")
            url_not_connected.append(url)
            continue

    if url_not_connected:
        df = pd.DataFrame({'URL': url_not_connected})
        df.to_csv("not_connected.csv")

    end_time = datetime.now()
    end_time_string = end_time.strftime("%d/%m/%Y %H:%M:%S")
    print("Start Date and Time =", start_time_string)
    print("End Date and Time =", end_time_string)
    
if __name__ == "__main__":
    email = 'maziya.iffat@yahoo.com'
    password = '**********'
    urls = [
        "https://br.linkedin.com/in/vinicius-marconi-691b52100",
        "https://ae.linkedin.com/in/syed-attaullah-159878229",
        "https://br.linkedin.com/in/daniel-neves-2287a192",
        "https://co.linkedin.com/in/michell-alejandra-avila-tafur-53413b199",
        "https://ph.linkedin.com/in/edgarico-llaneta-a42b0996"
    ]
    message = "Hello {first_name},\nI would like to connect with you"
    search_and_connect(email, password, urls)

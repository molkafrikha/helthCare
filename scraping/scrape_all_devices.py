import json

# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.options import Options
# from webdriver_manager.chrome import ChromeDriverManager
# import time
#
#
# def get_driver():
#     options = Options()
#     options.add_argument('--headless')
#     options.add_argument('--no-sandbox')
#     options.add_argument('--disable-dev-shm-usage')
#     options.add_argument(
#         'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36')
#     driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
#     return driver
#
#
# def get_device_specs(driver, link):
#     driver.get(link)
#     time.sleep(3)  # Increase the sleep time to ensure the page loads fully
#
#     # Extract device name
#     try:
#         device_name = driver.find_element(By.CSS_SELECTOR, 'h1.aps-main-title').text
#     except:
#         device_name = 'Unknown'
#
#     # Extract manufacturer
#     try:
#         manufacturer = driver.find_element(By.CSS_SELECTOR, '.aps-product-brand span[itemprop="brand"]').text
#     except:
#         manufacturer = 'Unknown'
#
#     rear_camera_specs = {}
#     front_camera_specs = {}
#
#     try:
#         camera_section = driver.find_element(By.XPATH, "//h3[contains(text(), 'Camera')]")
#         specs_list = camera_section.find_elements(By.XPATH, "..//ul[@class='aps-specs-list']/li")
#
#         for spec in specs_list:
#             title = spec.find_element(By.CSS_SELECTOR, 'div.aps-attr-title strong').text
#             value = spec.find_element(By.CSS_SELECTOR, 'div.aps-attr-value span').text
#
#             if 'Rear Camera' in title:
#                 rear_camera_specs['resolution'] = value
#             elif 'Front Camera' in title:
#                 front_camera_specs['resolution'] = value
#     except Exception as e:
#         rear_camera_specs['resolution'] = 'N/A'
#         front_camera_specs['resolution'] = 'N/A'
#
#     # Extract operating system
#     try:
#         os_section = driver.find_element(By.XPATH,
#                                          "//strong[text()='Operating System']/ancestor::div[@class='aps-attr-title']/following-sibling::div/span")
#         os = os_section.text
#     except:
#         os = 'N/A'
#
#     return {
#         'device_name': device_name,
#         'manufacturer': manufacturer,
#         'rear_camera': rear_camera_specs,
#         'front_camera': front_camera_specs,
#         'operating_system': os
#     }
#
#
# def scrape_device_links(driver, page_url):
#     driver.get(page_url)
#     time.sleep(3)  # Allow the page to load completely
#     device_links = [element.get_attribute('href') for element in
#                     driver.find_elements(By.CSS_SELECTOR, '.aps-product-box .aps-product-thumb a')]
#     return device_links
#
#
# def main():
#     base_url = "https://www.gizmochina.com/cat/mobiles"
#     driver = get_driver()
#     driver.get(base_url)
#     all_device_links = []
#
#     page_number = 1
#
#     while page_number <= 293:  # Specify the total number of pages
#         # print(f"Scraping page {page_number}")
#         page_url = f"{base_url}/page/{page_number}"
#         # print(page_url)
#         device_links = scrape_device_links(driver, page_url)
#         # print(device_links)
#         if not device_links:
#             break
#         all_device_links.extend(device_links)
#         page_number += 1
#
#     all_device_specs = []
#     for link in all_device_links:
#         specs = get_device_specs(driver, link)
#         # Filter out devices without camera specs
#         if specs['rear_camera'].get('resolution', 'N/A') != 'N/A' or specs['front_camera'].get('resolution','N/A') != 'N/A':
#             print(specs)
#             all_device_specs.append(specs)
#             # print(f"Scraped data for {specs['device_name']}")
#     driver.quit()
#     # return all_device_specs
#     # with open('/home/imen/mobicrowd/Mobicrowd_backend/camera_specs1-293.json', 'w') as file:
#     #     for device_spec in all_device_specs:
#     #         json.dump(device_spec, file)
#     #         file.write('\n')
#
#
# if __name__ == "__main__":
#     device_specs = main()
import json
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def get_driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument(
        'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver



def scrape_device_links(driver, page_url):
    driver.get(page_url)
    try:
        # Wait for the device links to be present
        WebDriverWait(driver, 40).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.aps-product-box .aps-product-thumb a'))
        )
    except TimeoutException:
        print(f"Timeout while waiting for device links on {page_url}")
        return []

    device_links = [element.get_attribute('href') for element in
                    driver.find_elements(By.CSS_SELECTOR, '.aps-product-box .aps-product-thumb a')]
    return device_links

def get_device_specs(driver, link):
    driver.get(link)
    try:
        # Wait for the device name element to be present
        WebDriverWait(driver, 40).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'h1.aps-main-title'))
        )
    except TimeoutException:
        print(f"Timeout while waiting for device specs on {link}")
        return {'device_name': 'Unknown', 'manufacturer': 'Unknown', 'rear_camera': {}, 'front_camera': {}, 'operating_system': 'N/A'}

    # Extract device name
    try:
        device_name = driver.find_element(By.CSS_SELECTOR, 'h1.aps-main-title').text
    except:
        device_name = 'Unknown'

    # Extract manufacturer
    try:
        manufacturer = driver.find_element(By.CSS_SELECTOR, '.aps-product-brand span[itemprop="brand"]').text
    except:
        manufacturer = 'Unknown'

    rear_camera_specs = {}
    front_camera_specs = {}

    try:
        camera_section = driver.find_element(By.XPATH, "//h3[contains(text(), 'Camera')]")
        specs_list = camera_section.find_elements(By.XPATH, "..//ul[@class='aps-specs-list']/li")

        for spec in specs_list:
            title = spec.find_element(By.CSS_SELECTOR, 'div.aps-attr-title strong').text
            value = spec.find_element(By.CSS_SELECTOR, 'div.aps-attr-value span').text

            if 'Rear Camera' in title:
                rear_camera_specs['resolution'] = value
            elif 'Front Camera' in title:
                front_camera_specs['resolution'] = value
    except Exception as e:
        rear_camera_specs['resolution'] = 'N/A'
        front_camera_specs['resolution'] = 'N/A'

    # Extract operating system
    try:
        os_section = driver.find_element(By.XPATH,
                                         "//strong[text()='Operating System']/ancestor::div[@class='aps-attr-title']/following-sibling::div/span")
        os = os_section.text
    except:
        os = 'N/A'

    return {
        'device_name': device_name,
        'manufacturer': manufacturer,
        'rear_camera': rear_camera_specs,
        'front_camera': front_camera_specs,
        'operating_system': os
    }


def fetch_page_specs(page_number):
    driver = get_driver()
    base_url = "https://www.gizmochina.com/cat/mobiles"
    page_url = f"{base_url}/page/{page_number}"
    try:
        device_links = scrape_device_links(driver, page_url)
        all_device_specs = []
        print(f"Scraping page {page_number}, found {len(device_links)} devices")

        for link in device_links:
            try:
                specs = get_device_specs(driver, link)
                print(specs)
                # Filter out devices without camera specs
                if specs['rear_camera'].get('resolution', 'N/A') != 'N/A' or specs['front_camera'].get('resolution',
                                                                                                       'N/A') != 'N/A':
                    all_device_specs.append(specs)
            except Exception as e:
                print(f"Error getting specs for link {link}: {e}")

        return all_device_specs

    except Exception as e:
        print(f"Error on page {page_number}: {e}")
        return []

    finally:
        driver.quit()
def main():
    total_pages = 293
    batch_size = 8
    all_device_specs = []

    for batch_start in range(281, total_pages + 1, batch_size):
        batch_end = min(batch_start + batch_size - 1, total_pages)
        print(f"Processing batch: pages {batch_start} to {batch_end}")

        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(fetch_page_specs, page_number) for page_number in range(batch_start, batch_end + 1)]

            for future in as_completed(futures):
                try:
                    result = future.result()
                    all_device_specs.extend(result)
                except Exception as e:
                    print(f"Error occurred: {e}")

    # Process all_device_specs as needed, for example save to a file or database
    print(f"Scraped data from {total_pages} pages")
if __name__ == "__main__":
    main()
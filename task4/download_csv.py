from selenium import webdriver
import pandas as pd
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import chromedriver_binary
from chromedriver_binary import utils
import re
import os
import time


def download_csv(driver, url, name):
    driver.get(url)

    try:
        driver.find_element(By.ID, 'pageTitleHeader').text
        with open(os.path.join('data/citations', f'{name}.csv'), 'w+') as f:
            f.write('Author(s) ID,Link')
    except:
        time.sleep(1)
        try:
            driver.find_element(By.ID, "_pendo-close-guide_").click()
        except:
            pass

        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".noLabel")))
        driver.find_element(By.CSS_SELECTOR, ".noLabel").click()

        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#export_results > .ico-navigate-down")))
        driver.find_element(By.CSS_SELECTOR, "#export_results > .ico-navigate-down").click()

        wait.until(EC.visibility_of_element_located((By.ID, "exportTrigger")))
        driver.find_element(By.ID, "exportTrigger").click()

        if int(re.sub("\D", "", driver.find_element(By.CLASS_NAME, "resultsCount").text)) > 2000:
            wait.until(EC.visibility_of_element_located((By.ID, "exportTypeAndFormat")))
            driver.find_element(By.ID, "exportTypeAndFormat").click()

            wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#chunkExportTrigger > .btnText")))
            driver.find_element(By.CSS_SELECTOR, "#chunkExportTrigger > .btnText").click()

        while not os.path.isfile("data/citations/scopus.csv"):
            time.sleep(1)
        os.rename(os.path.join("data/citations", "scopus.csv"), os.path.join("data/citations", f"{name}.csv"))


if __name__ == '__main__':
    data = pd.read_csv("data/nodes.csv")

    options = Options()
    preference = {'download.default_directory': os.path.join(os.getcwd(),"data/citations"), "safebrowsing.enabled": "false"}
    options.add_experimental_option('prefs', preference)

    driver = webdriver.Chrome(options=options)
    # driver.set_window_size(2000,1500)
    wait = WebDriverWait(driver, 1000)

    i=0
    for index, row in data.iterrows():
        print(index)
        url = row["citations"]
        id = row["id"]
        if not os.path.isfile(os.path.join("data/citations",f"{id}.csv")):
            try:
                if i == 0:
                    driver.get(url)

                try:
                    driver.find_element(By.ID, 'pageTitleHeader').text
                    with open(os.path.join('data/citations', f'{id}.csv'), 'w+') as f:
                        f.write('Author(s) ID,Link')
                except:
                    wait.until(EC.visibility_of_element_located((By.ID, "_pendo-close-guide_")))
                    driver.find_element(By.ID, "_pendo-close-guide_").click()
                    wait.until(EC.visibility_of_element_located((By.ID, "_pendo-close-guide_")))
                    driver.find_element(By.ID, "_pendo-close-guide_").click()
                    driver.find_element(By.CSS_SELECTOR, ".noLabel").click()
                    driver.find_element(By.CSS_SELECTOR, "#export_results > .btnText").click()

                    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".radio-inline:nth-child(5) span")))
                    driver.find_element(By.CSS_SELECTOR, ".radio-inline:nth-child(5) span").click()
                    driver.find_element(By.CSS_SELECTOR, ".citationGroupCheckboxes > .checkbox-label").click()
                    driver.find_element(By.CSS_SELECTOR, "#authorIdChckbox > .checkbox-label").click()
                    driver.find_element(By.CSS_SELECTOR, "#exportTrigger > .btnText").click()
                    print(int(re.sub("\D", "", driver.find_element(By.CLASS_NAME, "resultsCount").text)))
                    if int(re.sub("\D", "", driver.find_element(By.CLASS_NAME, "resultsCount").text)) > 2000:
                        print("jeden")
                        wait.until(EC.visibility_of_element_located((By.ID, "exportTypeAndFormat")))
                        print("dwa")
                        driver.find_element(By.ID, "exportTypeAndFormat").click()
                        print("trzy")
                        # wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#chunkExportTrigger > .btnText")))
                        driver.find_element(By.CSS_SELECTOR, "#chunkExportTrigger > .btnText").click()
                        print("cztery")
                    while not os.path.isfile(os.path.join("data/citations", "scopus.csv")):
                        time.sleep(1)
                    os.rename(os.path.join("data/citations", "scopus.csv"), os.path.join("data/citations", f"{id}.csv"))
                    i+=1
                else:
                    download_csv(driver, url,id)
            except NoSuchElementException:
                print('0 citations')
                i+=1

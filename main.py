from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium import webdriver
import pandas as pd
import config
import time


driver = webdriver.Chrome()

# Navigate to url
driver.get('https://itdashboard.gov/')


def create_table():
    #Time of wait
    driver.implicitly_wait(5)

    #Now click on button
    dive_button = driver.find_element(By.LINK_TEXT, value='DIVE IN')
    dive_button.click()
    time.sleep(5)

    #Gets all departments and amounts -> objects
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="agency-tiles-container"]')))
    departments = driver.find_elements(By.XPATH, '//div[@id="agency-tiles-widget"]//span[@class="h4 w200"]')
    amounts = driver.find_elements(By.XPATH, '//div[@id="agency-tiles-widget"]//span[@class=" h1 w900"]')

    agencies = [department.text for department in departments]
    spendings = [amount.text for amount in amounts]

    #Add data in table -> table
    dictionary = {'department': agencies, 'amount': spendings, }
    df = pd.DataFrame(data=dictionary).drop_duplicates(ignore_index=True)
    df.to_excel('output/Agencies.xlsx', index=False)
    # Openening the file and work on it -> open_web_page
    agency = departments[agencies.index(config.agency)].click()
    time.sleep(8)
    return print('File Agencies created')


def get_data():
    #Displaying the entire table
    selector = driver.find_element_by_xpath(\
        "/html/body/main/div/div/div/div[4]/div/div/div/div[2]/div/div[1]/div/div/div/div/div[2]/div[2]/div/label/select/option[4]")
    selector.click()
    time.sleep(10)

    table = driver.find_element_by_id("investments-table-container")
    pd_table = pd.read_html(table.get_attribute("outerHTML"))
    pd_table[1].to_excel(f"output/{config.agency}_Individual_Investments.xlsx", index=False)

    #Getting links
    links_column = table.find_elements_by_tag_name("a")
    links = [item.get_attribute('href') for item in links_column if item.get_attribute('href') != None]
    time.sleep(5)
    driver.quit()

    #Downloadables file
    options = webdriver.ChromeOptions()
    prefs = {"download.default_directory": "\output"}
    options.add_experimental_option("prefs", prefs)
    for link in links:
        driver = webdriver.Chrome(options=options)
        driver.get(link)
        time.sleep(5)
        download = driver.find_element_by_xpath(\
            '/html/body/main/div/div/div/div[1]/div/div/div/div/div[1]/div/div/div/div/div[6]/a')
        download.click()
        time.sleep(10)
    driver.quit()


def main():
    create_table()
    get_data()



if __name__ == '__main__':
    main()





from selenium.webdriver.common.by import By
from selenium import webdriver
import xlsxwriter
import os

driver = webdriver.Chrome()


def main():

    # Navigate to url
    driver.get('https://itdashboard.gov/')

    # Now click on button
    dive_button = driver.find_element(By.LINK_TEXT, value='DIVE IN')
    dive_button.click()

    amounts =driver.find_elements(By.XPATH, '//*[@id="agency-tiles-widget"]/div/div[*]/div[*]/div/div/div/div[1]/a/span[2]')

    # Create a workbook and add a worksheet.
    workbook = xlsxwriter.Workbook('task.xlsx')
    worksheet = workbook.add_worksheet("Agencies")

    col = 0
    row = 0

    # Iterate over the data and write it out row by row.
    for date in amounts:
        worksheet.write(row, col, date.text)
        row += 1
    workbook.close()
    try:
        agency = driver.find_element(By.PARTIAL_LINK_TEXT, os.getenv("AGENCY"))
        agency.click()
    except BaseException:
        print("Error")


if __name__ == '__main__':
    main()
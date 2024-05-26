from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import os
from concurrent.futures import ThreadPoolExecutor
from selenium.webdriver.remote.webdriver import WebDriver


def download_file(link, driver: WebDriver, download_path: str):
    href = link.get_attribute('href')
    if href:
        file_name = href.split('/')[-1]
        file_path = os.path.join(download_path, file_name)

        # 检查文件是否已经存在
        if os.path.exists(file_path):
            return

        # 执行下载
        print(f'Downloading: {href}')
        driver.get(href)

        # 等待文件下载完成
        while not os.path.exists(file_path) or file_path.endswith('.crdownload'):
            time.sleep(1)
        print(f"Downloaded: {file_path}")

def download(links, driver: WebDriver, download_path: str, max_workers: int = 8):
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(download_file, link, driver, download_path) for link in links]
        for future in futures:
            future.result()


# 设置下载文件夹的路径
base_download_path = r'C:\Users\13512\Downloads'
driver_path = r'D:\other\chromedriver-win64\chromedriver.exe'
base_url = 'https://noaa-nesdis-tcprimed-pds.s3.amazonaws.com/index.html#v01r00/final/'
years = range(2021, 1996, -1)
basins = ['AL', 'CP', 'EP', 'IO', 'SH', 'WP']
numbers = [f'{i:02d}' for i in range(1, 100)]

# 创建驱动，配置Selenium WebDriver：实例化，加入下载地址和无界面模式
options = webdriver.ChromeOptions()
prefs = {'download.default_directory': base_download_path}
options.add_experimental_option('prefs', prefs)
# options.add_argument('--headless')
service = Service(driver_path)
driver = webdriver.Chrome(service=service, options=options)

# 逐页面下载
for year in years:
    for basin in basins:
        for number in numbers:
            url = f'{base_url}{year}/{basin}/{number}/'
            driver.get(url)

            # 总共等待30s, 每3s检查一次，找不到文件直接进下一个洋区
            total_wait_time = 0
            incremental_wait_time = 3
            while total_wait_time <= 27:
                time.sleep(3)
                # 判断是否有文件
                links = driver.find_elements(By.XPATH, '//a[contains(@href, ".nc")]')
                if links:
                    check_num = 1
                    driver.close()

                    # 更改下载路径和驱动
                    download_path = os.path.join(base_download_path, str(year), basin, number)
                    os.makedirs(download_path, exist_ok=True)
                    prefs = {'download.default_directory': download_path}
                    options.add_experimental_option('prefs', prefs)
                    driver = webdriver.Chrome(service=service, options=options)
                    driver.get(url)
                    links = driver.find_elements(By.XPATH, '//a[contains(@href, ".nc")]')
                    while not links:
                        time.sleep(1)
                        links = driver.find_elements(By.XPATH, '//a[contains(@href, ".nc")]')
                    download(links, driver, download_path)

                    # 文件大于50个，就翻页，如果正好是50倍数个，会重复8次后停止，防止卡住
                    while len(links) == 50:
                        if check_num == 8:
                            break
                        next_button = driver.find_element(By.XPATH, '//a[@aria-label="Next"]')
                        next_button.click()
                        time.sleep(5)
                        links = driver.find_elements(By.XPATH, '//a[contains(@href, ".nc")]')
                        download(links, driver, download_path)
                        check_num += 1
                    break
                else:
                    total_wait_time += incremental_wait_time
                    time.sleep(incremental_wait_time)
            if total_wait_time > 27:
                print("总等待时间超限，未找到 .nc 文件的链接，并开始下载下一个洋区")
                break
            print(f"{year}, {basin}, {number} has been downloaded")
driver.quit()
print("所有文件下载尝试完成。")

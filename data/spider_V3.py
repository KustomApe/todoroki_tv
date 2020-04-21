import pandas as pd
import time
import requests
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

# 初期設定
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--lang=ja')
browser = webdriver.Chrome(options=options, executable_path='./chromedriver')
# 取得先URL
url = 'https://fx.minkabu.jp/indicators'

# Basic settings
res = requests.get(url)
soup = bs(res.text, 'html5lib')
captions = soup.find_all('caption')
data = []

# データフレーム構築
df = pd.DataFrame(columns=['time_launch', 'name', 'important_level', 'moving_average', 'data01', 'data02', 'data03'])
dfs = pd.DataFrame(index=['release_date'])

# CSS Selectorの設定
PAGER_NEXT = 'a.ml10'
B_TABLE = 'table.tbl-fixed'
TABLE = 'tbody'
COLUMN = 'tr.fs-s'
TIME = 'td.eilist__time'
NAME = 'p.fbd'
SUB_NAME = 'p.fc-sub'
IMPORTANT_LEVEL = 'img.i-star'
MOVING_AVERAGE = 'td.eilist__move'
DATAS = 'td.eilist__data'
TAG_SPAN = 'span'
FILLED_STARS = 'Star fill'
DATE = 'caption.tlft'

# 実行部分
browser.get(url)

while True:
    pager = browser.find_elements_by_css_selector(PAGER_NEXT)
    # 日時含めたテーブル
    table_nums = browser.find_elements_by_css_selector(B_TABLE)
    if len(pager) > 0 and len(table_nums) > 0:
        print('Start getting tables...')
        e = 1
        print(e)
        if len(table_nums) > 0:
            for table_num in table_nums:
                f = str(e)
                n = 1
                m = str(n)
                # テーブルタグの中の実際のデータ
                base_tables = browser.find_element_by_xpath('/html/body/div/main/section/div/table[' + m + ']/tbody')
                for base_table in table_nums:
                    try:
                        release_date = browser.find_element_by_xpath('/html/body/div/main/section/div/table[' + f + ']/caption').text
                        e += 1
                        f = str(e)
                        tables = base_table.find_elements_by_tag_name(COLUMN)
                        print(release_date)
                        for table in tables:
                            try:
                                time_release = table.find_element_by_css_selector(TIME)
                                time_launch = time_release.find_element_by_tag_name(TAG_SPAN).text
                                if time_launch:
                                    print('時間 : ' + time_launch)
                                elif time_launch == ' ':
                                    time_launch = 'None'
                                    print('時間 : ' + time_launch)
                                else:
                                    print('Error')
                                    pass
                                name = table.find_element_by_css_selector(NAME).text
                                if name:
                                    print('指標名 : ' + name)
                                sub_name = table.find_element_by_css_selector(SUB_NAME).text
                                if sub_name:
                                    print('メモ : ' + sub_name)
                                elif sub_name == ' ':
                                    sub_name = 'None'
                                    print('メモ : ' + sub_name)
                                else:
                                    pass
                                important_data = table.find_elements_by_css_selector(IMPORTANT_LEVEL)
                                if len(important_data) > 0:
                                    nums = 0
                                    for stars in important_data:
                                        filled = stars.get_attribute('alt')
                                        if filled == FILLED_STARS:
                                            nums += 1
                                    print('重要度 : ' + str(nums))
                                moving_average = table.find_element_by_css_selector(MOVING_AVERAGE).text
                                print('前回ドル円変動幅 : ' + moving_average)
                                data01 = table.find_element_by_xpath('//*/td[5]/span').text
                                data02 = table.find_element_by_xpath('//*/td[6]/span').text
                                data03 = table.find_element_by_xpath('//*/td[7]/span').text
                                print('前回(改定) : ' + data01)
                                print('予想 : ' + data02)
                                print('結果 : ' + data03)
                            except NoSuchElementException:
                                print('NA')
                        print('--------------------------------------')
                        n += 1
                    except NoSuchElementException:
                        btn = browser.find_element_by_css_selector(PAGER_NEXT).get_attribute('href')
                        pass
        print('next url:{}'.format(btn))
        time.sleep(3)
        browser.get(btn)
        print('Moving to next page...')
    else:
        print('No pager exist anymore.')
        break
print('Finished scraping. Writing out to CSV......')
# df_final = df.set_index([dfs])
# print(df_final)
print('Done')

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
import time

# 初期設定
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--lang=ja')
browser = webdriver.Chrome(options=options, executable_path='./chromedriver')

# データフレーム構築
df = pd.DataFrame(columns=['release_time', 'time_launch', 'name', 'important_level', 'moving_average', 'data01', 'data02', 'data03'])

# 取得先URL
url = 'https://fx.minkabu.jp/indicators'

# CSS Selectorの設定
PAGER_NEXT = 'a.ml10'
B_TABLE = 'table.tbl-fixed'
TABLE = 'tbody'
COLUMN = 'tr.fs-s'
TIME = 'td.eilist__time'
NAME = 'p.fbd'
IMPORTANT_LEVEL = 'img.i-star'
MOVING_AVERAGE = 'td.eilist__move'
DATAS = 'td.eilist__data'
TAG_SPAN = 'span'
FILLED_STARS = 'Star fill'
DATE = 'caption.tlft'

# 実行部分
browser.get(url)

while True: # Continue until getting the last page.
    if len(browser.find_elements_by_css_selector(PAGER_NEXT)) > 0:
        print('Start getting tables...')
        table_nums = browser.find_elements_by_css_selector(B_TABLE)
        if len(table_nums) > 0 and table_nums is not None:
            dates = browser.find_elements_by_css_selector(B_TABLE)
            n = 1
            m = str(n)
            for date in dates:
                release_date = date.find_element_by_css_selector(DATE).text
                print(release_date)
                base_table = browser.find_element_by_xpath('/html/body/div/main/section/div/table[' + m + ']/tbody')
                tables = base_table.find_elements_by_tag_name(COLUMN)
                n += 1
                print(n)
                for table in tables:
                    try:
                        time_release = table.find_element_by_css_selector(TIME)
                        time_launch = time_release.find_element_by_tag_name(TAG_SPAN).text
                        if time_launch or time_launch == '':
                            print('時間 : ' + time_launch)
                        else:
                            print('Error')
                        name = table.find_element_by_css_selector(NAME).text
                        print('指標名 : ' + name)
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
                        print('--------------------------------------')
                        n += 1
                    except NoSuchElementException as e:
                        print(e)
                btn = browser.find_element_by_css_selector(PAGER_NEXT).get_attribute('href')
            print('next url:{}'.format(btn))
            time.sleep(3)
            browser.get(btn)
            print('Moving to next page...')
    else:
        print('No pager exist anymore.')
        break
print('Finished scraping. Writing out to CSV......')
df.to_csv('indicators_01.csv')
print('Done')
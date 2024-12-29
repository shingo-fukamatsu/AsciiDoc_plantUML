#import time
#from selenium import webdriver
#
#driver = webdriver.Chrome()
##driver = webdriver.Chrome(r'c:\chromedriver-win64\chromedriver.exe')
#driver.get('https://www.google.com/')
#time.sleep(5)
##search_box = driver.find_element_by_name("q")
#search_box = driver.find_element(By.CLASS_NAME, 'UK6dSd')
#search_box.send_keys('ChromeDriver')
#search_box.submit()
#time.sleep(5)
#driver.quit()
#
import time 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# WebDriverのインスタンスを作成
driver = webdriver.Chrome()

try:
    # Googleのトップページを開く
    driver.get('https://copilot.microsoft.com/')
    time.sleep(5)

    # 検索ボックスを見つける
    start_bottun = driver.find_element(By.CLASS_NAME, 'relative flex items-center justify-center text-foreground-250 fill-foreground-250 active:text-foreground-350 active:fill-foreground-350 dark:text-foreground-750 dark:fill-foreground-750 dark:active:text-foreground-650 dark:active:fill-foreground-650 shadow-button-strong-light dark:shadow-button-dark bg-stone-800 hover:bg-black active:bg-stone-750 dark:bg-slate-600 dark:hover:bg-slate-550 dark:active:bg-slate-600/80 text-base min-h-14 min-w-14 px-4 py-3.5 gap-x-3 rounded-4xl before:rounded-4xl before:absolute before:inset-0 before:pointer-events-none before:border before:border-transparent before:contrast-more:border-2 outline-2 outline-offset-1 focus-visible:z-[1] focus-visible:outline focus-visible:outline-stroke-900 w-full shadow-lg min-w-40 sm:w-auto')
    start_bottun.click()
    time.sleep(5)
#    # 検索キーワードを入力
#    search_box.send_keys('Murasan IT Lab')
#
#    # Enterキーを送信して検索を実行
#    search_box.send_keys(Keys.RETURN)
#
#    # 検索結果画面が表示されるまで待機
#    WebDriverWait(driver, 10).until(
#        EC.presence_of_element_located((By.ID, 'search'))
#    )
    
    # 10秒間待機してユーザーが検索結果を確認できるようにする
    time.sleep(5)
finally:
    # ブラウザを閉じる (エラーが発生しても必ず実行)
    driver.quit()

    
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
    driver.get('https://www.yahoo.co.jp/')

    # 検索ボックスを見つける
    search_box = driver.find_element(By.CLASS_NAME, '_1wsoZ5fswvzAoNYvIJgrU4')

    # 検索キーワードを入力
    search_box.send_keys('Asciidoc')

    # Enterキーを送信して検索を実行
    search_box.send_keys(Keys.RETURN)

    # 検索結果画面が表示されるまで待機
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'search'))
    )
    
    # 10秒間待機してユーザーが検索結果を確認できるようにする
    time.sleep(5)
finally:
    # ブラウザを閉じる (エラーが発生しても必ず実行)
    driver.quit()

    
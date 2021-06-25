import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from tkinter import messagebox

def ConnectDriver(parent):
    '''これはChromeDriverを用いた動作を行う'''
    def getDetailData(driver,wait,link):
        '''詳細を取得し元のページに戻る'''
        driver.find_element_by_id(link).click()
        wait.until(expected_conditions.element_to_be_clickable((By.ID, "listShinseiView_itm14")))
        #ここで要素内容を切り出して、リストを作成しそれを返却する
        U_ID = driver.find_element_by_id('lblNo').text
        U_NAME = driver.find_element_by_id('lblName').text
        U_NAME = ''.join(U_NAME.split())[:-1]
        #対象の日付の取得
        #申請の種別によって、日付や理由の位置が変更されてしまう問題をいかに解決するか(申請種別を取得しそれごとに取得する内容を変更するしかない)
        StartDate_list = [driver.find_element_by_id('listShinseiView_itm2').text,driver.find_element_by_id('listShinseiView_itm3').text,driver.find_element_by_id('listShinseiView_itm4').text,driver.find_element_by_id('listShinseiView_itm5').text,driver.find_element_by_id('listShinseiView_itm6').text]
        D_StartDate = ''.join(StartDate_list)
        D_ENDDate = ''
        
        if re.compile("\d{4}").search(driver.find_element_by_id('listShinseiView_itm9').text) and re.compile("\d{1,2}").search(driver.find_element_by_id('listShinseiView_itm11').text) and re.compile("\d{1,2}").search(driver.find_element_by_id('listShinseiView_itm13').text):
            ENDDate_list = [driver.find_element_by_id('listShinseiView_itm9').text,driver.find_element_by_id('listShinseiView_itm10').text,driver.find_element_by_id('listShinseiView_itm11').text,driver.find_element_by_id('listShinseiView_itm12').text,driver.find_element_by_id('listShinseiView_itm13').text]
            D_ENDDate = D_ENDDate.join(ENDDate_list)

        D_title = driver.find_element_by_id('lblTitle').text
        #終了日があると理由が取得できない問題(listShinseiView_itm14)がずれる
        D_Reason = driver.find_element_by_id('listShinseiView_itm14').text
        Detail_Dict ={'ID':U_ID,'NAME':U_NAME,'StartDate':D_StartDate,'EndDate':D_ENDDate,'Title':D_title,'Reason':D_Reason}
        '''申請一覧のページに戻る'''
        driver.back()
        wait.until(expected_conditions.element_to_be_clickable((By.ID, "listShinseiList")))
        return Detail_Dict
    if parent.St_ID.get()!='' and parent.St_PASS.get() != '':
        #seleniumの設定
        option = Options()
        option.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver = webdriver.Chrome("C:\chromedriver_win32\chromedriver.exe",options=option)
        driver.get(parent.St_URL)
        wait = WebDriverWait(driver,10)
        #ログイン処理
        ID = driver.find_element_by_id('txtLoginId')
        ID.send_keys(parent.St_ID.get())
        PASS = driver.find_element_by_id('txtPassword')
        PASS.send_keys(parent.St_PASS.get())
        BTN_LOGIN = driver.find_element_by_id('btnLogin')
        BTN_LOGIN.click()
        #メイン画面から申請一覧へ移行する
        wait.until(expected_conditions.element_to_be_clickable((By.ID, "btnShinsei")))
        BTN_Shinsei = driver.find_element_by_id('btnShinsei')
        BTN_Shinsei.click()
        wait.until(expected_conditions.element_to_be_clickable((By.ID, "listShinseiList_ctl00_linkShinsei")))
        BTN_ITIRAN = driver.find_element_by_id('listShinseiList_ctl00_linkShinsei')
        BTN_ITIRAN.click()

        #一覧から申請一覧を抜き出し、IDのリストを抽出する
        wait.until(expected_conditions.element_to_be_clickable((By.ID, "listShinseiList")))
        table_list = driver.find_elements_by_xpath("//table[@id='listShinseiList']/tbody/tr/td[3]/a")
        links_list = [iterater.get_attribute('id') for iterater in table_list]
        #ここで辞書を作成する
        Detail_dictList = []
        #とりあえず先頭2件のデータのリンクをクリックして情報を取得する(今後複数データを取得することになる)
        for iterate in range(0,4):
            '''申請一覧ページであるかを待つ必要がある'''
            Detail_dictList.append(getDetailData(driver,wait,links_list[iterate]))
        print(Detail_dictList)
    else:
        messagebox.showwarning("警告","IDとパスワードを入力してください")
    return "break"
        #ここで要素を取得する
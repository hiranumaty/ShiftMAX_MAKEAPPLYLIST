from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from tkinter import messagebox

def ConnectDriver(parent):
    '''これはChromeDriverを用いた動作を行う'''
    def getDetailData(driver,wait,link):
        '''詳細情報を辞書の形で取得しreturn'''
        #要素を取得して、辞書にして返す
        driver.find_element_by_id(link).click()
        wait.until(expected_conditions.element_to_be_clickable((By.ID, "lblTitle")))
        U_ID = driver.find_element_by_id('lblNo').text
        U_NAME = driver.find_element_by_id('lblName').text
        U_NAME = ''.join(U_NAME.split())[:-1]
        D_title = driver.find_element_by_id('lblTitle').text
        #titleを元に取得個所を変更する
        D_StartDate = ''
        D_ENDDate = ''
        D_Reason = ''
        if D_title == "休暇申請":
            StartDate_list = [driver.find_element_by_id('listShinseiView_itm2').text,driver.find_element_by_id('listShinseiView_itm3').text,driver.find_element_by_id('listShinseiView_itm4').text,driver.find_element_by_id('listShinseiView_itm5').text,driver.find_element_by_id('listShinseiView_itm6').text]
            D_StartDate = D_StartDate.join(StartDate_list)
            ENDDate_list = [driver.find_element_by_id('listShinseiView_itm9').text,driver.find_element_by_id('listShinseiView_itm10').text,driver.find_element_by_id('listShinseiView_itm11').text,driver.find_element_by_id('listShinseiView_itm12').text,driver.find_element_by_id('listShinseiView_itm13').text]
            D_ENDDate = D_ENDDate.join(ENDDate_list)
            D_Reason = driver.find_element_by_id('listShinseiView_itm17').text
        elif D_title == "シフト勤務申請":
            StartDate_list = [driver.find_element_by_id('listShinseiView_itm2').text,driver.find_element_by_id('listShinseiView_itm3').text,driver.find_element_by_id('listShinseiView_itm4').text,driver.find_element_by_id('listShinseiView_itm5').text,driver.find_element_by_id('listShinseiView_itm6').text]
            D_StartDate = D_StartDate.join(StartDate_list)
            D_Reason = driver.find_element_by_id('listShinseiView_itm10').text
        Detail_Dict ={'ID':U_ID,'NAME':U_NAME,'StartDate':D_StartDate,'EndDate':D_ENDDate,'Title':D_title,'Reason':D_Reason}
        '''申請一覧のページに戻る'''
        driver.find_element_by_id('btnBack').click()
        wait.until(expected_conditions.element_to_be_clickable((By.ID, "listShinseiList")))
        return Detail_Dict
    '''以下がドライバーの基本操作'''
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
        #現在一覧の1ページ目しか見れていない
        links_list = [iterater.get_attribute('id') for iterater in table_list if (iterater.text=="休暇申請" or iterater.text=="シフト勤務申請")]
        #ここで辞書を作成する
        Detail_dictList = []
        #for iterate in range(0,len(links_list)):
        #とりあえず先頭3件のデータのリンクをクリックして情報を取得する
        for iterate in range(0,3):
            '''申請一覧ページであるかを待つ必要がある'''
            Detail_dictList.append(getDetailData(driver,wait,links_list[iterate]))
        print(Detail_dictList)
    else:
        messagebox.showwarning("警告","IDとパスワードを入力してください")
    return "break"
        #ここで要素を取得する
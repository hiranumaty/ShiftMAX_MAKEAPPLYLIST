from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from Modules import DateComparison
def ConnectDriver(parent):
    '''これはChromeDriverを用いた動作を行う
    1アカウントの申請情報(休暇申請orシフト勤務申請データの一覧を取得する)
    '''
    def getDetailData(parent,driver,wait,link):
        '''詳細情報を辞書の形で取得しreturn'''
        #要素を取得して、辞書にして返す
        driver.find_element_by_id(link).click()
        wait.until(expected_conditions.element_to_be_clickable((By.ID, "lblTitle")))
        U_ID = driver.find_element_by_id('lblNo').text
        U_NAME = driver.find_element_by_id('lblName').text
        U_NAME = ''.join(U_NAME.split())[:-1]
        D_title = driver.find_element_by_id('lblTitle').text
        D_StartDate = ''
        D_ENDDate = ''
        D_Reason = ''
        appendflg =None
        #申請種別ごとに取得するフィールドが異なる
        if D_title == "休暇申請":
            StartDate_list = [driver.find_element_by_id('listShinseiView_itm2').text,driver.find_element_by_id('listShinseiView_itm3').text,driver.find_element_by_id('listShinseiView_itm4').text,driver.find_element_by_id('listShinseiView_itm5').text,driver.find_element_by_id('listShinseiView_itm6').text]
            D_StartDate = D_StartDate.join(StartDate_list)
            ENDDate_list = [driver.find_element_by_id('listShinseiView_itm9').text,driver.find_element_by_id('listShinseiView_itm10').text,driver.find_element_by_id('listShinseiView_itm11').text,driver.find_element_by_id('listShinseiView_itm12').text,driver.find_element_by_id('listShinseiView_itm13').text]
            D_ENDDate = D_ENDDate.join(ENDDate_list)
            D_Reason = driver.find_element_by_id('listShinseiView_itm17').text
            #フィルターの日付に合致するデータかどうかを判断する
            appendflg = DateComparison.DateCompare2(parent,D_StartDate,D_ENDDate)
        elif D_title == "シフト勤務申請":
            StartDate_list = [driver.find_element_by_id('listShinseiView_itm2').text,driver.find_element_by_id('listShinseiView_itm3').text,driver.find_element_by_id('listShinseiView_itm4').text,driver.find_element_by_id('listShinseiView_itm5').text,driver.find_element_by_id('listShinseiView_itm6').text]
            D_StartDate = D_StartDate.join(StartDate_list)
            D_Reason = driver.find_element_by_id('listShinseiView_itm10').text
            #フィルターの日付に合致するデータかどうかを判断する
            appendflg = DateComparison.DateCompare1(parent,D_StartDate)
        Detail_Dict ={'ID':U_ID,'NAME':U_NAME,'StartDate':D_StartDate,'EndDate':D_ENDDate,'Title':D_title,'Reason':D_Reason}
        '''申請一覧のページに戻る'''
        driver.find_element_by_id('btnBack').click()
        wait.until(expected_conditions.element_to_be_clickable((By.ID, "listShinseiList")))
        if appendflg:
            return Detail_Dict
        else:
            return None

    '''以下がドライバーの基本操作'''
    #seleniumの設定
    option = Options()
    option.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(parent.DRIVERURL,options=option)
    driver.get(parent.St_URL)
    wait = WebDriverWait(driver,10)
    #ログイン処理
    ID = driver.find_element_by_id('txtLoginId')
    ID.send_keys(parent.St_ID.get())
    PASS = driver.find_element_by_id('txtPassword')
    PASS.send_keys(parent.St_PASS.get())
    BTN_LOGIN = driver.find_element_by_id('btnLogin')
    BTN_LOGIN.click()
    try:
        wait.until(expected_conditions.element_to_be_clickable((By.ID, "btnShinsei")))
        BTN_Shinsei = driver.find_element_by_id('btnShinsei')
        BTN_Shinsei.click()
        wait.until(expected_conditions.element_to_be_clickable((By.ID, "listShinseiList_ctl00_linkShinsei")))
        BTN_ITIRAN = driver.find_element_by_id('listShinseiList_ctl00_linkShinsei')
        BTN_ITIRAN.click()
        SELECT_TITLE = parent.APPLYNAMEAREA.get()
        #一覧から詳細情報の配列を作成する(リストが複数ページ存在する場合はそれぞれ取得する)
        Detail_dictList = []
        firstloop =True
        while True:
            if firstloop ==False:
                driver.find_element_by_id('btnPageNext').click()
            else:
                firstloop =False
            wait.until(expected_conditions.element_to_be_clickable((By.ID, "listShinseiList")))
            table_list = driver.find_elements_by_xpath("//table[@id='listShinseiList']/tbody/tr/td[3]/a")
            links_list = None
            #そのページの一覧に含まれる取得したい情報のページのリンクを取得する
            if SELECT_TITLE == "選択無し":
                links_list = [iterater.get_attribute('id') for iterater in table_list if (iterater.text=="休暇申請" or iterater.text=="シフト勤務申請")]
            elif SELECT_TITLE == "休暇申請":
                links_list = [iterater.get_attribute('id') for iterater in table_list if iterater.text=="休暇申請"]
            elif SELECT_TITLE == "シフト勤務申請":
                links_list = [iterater.get_attribute('id') for iterater in table_list if iterater.text=="シフト勤務申請"]
            
            for iterate in range(0,len(links_list)):
                #現在は1ページごとに3件取得する
                if iterate ==3:
                    break
                appendData = getDetailData(parent,driver,wait,links_list[iterate])
                if appendData is not None:
                    Detail_dictList.append(appendData)
            #次へのボタンがある限り続ける
            if len(driver.find_elements_by_id('btnPageNext'))==0:
                break
        driver.quit()
        return Detail_dictList
    except TimeoutException as e:
        driver.quit()
        return ""
    return ""
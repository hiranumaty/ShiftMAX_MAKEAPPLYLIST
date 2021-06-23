import tkinter as tk
import tkinter.ttk as ttk
import asyncio
import time
from tkcalendar import Calendar, DateEntry
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from tkinter import messagebox
class MakeApplyList(tk.Frame):
    '''
    このwindowを用いて作成する
    '''
    
    def __init__(self,master=None):
        self.St_URL = "https://trs-shiftmax.jp/trTk1559"
        self.St_ID = tk.StringVar()
        self.St_PASS = tk.StringVar()
        self.St_BEGINING = tk.StringVar()
        self.St_FINAL = tk.StringVar()
        self.sub_win = None
        super().__init__(master)
        self.create_widgets(master)
    def create_widgets(self,master):
        #ラベル
        LBL1 = tk.Label(master,text="ID:",width=2)
        LBL2 = tk.Label(master,text="PASS:",width=6)
        LBL1.place(x=30,y=20)
        LBL2.place(x=200,y=20)
        LBL3 = tk.Label(master,text="申請名:",width=5)
        LBL3.place(x=30,y=80)
        LBL4 = tk.Label(master,text="日付:",width=5)
        LBL4.place(x=30,y=150)
        LBL5 = tk.Label(master,text="~",width=1)
        LBL5.place(x=200,y=150)
        #UserInfo
        IDAREA = tk.Entry(master,width=20,textvariable=self.St_ID)
        IDAREA.place(x=60,y=20)
        PASSAREA = tk.Entry(master,width=20,textvariable=self.St_PASS)
        PASSAREA.place(x=250,y=20)
        #申請名コンボボックス
        APPLYNAMEAREA = ttk.Combobox(master,state='readonly')
        APPLYNAMEAREA["values"] = ("選択無し","時間外申請","休暇申請","休日出勤申請","打刻修整申請","シフト勤務申請")
        APPLYNAMEAREA.current(0)
        APPLYNAMEAREA.place(x=100,y=80)
        #日付部(クリックイベントでモーダルを適用すること)
        BEGININGDATE = tk.Entry(master,width=20,textvariable=self.St_BEGINING)
        BEGININGDATE.place(x=70,y=150)
        BEGININGDATE.bind('<Button-1>',self.__MORDALBEGINDATE)
        FINALDATE = tk.Entry(master,width=20,textvariable=self.St_FINAL)
        FINALDATE.bind('<Button-1>',self.__MORDALFINALDATE)
        FINALDATE.place(x=230,y=150)
        #ボタン
        BTN_MakeApplyList = tk.Button(master,text="申請一覧抽出",width=40,relief="raised")
        BTN_MakeApplyList.bind('<Button-1>',self.__Driver)
        BTN_MakeApplyList.place(x=50,y=220)
    #モーダルの作成
    def __MORDALBEGINDATE(self,event):
        if self.sub_win == None or not self.sub_win.winfo_exists():
            if self.St_BEGINING.get() !="":
                self.St_BEGINING.set("")
            self.sub_win = tk.Toplevel(master=self.master)
            self.sub_win.title("日付選択(開始日)")
            self.sub_win.geometry("400x300")
            self.inputCal = Calendar(self.sub_win,textvariable=self.St_BEGINING)
            self.inputCal.bind("<Button-1>",self.destroyMORDAL)
            self.inputCal.place(x=100,y=50)
            CloseBTN = tk.Button(self.sub_win,text="決定")
            CloseBTN.bind("<Button-1>",self.destroyMORDAL)
            CloseBTN.place(x=100,y=220)
    def __MORDALFINALDATE(self,event):
        if self.sub_win == None or not self.sub_win.winfo_exists():
            if self.St_FINAL.get() != "":
                self.St_FINAL.set("")
            self.sub_win = tk.Toplevel(master=self.master)
            self.sub_win.title("日付選択(終了日)")
            self.sub_win.geometry("400x300")
            self.inputCal = Calendar(self.sub_win,textvariable=self.St_FINAL)
            self.inputCal.bind("<Button-1>",self.destroyMORDAL)
            self.inputCal.place(x=100,y=50)
            CloseBTN = tk.Button(self.sub_win,text="決定")
            CloseBTN.bind("<Button-1>",self.destroyMORDAL)
            CloseBTN.place(x=100,y=220)
    def destroyMORDAL(self,event):
        self.sub_win.destroy()
    def getDetailData(self,driver,wait,link):
        '''詳細を取得し元のページに戻る'''
        driver.find_element_by_id(link).click()
        wait.until(expected_conditions.element_to_be_clickable((By.ID, "listShinseiView_itm14")))
        #ここで要素内容を切り出して、リストを作成しそれを返却する
        U_ID = driver.find_element_by_id('lblNo').text
        U_NAME = driver.find_element_by_id('lblName').text
        U_NAME = ''.join(U_NAME.split())[:-1]
        #日付(開始と終了の取得をどのように行うか)
        D_title = driver.find_element_by_id('lblTitle').text
        D_Reason = driver.find_element_by_id('listShinseiView_itm14').text
        Detail_Dict ={'ID':U_ID,'NAME':U_NAME,'Title':D_title,'Reason':D_Reason}
        '''申請一覧のページに戻る'''
        driver.back()
        wait.until(expected_conditions.element_to_be_clickable((By.ID, "listShinseiList")))
        return Detail_Dict
    def __Driver(self,event):
        if self.St_ID.get()!='' and self.St_PASS.get() != '':
            #seleniumの設定
            option = Options()
            option.add_experimental_option('excludeSwitches', ['enable-logging'])
            driver = webdriver.Chrome("C:\chromedriver_win32\chromedriver.exe",options=option)
            driver.get(self.St_URL)
            wait = WebDriverWait(driver,10)
            #ログイン処理
            ID = driver.find_element_by_id('txtLoginId')
            ID.send_keys(self.St_ID.get())
            PASS = driver.find_element_by_id('txtPassword')
            PASS.send_keys(self.St_PASS.get())
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
            for iterate in range(0,2):
                '''申請一覧ページであるかを待つ必要がある'''
                print(links_list[iterate])
                Detail_dictList.append(self.getDetailData(driver,wait,links_list[iterate]))
            print(Detail_dictList)
        else:
            messagebox.showwarning("警告","IDとパスワードを入力してください")
        return "break"
            #ここで要素を取得する


def main():
    win = tk.Tk()
    win.geometry("400x300")
    win.title("申請一覧作成")
    MakeApplyList(master=win)
    win.mainloop()

if __name__ == "__main__":
    main()
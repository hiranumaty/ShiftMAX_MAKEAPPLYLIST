import tkinter as tk
import tkinter.ttk as ttk
import time
from tkcalendar import Calendar, DateEntry
from Modules import Driver,PrintExcel,DateComparison,ReadExcel
from os.path import join,dirname
from dotenv import load_dotenv
from tkinter import messagebox,filedialog
import os 
class MakeApplyList(tk.Frame):
    '''
    このwindowを用いて作成する
    起動と同時に設定ファイルからwebドライバーの位置を取得する
    '''
    
    def __init__(self,master=None):
        load_dotenv(verbose=True,encoding='utf8')
        dotenv_path = join(os.getcwd(),'setting.env')
        load_dotenv(dotenv_path)
        self.DRIVERURL = os.environ.get('DRIVERURL')
        self.St_URL = os.environ.get('URL')
        #St_IDとSt_PASSをset()で変更すればDriverで使いまわせるのでは
        self.St_ID = tk.StringVar()
        self.St_PASS = tk.StringVar()
        self.St_EMployeeListPath = tk.StringVar()      
        self.St_BEGINING = tk.StringVar()
        self.St_FINAL = tk.StringVar()
        self.APPLYNAMEAREA = tk.StringVar()
        self.sub_win = None
        super().__init__(master)
        self.create_widgets(master)
    def create_widgets(self,master):
        #ラベル
        LBL1 = tk.Label(master,text="取得対象の社員一覧(.xlsx)",width=20)
        LBL1.place(x=10,y=10)
        LBL3 = tk.Label(master,text="申請名:",width=5)
        LBL3.place(x=30,y=100)
        LBL4 = tk.Label(master,text="日付:",width=5)
        LBL4.place(x=30,y=150)
        LBL5 = tk.Label(master,text="~",width=1)
        LBL5.place(x=200,y=150)
        LBLFILTER = tk.Label(master,text="絞り込み条件の指定:",width=15)
        LBLFILTER.place(x=30,y=60)
        #セパレーター
        separator1 = ttk.Separator(master, orient='horizontal')
        separator1.place(x=0,y=50,width=400)
        separator2 = ttk.Separator(master, orient='horizontal')
        separator2.place(x=0,y=200,width=400)
        #ファイルダイアログをここに設置する
        FILEDIALOG = ttk.Entry(master,textvariable=self.St_EMployeeListPath,width=30)
        FILEDIALOG.bind('<Button-1>',self.file_open)
        FILEDIALOG.place(x=180,y=10)
        #申請名コンボボックス
        APPLYNAMEAREA = ttk.Combobox(master,state='readonly',textvariable=self.APPLYNAMEAREA)
        APPLYNAMEAREA["values"] = ("選択無し","休暇申請","シフト勤務申請")
        APPLYNAMEAREA.current(0)
        APPLYNAMEAREA.place(x=100,y=100)
        #日付部(クリックイベントでモーダルを適用すること)
        BEGININGDATE = tk.Entry(master,width=20,textvariable=self.St_BEGINING)
        BEGININGDATE.place(x=70,y=150)
        BEGININGDATE.bind('<Button-1>',self.__MORDALBEGINDATE)
        FINALDATE = tk.Entry(master,width=20,textvariable=self.St_FINAL)
        FINALDATE.bind('<Button-1>',self.__MORDALFINALDATE)
        FINALDATE.place(x=230,y=150)
        #ボタン
        BTN_MakeApplyList = tk.Button(master,text="申請一覧抽出",width=40,relief="raised")
        BTN_MakeApplyList.bind('<Button-1>',self.__StartModules)
        BTN_MakeApplyList.place(x=50,y=220)
    def __StartModules(self,event):
        """DriverとExcelPrintを起動する"""
        if self.St_EMployeeListPath.get()!='' and DateComparison.EntryCompare(self.St_BEGINING,self.St_FINAL):
            #ログイン用のリストを作成する
            USERSINFO_LIST = ReadExcel.ReadEmployeeList(self)
            Detail_Datas = {}
            for USERINFO in USERSINFO_LIST:
                self.St_ID.set(USERINFO["ID"])
                self.St_PASS.set(USERINFO["PASSWORD"])
                Detail_dictList =  Driver.ConnectDriver(self)
                if Detail_dictList != "":
                    Detail_Datas[USERINFO["ID"]] = Detail_dictList
            PrintExcel.MultiExcelWriter(Detail_Datas)
            return "break"
        else:
            messagebox.showwarning("警告","ファイルの選択ミスまたは日付の入力ミスがあります")
            return "break"
    def file_open(self,event):
        inidir = os.getcwd()
        fTyp = [("", "*.xlsx")]
        filename = filedialog.askopenfilename(filetypes=fTyp,initialdir=inidir)
        if filename:
            self.St_EMployeeListPath.set(filename)
        else:
            messagebox.showwarning("警告","ファイルを選択してください")



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

def main():
    win = tk.Tk()
    win.geometry("400x300")
    win.title("申請一覧作成")
    MakeApplyList(master=win)
    win.mainloop()

if __name__ == "__main__":
    main()
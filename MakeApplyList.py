import tkinter as tk
import tkinter.ttk as ttk
import time
from tkcalendar import Calendar, DateEntry
from Modules import Driver
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
        self.APPLYNAMEAREA = tk.StringVar()
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
        APPLYNAMEAREA = ttk.Combobox(master,state='readonly',textvariable=self.APPLYNAMEAREA)
        APPLYNAMEAREA["values"] = ("選択無し","休暇申請","シフト勤務申請")
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
        BTN_MakeApplyList.bind('<Button-1>',self.__StartModules)
        BTN_MakeApplyList.place(x=50,y=220)
    def __StartModules(self,event):
        """DriverとExcelPrintを起動する"""
        Detail_dictList =  Driver.ConnectDriver(self)
        if Detail_dictList != "":
            print(Detail_dictList)
        else:
            print("データがありません")
        return "break"

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
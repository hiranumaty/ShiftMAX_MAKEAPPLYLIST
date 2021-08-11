import datetime
from datetime import timedelta
"""これは期日の比較のためのパッケージ"""
def DateCompare1(parent,Data_bigin):
    """
    シフト勤務申請の期日フィルターのための関数
    """
    appendflg = True
    try:
        DATE = datetime.datetime.strptime(Data_bigin,"%Y年%m月%d")
        if parent.St_BEGINING.get() == '' and parent.St_FINAL.get()== '':
            appendflg = True
        else:
            if parent.St_BEGINING.get() != "":
                ComPare_BEGIN = datetime.datetime.strptime(parent.St_BEGINING.get(),"%Y/%m/%d")
                if DATE < ComPare_BEGIN:
                    appendflg = False
                    pass
            if parent.St_FINAL.get() != "":
                ComPare_FINAL = datetime.datetime.strptime(parent.St_FINAL.get(),"%Y/%m/%d")
                if DATE > ComPare_FINAL:
                    appendflg = False
        return  appendflg
    except ValueError as e:
        return False
def DateCompare2(parent,Data_bigin,Data_final):
    """休暇申請の期日フィルターのための関数"""
    """まず詳細データの一覧から日付のリストを作り出しそれがフィルターの開始と終了にかすっていればTrue"""
    appendflg = False
    try:
        StartDate = datetime.datetime.strptime(Data_bigin,"%Y年%m月%d")
        ENDDate = datetime.datetime.strptime(Data_final,"%Y年%m月%d")
        #入力がない場合は
        if parent.St_BEGINING.get() != '':
            ComPare_BEGIN = datetime.datetime.strptime(parent.St_BEGINING.get(),"%Y/%m/%d")
        else:
            ComPare_BEGIN = datetime.datetime.min
        if parent.St_FINAL.get() != '':
            ComPare_FINAL = datetime.datetime.strptime(parent.St_FINAL.get(),"%Y/%m/%d")
        else:
            ComPare_FINAL = datetime.datetime.max
        days_num = (ENDDate -StartDate).days +1
        Date_LIST = []
        for i in range(days_num):
            Date_LIST.append(StartDate + timedelta(days=i))
        
        for iterator in Date_LIST:
            if ComPare_BEGIN<=iterator<=ComPare_FINAL:
                appendflg = True
                break
        return appendflg
    except ValueError as e:
        return False
    

    

    
def EntryCompare(begin,final):
    """これは日付フィルターの入力が正しいかどうかを判定するためのもの"""
    flg = True
    if begin.get() != '' and final.get() != '':
        ComPare_BEGIN = datetime.datetime.strptime(begin.get(),"%Y/%m/%d")
        ComPare_FINAL = datetime.datetime.strptime(final.get(),"%Y/%m/%d")
        if ComPare_BEGIN>ComPare_FINAL:
            flg = False
    return flg

def ChangeDateFormat(DateString,mode):
    """YYYY/MM/DDを"%Y年%m月%d"に変化させる"""
    import locale
    locale.setlocale(locale.LC_CTYPE, "English_United States.932")
    if DateString != '':
        DATE = datetime.datetime.strptime(DateString[:10],"%Y/%m/%d")
    else:
        if mode =='Start':
            DATE = datetime.datetime.min
        else:
            DATE = datetime.datetime.max
    DATE_STRING =DATE.strftime("%Y年%m月%d")
    return DATE_STRING    
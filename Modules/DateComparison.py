import datetime
"""これは期日の比較のためのパッケージ"""
def DateCompare1(parent,Data_bigin):
    """
    シフト勤務申請の期日フィルターのための関数
    """
    appendflg = True
    if parent.St_BEGINING.get() == '' and parent.St_FINAL.get()== '':
        pass
    else:
        DATE = datetime.datetime.strptime(Data_bigin,"%Y年%m月%d")
        if parent.St_BEGINING.get() != "":
            ComPare_BEGIN = datetime.datetime.strptime(parent.St_BEGINING.get(),"%Y/%m/%d")
            if DATE < ComPare_BEGIN:
                appendflg = False
                pass
        if parent.St_FINAL.get() != "":
            ComPare_FINAL = datetime.datetime.strptime(parent.St_FINAL.get(),"%Y/%m/%d")
            if DATE > ComPare_FINAL:
                appendflg = False
                pass
    return  appendflg
def DateCompare2(parent,Data_bigin,Data_final):
    pass
def EntryCompare(begin,final):
    """これはtkinterの入力が正しいかどうかを判定するためのもの"""
    flg = True
    if begin.get() != '' and final.get() != '':
        ComPare_BEGIN = datetime.datetime.strptime(begin.get(),"%Y/%m/%d")
        ComPare_FINAL = datetime.datetime.strptime(final.get(),"%Y/%m/%d")
        if ComPare_BEGIN>ComPare_FINAL:
            flg = False
    return flg
    

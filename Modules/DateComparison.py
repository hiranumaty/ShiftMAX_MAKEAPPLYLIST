import datetime

def DateCompare1(parent,Data_bigin):
    """
    引数は 対象の開始日
    データの開始日とデータの終了日
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

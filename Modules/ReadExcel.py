import openpyxl

def ReadEmployeeList(parent):
    """parent.St_EMployeeListからファイル名を取得するようにすること"""

    wb = openpyxl.load_workbook(R"C:\Users\拓也\Desktop\testRead.xlsx")
    headers = None
    dic_list=[]

    for row in ws.rows:
        if row[0].row ==1:
            headers = row
        else:
            dic ={}
            for k,v in zip(headers,row):
                dic[k.value] = v.value
            dic_list.append(dic)
    return dic_list

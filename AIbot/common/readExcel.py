'''20180920'''


import xlrd


def text_format(text):
    return text.strip().replace(': ', ':').replace('(', '(')\
                .replace(')', '(').replace(',', ', ').replace('>', '>')

def get_excel_value(sheet, row, column):
    '''获取单元格具体数值，支持合并单元格'''
    for (r_low, r_high, c_low, c_high) in sheet.merged_cells:
        if r_low <= row < r_high and c_low <= column < c_high:
            return text_format(str(sheet.cell_value(r_low, c_low)))

    return text_format(str(sheet.cell_value(row, column)))

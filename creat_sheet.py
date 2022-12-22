import xlsxwriter

def creat_xls(check_type,whole_num, successful_checks):
    workbook = xlsxwriter.Workbook(f'{check_type}.xlsx')
    worksheet = workbook.add_worksheet()
    worksheet.write('A1', f'Checked links:')
    worksheet.write('B1', f'{whole_num}')
    worksheet.write('A2', f'Successful Checks:')
    worksheet.write('B2', f'{successful_checks}')
    workbook.close()
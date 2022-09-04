import csv


data = [
        ['376475TCh=byC'], 
        ['376478=uPM95R'], 
        ['376479l8z=fhe'],
        ['376481W3PYAug'], 
        ['376482J5IfOb='],
        ['376484k1kAhVe'], ['376486ZwA-Nk5'], ['376488Wlj=XUf'], ['376491WOEzkBW'], ['376493ubd16sG'], ['376495f0W3Weo'], ['376497AUfBQ=E'], ['37649991YXn=Y'], ['376501yUFNjAr'], ['376503h2HVCrq'], ['376505=zH=YRc'], ['376506X=GpdSx'], ['376508tpQ24-='], ['376511U=s5gC3'], ['376513dQ5=xbl']]



def save_to_csv(fileName, mode, contents):

    with open(f'{fileName}.csv', mode, encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerows(contents)
        print('数据保存成功.')


save_to_csv('test','a+',data)

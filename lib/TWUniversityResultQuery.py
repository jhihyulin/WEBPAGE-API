import sqlite3

def search(id):
    conn = sqlite3.connect('db/TW-University-result-query.sqlite')
    c = conn.cursor()
    data = c.execute('SELECT * FROM pdata WHERE id = ?', (id,)).fetchone()
    conn.close()
    if data is None:
        return None
    else:
        pass_li = data[1].replace('[', '').replace(']', '').split(', ')
        for i in range(len(pass_li)):
            if type(pass_li[i]) == str:
                pass_li[i] = int(pass_li[i].replace('\'', ''))
            else:
                pass_li[i] = int(pass_li[i])
        conn = sqlite3.connect('db/TW-University-result-query.sqlite')
        cw = conn.cursor()
        pass_li_sch_dep = {}
        for i in range(len(pass_li)):
            data = cw.execute('SELECT * FROM data WHERE id = ?', (pass_li[i],)).fetchone()
            pass_li_sch_dep.update({pass_li[i]: data[1].replace(' ', '') + ' ' + data[2].replace(' ', '')})
        conn.close()
        return pass_li_sch_dep

def tusearch(id):
    conn = sqlite3.connect('db/TW-University-result-query.sqlite')
    c = conn.cursor()
    data = c.execute('SELECT * FROM tupdata WHERE id = ?', (id,)).fetchone()
    conn.close()
    if data is None:
        return None
    else:
        pass_li = data[1].replace('[', '').replace(']', '').split(', ')
        for i in range(len(pass_li)):
            if type(pass_li[i]) == str:
                pass_li[i] = int(pass_li[i].replace('\'', ''))
            else:
                pass_li[i] = int(pass_li[i])
        conn = sqlite3.connect('db/TW-University-result-query.sqlite')
        cw = conn.cursor()
        pass_li_sch_dep = {}
        for i in range(len(pass_li)):
            data = cw.execute('SELECT * FROM tudata WHERE id = ?', (pass_li[i],)).fetchone()
            pass_li_sch_dep.update({pass_li[i]: data[1].replace(' ', '') + ' ' + data[2].replace(' ', '')})
        conn.close()
        return pass_li_sch_dep

def starsearch(id):
    conn = sqlite3.connect('db/TW-University-result-query.sqlite')
    c = conn.cursor()
    data = c.execute('SELECT * FROM starpdata WHERE id = ?', (id,)).fetchone()
    conn.close()
    if data is None:
        return None
    else:
        pass_li = data[1].replace('[', '').replace(']', '').split(', ')
        for i in range(len(pass_li)):
            if type(pass_li[i]) == str:
                pass_li[i] = int(pass_li[i].replace('\'', ''))
            else:
                pass_li[i] = int(pass_li[i])
        conn = sqlite3.connect('db/TW-University-result-query.sqlite')
        cw = conn.cursor()
        pass_li_sch_dep = {}
        for i in range(len(pass_li)):
            data = cw.execute('SELECT * FROM stardata WHERE id = ?', (pass_li[i],)).fetchone()
            pass_li_sch_dep.update({pass_li[i]: data[1].replace(' ', '') + ' ' + data[2].replace(' ', '')})
        conn.close()
        return pass_li_sch_dep

def searchname(id):
    conn = sqlite3.connect('db/TW-University-result-query.sqlite')
    c = conn.cursor()
    data = c.execute('SELECT * FROM pnamedata WHERE id = ?', (id,)).fetchone()
    conn.close()
    if data is None:
        return None
    else:
        return data[1]

def search_with_test_number(id):
    udata = search(int(id))
    tudata = tusearch(int(id))
    stardata = starsearch(int(id)) 
    name = searchname(int(id))
    data = {}
    if name is not None:
        data.update({'姓名': str(name)})
    if udata is None and tudata is None and stardata is None:
        data.update({'result': '查無資料'})
    else:
        if stardata is not None:
            data.update({'繁星推薦結果': {}})
            for i in stardata.keys():
                data['繁星推薦結果'].update({str(i).zfill(5): str(stardata[i])})
        if udata is not None:
            data.update({'大學個人申請第一階段結果': {}})
            for i in udata.keys():
                data['大學個人申請第一階段結果'].update({str(i).zfill(6): str(udata[i])})
        if tudata is not None:
            data.update({'科大四技申請第一階段結果': {}})
            for i in tudata.keys():
                data['科大四技申請第一階段結果'].update({str(i).zfill(6): str(tudata[i])})
    return data

import pymysql
#import charts
# 資料庫參數設定
db = pymysql.connect(host='localhost', port=3306, user='root', passwd='123qwe', db='company', charset='utf8')
try:
    # 建立Connection物件
    cursor = db.cursor()
    sql = 'SELECT * from users'
    #執行語法
    cursor.execute(sql)
    #選取第一筆結果
    data = cursor.fetchone()

    print (data)
    #關閉連線
    db.close()

except Exception as ex:
    print(ex)
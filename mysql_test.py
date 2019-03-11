import pymysql
db = pymysql.connect("162.211.225.42","test","123qwe","tot" )
# print(db)
# 使用cursor()方法获取操作游标 
cursor = db.cursor()

values = (
            2,
            3,
            '20190306000000',
            'area',
            'username',
            2,
            '20190306000000',
            'title',
            5,
            'content',
        )
# SQL 插入语句
# sql = "INSERT INTO forum( trade_id, sold_num, \
#                 post_time, area, username, userid, reg_time, title, price, content) \
#                 VALUES ( %s, %s,  %s,  '%s',  '%s', %s, %s, '%s', %s, '%s')" % \
#                 (1, 1, '20190306000000', 'qw', 'qwe', 123, '20190306000000', '2daw', 2, '2adar3')
# try:
   # 执行sql语句
sql = "INSERT INTO forum( trade_id, sold_num, \
                post_time, area, username, userid, reg_time, title, price, content) \
                VALUES ( %s, %s,  %s,  '%s',  '%s', %s, %s, '%s', %s, '%s')"
cursor.execute(sql % values)

# 执行sql语句
db.commit()
print('Done')
# except:
#    # 发生错误时回滚
#    db.rollback()
#    print('error')
 
# 关闭数据库连接
db.close()
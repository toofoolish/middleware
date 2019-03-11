import pymysql
db = pymysql.connect("162.211.225.42","test","123qwe","tot" )
# print(db)
# 使用cursor()方法获取操作游标 
# trade_id = Field()
# sold_num = Field()
# post_time = Field()
# area = Field()
# username = Field()
# userid = Field()
# reg_time = Field()
# title = Field()
# price = Field()
# content = Field()
cursor = db.cursor()
item = {
   'trade_id': 10660,
   'sold_num': 42,
   'post_time': '20180922122100',
   'area': '数据-情报',
   'username': 'fish',
   'userid': 44614,
   'reg_time': '20180204133300',
   'title': '珍藏的猫扇秘法',
   'price': 4.2,
   'content': '家传茅山秘法，不想让此神物在我手里断了传承，蒙羞。仅出三份定下相对高一点，因为想修行的人，必须法侣财地四样俱全。所以0.01BTC一份想请者自己看着买，几份都行。如果实在想学，可以留言留下你的生辰八字与我有缘者，请进随喜。我会修改金额。购买以后留地址。送一张灵符。因为是文字，随意不需要口传心授。将符挑一个好日子，摆大供。到时候我会教你怎么弄。一切随缘随喜。我可以引你入门，有没有这个缘分能修成，要看你自己。拍后跟我联系。想好再拍。拍了不退，提前声明。别拍了以后有找管理员整事。拍前确定好是否要真入门',
}
values = (
   item['trade_id'],
   item['sold_num'],
   item['post_time'],
   item['area'],
   item['username'],
   item['userid'],
   item['reg_time'],
   item['title'],
   item['price'],
   item['content'],
         )
# SQL 插入语句
# sql = "INSERT INTO forum( trade_id, sold_num, \
#                 post_time, area, username, userid, reg_time, title, price, content) \
#                 VALUES ( %s, %s,  %s,  '%s',  '%s', %s, %s, '%s', %s, '%s')" % \
#                 (1, 1, '20190306000000', 'qw', 'qwe', 123, '20190306000000', '2daw', 2, '2adar3')
# try:
   # 执行sql语句
sql = "insert into forum( trade_id, sold_num, \
                post_time, area, username, userid, reg_time, title, price, content) \
                values ( %s, %s,  %s,  '%s',  '%s', %s, %s, '%s', %s, '%s')"
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
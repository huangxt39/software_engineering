import json

from datetime import datetime, timedelta

book_borrow_time = '2012-11-19'
now = datetime.now()
print(str(now))
now = now+timedelta(days=1)-timedelta(seconds=1)
print(str(now))
print(str(now)[10:19])

book_borrow_time = datetime.strptime(book_borrow_time +" 24:00:00",'%Y-%m-%d %H:%M:%S')
# print( (book_borrow_time - now).days)
print(book_borrow_time)
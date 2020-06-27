# 并行工作进程数
workers = 3
# 指定每个工作者的线程数
threads = 1
# 工作模式协程
worker_class = "gevent"   # 采用gevent库，支持异步处理请求，提高吞吐量
# 监听内网端口80
bind = "0.0.0.0:80"
# # 设置守护进程,将进程交给supervisor管理
# daemon = 'true'
# 设置进程文件目录
# pidfile = '/var/run/gunicorn.pid'
# 设置访问日志和错误信息日志路径
accesslog = '/root/flask/gunicorn_acess.log'
errorlog = '/root/flask/gunicorn_info.log'
# 设置日志记录水平
loglevel = 'info'

reload=True
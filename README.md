# sky_main

# 创建的目的就是为了做一个自己常用工具的集合

由docker驱动

启动命令

* 构建镜像 `docker build -t sky_main .`

* 启动 redis `docker run --name redis-6379 -p 6379:6379`

* 启动 mysql `docker run --name mysql-3306 -p 3306:3306 -v /data/mysql:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=12345678 -e MYSQL_DATABASE=sky_main -d hypriot/rpi-mysql --character-set-server=utf8mb4 --collation-server=utf8mb4_unicode_ci`

* 启动 celery beat `docker run --name celery-beat --link mysql-3306:mysql --link redis-6379:redis -d flask_sky_main celery beat -A celery_worker.celery_app`

* 启动 celery worker `docker run --name celery-worker --link mysql-3306:mysql --link redis-6379:redis -d flask_sky_main celery -A celery_worker.celery_app worker --loglevel=info -E`

* 启动后端项目 `docker run --name sky_main-5011 -p 0.0.0.0:5011:8000 --link mysql-3306:mysql --link redis-6379:redis -d flask_sky_main gunicorn -w 2 -b 0.0.0.0:8000 manager:application`

> 如果之后学习到了编排，会替换。目前需要学习一下docker的命令
# BUAA_DB_2020Autumn

北航《数据库系统原理》课程2020秋课程设计

正在进行中……

## Requirements

- flask >= 1.0
- mysql-connector-python

建议使用virtualenv配置运行环境。

## 运行步骤

首先在本地启动MySQL服务，并建立一个用于该项目的数据库。

在cmd中激活对应的virtualenv后，在项目目录下执行下列语句：

```
set FLASK_APP=jiaowu
set FLASK_ENV=development
set FLASK_DEBUG=0
flask init-db
```

完成后执行flask run，根据提示在浏览器中访问链接（一般是http://127.0.0.1:5000/）即可。
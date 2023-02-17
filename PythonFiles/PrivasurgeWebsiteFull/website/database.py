from website import app 
from flask_mysqldb import MySQL


app.config['MYSQL_HOST'] = '45.79.53.24'
app.config['MYSQL_USER'] = 'remote_test'
app.config['MYSQL_PASSWORD'] = 'Nielsen7579'
app.config['MYSQL_DB'] = 'web_data'
mysql = MySQL(app)


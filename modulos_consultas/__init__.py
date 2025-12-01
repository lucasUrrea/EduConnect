import os
import pymysql

# If the project is configured to use MySQL via PyMySQL but the installed
# PyMySQL version is older than Django's recommended mysqlclient version
# check, set a compatible version string so Django's import-time check
# passes in development. This is a non-invasive development shim.
try:
	# ensure version info and __version__ are present and satisfy Django
	pymysql.version_info = getattr(pymysql, 'version_info', (1, 4, 3))
	pymysql.__version__ = getattr(pymysql, '__version__', '1.4.3')
except Exception:
	pass

pymysql.install_as_MySQLdb()

#!/usr/bin/python
#
#External auth script for ejabberd that enable auth against MySQL db with
#use of custom fields and table. It works with hashed passwords.
#Inspired by Lukas Kolbe script.
#Released under GNU GPLv3
#Requires Python 2
#Author: iltl. Contact: iltl@free.fr
#Author: Candid Dauth <cdauth@cdauth.eu>
#Version: 2015-12-20

########################################################################
#DB Settings
#Just put your settings here.
#Only add some modify of salt
########################################################################

import os
# db_host=os.environ['AUTH_MYSQL_HOST']
# db_user=os.environ['AUTH_MYSQL_USER']
# db_pass=os.environ['AUTH_MYSQL_PASSWORD']
# db_name=os.environ['AUTH_MYSQL_DATABASE']

db_host="localhost"
db_user="root"
db_pass="1234"
db_name="im_server"
salt_key_front= "YOUR SALT HERE"
salt_key_end= "YOUR SALT HERE"

# Get the password for a user. Use the placeholders `%(user)s`, `%(host)s`. Example: `SELECT password FROM users WHERE username = CONCAT(%(user)s, '@', %(host)s)`
db_query_getpass="SELECT password FROM users WHERE username = %(user)s"

# Update the password for a user. Leave empty to disable. Placeholder `%(password)s` contains the hashed password. Example: `UPDATE users SET password = %(password)s WHERE username = CONCAT(%(user)s, '@', %(host)s)`
db_query_setpass=os.getenv('AUTH_MYSQL_QUERY_SETPASS', '')

# Register a new user. Leave empty to disable. Example: `INSERT INTO users ( username, password ) VALUES ( CONCAT(%(user)s, '@', %(host)s), %(password)s )`
db_query_register="INSERT INTO users ( username, password ) VALUES ( %(user)s, %(password)s )"

# Removes a user. Leave empty to disable. Example: `DELETE FROM users WHERE username = CONCAT(%(user)s, '@', %(host)s)`
db_query_unregister=os.getenv('AUTH_MYSQL_QUERY_UNREGISTER', '')

# Format of the password in the database. Default is cleartext. Options are `crypt`, `md5`, `sha1`, `sha224`, `sha256`, `sha384`, `sha512`. `crypt` is recommended.
db_hashalg=os.getenv('AUTH_MYSQL_HASHALG', 'sha256')

########################################################################
#Setup
########################################################################

#import sys, logging, struct, hashlib, MySQLdb, crypt, random, atexit, time
import sys, logging, struct, hashlib, MySQLdb,random, atexit, time

sys.stderr = open('./extauth_err.log', 'a')
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s',
                    filename='./extauth_err.log',
                    filemode='a')
MySQLdb.paramstyle = 'pyformat'
logging.info("ej connect")
try:
	database=MySQLdb.connect(db_host, db_user, db_pass, db_name)
except:
	print("error");
	logging.error("Unable to initialize database, check settings!")
	time.sleep(10)
	sys.exit(1)

@atexit.register
def close_db():
	database.close()

logging.info('extauth script started, waiting for ejabberd requests')

class EjabberdInputError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)


########################################################################
#Declarations
########################################################################

def ejabberd_in():
	logging.debug("trying to read 2 bytes from ejabberd:")

	input_length = sys.stdin.read(2)
	# logging.debug(input_length)

	if len(input_length) is not 2:
		logging.debug("ejabberd sent us wrong things!")
		raise EjabberdInputError('Wrong input from ejabberd!')

	logging.debug('got 2 bytes via stdin: %s'%input_length)

	(size,) = struct.unpack('>H', input_length)
	logging.debug('size of data: %i'%size)

	income=sys.stdin.read(size).split(':', 4)
	logging.debug("incoming data: %s"%income)

	return income


def ejabberd_out(bool):
	logging.debug("Ejabberd gets: %s" % bool)

	token = genanswer(bool)

	logging.debug("sent bytes: %#x %#x %#x %#x" % (ord(token[0]), ord(token[1]), ord(token[2]), ord(token[3])))

	sys.stdout.write(token)
	sys.stdout.flush()


def genanswer(bool):
	answer = 0
	if bool:
		answer = 1
	token = struct.pack('>hh', 2, answer)
	return token


def password_hash(password, old_password=None):
	if old_password == None:
		old_password = '$6$'+''.join(random.choice("0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ./") for i in range(16))
    #unix crypt methond mark at first to
	if db_hashalg == "crypt":
		return 0
		#return crypt.crypt(password, old_password)
	elif db_hashalg == "":
		return password
	else:
		hasher = hashlib.new(db_hashalg)
		hasher.update(password)
		return hasher.hexdigest()


def get_password(user, host):
	database.ping(True)
	with database as dbcur:
		dbcur.execute(db_query_getpass, {"user": user, "host": host})
		data = dbcur.fetchone()
		return data[0] if data != None else None;


def isuser(user, host):
	# print(get_password(user, host))
	return get_password(user, host) != None


def auth(user, host, password):
	db_password = get_password(user, host)
	if db_password == None:
		logging.debug("Wrong username: %s@%s" % (user, host))
		return False
	else:
		if password_hash(password, db_password) == db_password:
			return True
		else:
			logging.debug("Wrong password for user: %s@%s" % (user, host))
			return False


def setpass(user, host, password):
	if db_query_setpass == "":
		return False

	database.ping(True)
	with database as dbcur:
		dbcur.execute(db_query_setpass, {"user": user, "host": host, "password": password_hash(password)})
		if dbcur.rowcount > 0:
			return True
		else:
			logging.info("No rows found for user %s@%s to update password" % (user, host))
			return False


def tryregister(user, host, password):
	if db_query_register == "":
		return False

	if isuser(user, host):
		logging.info("Could not register user %s@%s as it already exists." % (user, host))
		return False

	database.ping(True)
	with database as dbcur:
		dbcur.execute(db_query_register, {"user": user, "password": password_hash(password)})
		return True


def removeuser(user, host):
	if db_query_unregister == "":
		return False

	database.ping(True)
	with database as dbcur:
		dbcur.execute(db_query_unregister, {"user": user, "host": host})
		if dbcur.rowcount > 0:
			return True
		else:
			logging.debug("No rows found to remove user %s@%s" % (user, host))
			return False


def removeuser3(user, host, password):
	if db_query_unregister == "":
		return False

	return auth(user, host, password) and removeuser(user, host)


########################################################################
#Main Loop
########################################################################

exitcode=0
#test code of query user password
while True:
	logging.debug("start of infinite loop")

	try:
		ejab_request = ejabberd_in()
	except EOFError:
		logging.exception("EOFError")
		break
	except Exception as e:
		logging.exception("Exception occured while reading stdin")
		raise

	logging.debug('operation: %s' % (":".join(ejab_request)))

	op_result = False
	logging.info(ejab_request)
	try:
		if ejab_request[0] == "auth":
			#user, host, password
			op_result = auth(ejab_request[1], ejab_request[2], salt_key_front+ejab_request[3]+salt_key_end)
		elif ejab_request[0] == "isuser":
			op_result = isuser(ejab_request[1], ejab_request[2])
		elif ejab_request[0] == "setpass":
			op_result = setpass(ejab_request[1], ejab_request[2], salt_key_front+ejab_request[3]+salt_key_end)
		elif ejab_request[0] == "tryregister":
			op_result = tryregister(ejab_request[1], ejab_request[2], salt_key_front+ejab_request[3]+salt_key_end)
		elif ejab_request[0] == "removeuser":
			op_result = removeuser(ejab_request[1], ejab_request[2])
		elif ejab_request[0] == "removeuser3":
			op_result = removeuser3(ejab_request[1], ejab_request[2], salt_key_front+ejab_request[3]+salt_key_end)
	except Exception:
		logging.exception("Exception occured")

	ejabberd_out(op_result)
	logging.debug("successful" if op_result else "unsuccessful")

logging.debug("end of infinite loop")
logging.info('extauth script terminating')
database.close()
sys.exit(exitcode)

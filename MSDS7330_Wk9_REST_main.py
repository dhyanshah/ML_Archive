#!flask/bin/python
from flask import Flask
import MySQLdb
from flask import jsonify 
from flask import Flask, abort, request 
import logging



app = Flask(__name__)

@app.route('/')
def index():
    return "This is a sample rest service"


#### Rest Service definition for returning the list of actors from sakila.actor table
@app.route('/api/v1.0/getCustomerList', methods=['GET'])
def getCustomerList():

	global query_result;
	try:
		# Create connection to the MYSQL instance running on the local machine
		## Change the credentials to match your system
		
		logging.warning("Inside getCustomerList()")
		connection = MySQLdb.Connection(host='localhost', user='dshah2009', passwd='Shriji20977', db='EcommerceDB')
		cursor = connection.cursor()
		logging.warning("Connection with DB established")
		cursor.execute("select * from CustomerTable;")
		query_result = [ dict(line) for line in [zip([ column[0] for column in cursor.description], row) for row in cursor.fetchall()] ]
	except Exception, e:
		print "Error [%r]" % (e)
		#sys.exit(1)
	finally:
		if cursor:
			cursor.close()
	
	## Return the list of actors as a json object
	return jsonify({'CustomerList': query_result})
	
	
#### Rest Service definition for returning the actor record for a given id.

@app.route('/api/v1.0/getOrderDetails/<orderNumber>', methods=['POST','GET'])
def getOrderDetails(orderNumber):
	
	global query_result;
	try:
		# Create connection to the MYSQL instance running on the local machine
		## Change the credentials to match your system
		connection = MySQLdb.Connection(host='localhost', user='msds', passwd='msds', db='EcommerceDB')
		cursor = connection.cursor()
		logging.warning("Connection established")
		## Read the input json from the incoming request
		reqObj = request.json
		logging.warning("Request Object \n %s"%reqObj)

		
		queryStr = "select * from OrderHeader  oh , OrderLine ol \
					where ol.OrderHeader_OrderNumber=oh.OrderNumber and oh.OrderNumber = %d;"%int(orderNumber)
		logging.warning(queryStr)
		cursor.execute(queryStr)
		query_result = [ dict(line) for line in [zip([ column[0] for column in cursor.description], row) for row in cursor.fetchall()] ]
	except Exception, e:
		logging.warning("Error [%r]" % (e))
		#sys.exit(1)
	finally:
		if cursor:
			cursor.close()
			
	return jsonify({'OrderDetails': query_result})


## Starts the server for serving Rest Services 
if __name__ == '__main__':
    app.run(debug=False)
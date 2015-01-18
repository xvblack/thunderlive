import json
from threading import Lock

def return_json(f):

	def decorated(*args, **kwargs):
		result = f(*args, **kwargs)
		# TODO: check type
		return json.dumps(result)

	return decorated
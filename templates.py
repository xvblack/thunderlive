from utility import return_json

def render_application(application):
	result = {}
	result["name"] = application.name()
	result["streams"] = [render_stream(s) for s in application.streams()]
	result["nstreams"] = len(result["streams"])
	print result
	return result

def render_stream(stream):
	result = {}
	result["name"] = stream.name()
	result["time"] = stream.uptime()
	result["meta"] = stream.meta()
	result["clients"] = [render_client(c) for c in stream.clients()]
	result["nclients"] = len(result["clients"])
	print result
	return result

def render_client(client):
	result = {}
	result["address"] = client.address()
	result["time"] = client.uptime()
	result["version"] = client.version()
	print result
	return result

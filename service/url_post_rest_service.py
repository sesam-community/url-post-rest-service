import json
import requests
from flask import Flask, Response
import os
import logger
import cherrypy

app = Flask(__name__)
logger = logger.Logger('url-post-rest-service')
url = os.environ.get("baseurl")
apiKey = os.environ.get("apiKey")
error_is_embedded = os.environ.get("error_is_embedded")
embedded_error_message_property = os.environ.get("embedded_error_message_property")
embedded_error_code_property = os.environ.get("embedded_error_code_property")


@app.route("/<path:path>", methods=["GET"])
def get(path):
    requesturl = "{0}{1}".format(url, path)
    headers = {'Content-Type': 'application/json'}
    data = {'apiKey': apiKey}

    logger.info("Downloading data from: '%s'", requesturl)

    try:
        response = requests.post(requesturl, data=json.dumps(data), headers=headers)

        #Error messages may be sent as data with http status code 200 and not as exceptions (http status code 500 for example).
        #Assumes that if the length of the response is greater than 300 characters, real data is returned.
        if response.status_code == 200 and error_is_embedded and len(response.text) < 300:
            response_data = json.loads(response.text)
            if len(response_data) == 1:
                error_entity = response_data[0]
                if error_entity[embedded_error_code_property] != 200:
                    raise Exception(error_entity[embedded_error_message_property])

    except Exception as e:
        logger.warn("Exception occured when download data from '%s': '%s'", requesturl, e)
        raise

    return Response(response=response.text, mimetype='application/json')


if __name__ == '__main__':
    cherrypy.tree.graft(app, '/')

    # Set the configuration of the web server to production mode
    cherrypy.config.update({
        'environment': 'production',
        'engine.autoreload_on': False,
        'log.screen': True,
        'server.socket_port': 5001,
        'server.socket_host': '0.0.0.0'
    })

    # Start the CherryPy WSGI web server
    cherrypy.engine.start()
    cherrypy.engine.block()
    
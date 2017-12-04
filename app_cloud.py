from flask import Flask, request, Response
import requests
import json
import sys
import logging

MEC_APP_CLOUD_PORT = 65000

MEC_CMS_IP = "localhost"
MEC_CMS_PORT = 0x17d2
MEC_MSCATALOG_IP = "mscatalog"
MEC_MSCATALOG_PORT = 60617

app_cloud = Flask(__name__)

logging.basicConfig(filename='/opt/logs/appcloud.log', level=logging.DEBUG,
                    format='%(asctime)-15s %(levelname)-8s %(filename)-16s %(lineno)4d %(message)s')

@app_cloud.route('/api/v1.0/app_cloud/<developer_id>/<app_id>/<cloudlet_id>/<client_id>',methods=['POST'])
def provision_application(developer_id, app_id, cloudlet_id,client_id):
    # Call provision api of llo's cms with payload as client_id

    payload = None
    #Get Extension data, if any
    #Only VMI extensions available now
    extension_json = None
    try:
        extension_json = request.get_json()
    #Catching a generic exception for the time being
    except Exception as ex:
        print('No extension data received. Continuing...')

    is_microservice = False
    headers = {'content-type': 'application/json'}
    url = "http://%s:%d/microservicecatalog/microservice/%s" %(MEC_MSCATALOG_IP,MEC_MSCATALOG_PORT,app_id)
    response = requests.get(url, data=json.dumps(payload), headers=headers)
    if response.status_code == 200:
        is_microservice = True
        print "Microservice catalog response => %s" %response.text

    payload = {}
    payload['clientId'] = client_id

    if is_microservice:
        payload['microservice'] = 'yes'

    if extension_json:
        payload['extensions'] = extension_json

    headers = {'content-type': 'application/json'}
    url = "http://%s:%d/api/v1.0/llo/cms/%s/%s/%s" %(MEC_CMS_IP,MEC_CMS_PORT,developer_id,app_id,cloudlet_id)
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    if response.status_code == 200:
        print "Application provisioned; response => %s" %response.text
        return response.text
    else:
        return Response(status=response.status_code)

@app_cloud.route('/api/v1.0/app_cloud/<developer_id>/<app_id>/<cloudlet_id>/<client_id>/<uuid>',methods=['DELETE'])
def terminate_application(developer_id, app_id, cloudlet_id, client_id, uuid):
    payload = {'clientId':client_id}
    headers = {'content-type': 'application/json'}
    # Call terminate api of llo's cms with deployment-id (uuid)
    url = "http://%s:%d/api/v1.0/llo/cms/%s/%s/%s/%s" %(MEC_CMS_IP,MEC_CMS_PORT,developer_id,app_id,cloudlet_id,uuid)
    response = requests.delete(url, data=json.dumps(payload), headers=headers)
    if response.status_code == 200:
        return response.text
    else:
        return Response(status=response.status_code)

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: %s <llo_cms_ip> <ms_catalog_ip>" % sys.argv[0])
        sys.exit(1)

    MEC_CMS_IP = sys.argv[1]
    MEC_MSCATALOG_IP = sys.argv[2]

    app_cloud.run(host="0.0.0.0", port=MEC_APP_CLOUD_PORT, threaded=True)


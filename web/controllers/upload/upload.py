from flask import Blueprint,request , jsonify
from application import db,app
from common.libs.UploadService import UploadService
import json,re

route_upload = Blueprint('upload_page', __name__)

@route_upload.route("/ueditor",methods = [ "GET","POST" ])
def ueditor():

	req = request.values
	action = req['action'] if 'action' in req else ''

	if action == "config":
		root_path = app.root_path
		config_path = "{0}/web/static/plugins/ueditor/upload_config.json".format( root_path )
		with open( config_path,encoding="utf-8" ) as fp:
			try:
				config_data =  json.loads( re.sub( r'\/\*.*\*/' ,'',fp.read() ) )
			except:
				config_data = {}
		return  jsonify( config_data )

	if action == "uploadimage":
		return uploadImage()

	# if action == "listimage":
	# 	return listImage()

	return "upload"

def uploadImage():
    resp = {'status': 'SUCCESS' , 'url':'', 'title': '', 'original': ''}
    file_target = request.files
    upfile = file_target['upfile'] if 'upfile' in file_target else ''
    if upfile is None:
        resp['state'] = "上传失败"
        return jsonify(resp)

    ret = UploadService.uploadByFile(upfile)
    return jsonify(resp)
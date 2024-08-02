from flask import request, jsonify
from . import api_blueprint

from services.CrawlService import Crawl
import json
from services.DatabaseService import DatabaseService

@api_blueprint.route('/fetch', methods=['GET'])
def fetch_data():
    print("fetching data")
    with open('config.json',encoding="utf8") as json_file:
        jsondata = json.load(json_file)
    items=[]
    for config in jsondata:
        if config["active"]==0:
            print("not active")
            continue
        mainlink=config["mainlink"]
        items1 = Crawl(mainlink, config)
        #loop through the items and add them to the database
        db = DatabaseService()
        for item in items1:
            db.create_project(item['name'], item['province'],item['district'], item['price'], item['area'], item['legal'], item['image'])
        items.append(items1)

    return jsonify(items)

#get data from database
@api_blueprint.route('/get', methods=['GET'])
def get():
    db = DatabaseService()
    page=request.args.get('page')
    itemperpage=request.args.get('itemperpage')
    projects = db.get_all_project()
    if page is not None and itemperpage is not None:
        start=(int(page)-1)*int(itemperpage)
        end=start+int(itemperpage)
        projects=projects[start:end]
    
    return jsonify(projects)

#sample data
@api_blueprint.route('/create', methods=['GET'])
def create():
    db = DatabaseService()
    db.create_sample_data()
    return 'Create Project'
#delete all data
@api_blueprint.route('/delete', methods=['GET'])
def delete():
    #db.drop_all()
    return 'Delete all data'

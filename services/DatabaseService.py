from models import db
from models.model import Project

class DatabaseService:
    def create_project(self, name, province,district, price, area, legal, image):
        project = Project(name, province,district ,price, area, legal, image)
        db.session.add(project)
        db.session.commit()
        return 'Create Project'

    def get_all_project(self):
        projects = Project.query.all()
        return [project.serialize() for project in projects]
    def delete_all(self):
        db.drop_all()
        return 'Delete all data'
    
    def create_sample_data(self):
        db.create_all()
        project1 = Project('Huy', 'Hanoi','Cau Giay', 100000, 100, 'Legal', 'image')
        db.session.add(project1)
        db.session.commit()
        return 'Create Project'
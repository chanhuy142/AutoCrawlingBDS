from . import db
class Project(db.Model):
    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000))
    price = db.Column(db.String(1000))
    area = db.Column(db.String(200))
    legal = db.Column(db.String(200))
    province = db.Column(db.String(200))
    district = db.Column(db.String(200))
    image = db.Column(db.String(1000))
    def __init__(self, name, province,district, price, area, legal,image):
        self.name = name
        self.province = province
        self.district = district
        self.price = price
        self.area = area
        self.legal = legal
        self.image = image
    def __repr__(self):
        return '<Project %r>' % self.name
    #convert object to json
    def serialize(self):
        return {
            'name': self.name,
            'province': self.province,
            'district': self.district,
            'price': self.price,
            'area': self.area,
            'legal': self.legal,
            'image': self.image,
        }
    


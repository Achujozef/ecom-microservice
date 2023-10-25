# from flask import Flask, redirect, request, render_template
# from flask_sqlalchemy import SQLAlchemy
# from cloudinary.uploader import upload
# from cloudinary.utils import cloudinary_url
# import cloudinary

# app = Flask(__name__)

# cloudinary.config(
#     cloud_name='dkocmifft',
#     api_key='479515447813437',
#     api_secret='IEX3f2GQWssMdy7MmheqF9Rd8Cc'
# )

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banner.db'
# db = SQLAlchemy(app)

# class Banner(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     public_id = db.Column(db.String(100), nullable=False)
#     # Add more fields for your banner
# with app.app_context():
#     # Create the database tables
#     db.create_all()

# @app.route('/')
# def index():
#     banners = Banner.query.all()
#     return render_template('index.html', banners=banners)

# @app.route('/upload', methods=['POST'])
# def upload_banner():
#     if request.method == 'POST':
#         image = request.files['image']
#         if image:
#             response = upload(image)
#             public_id = response['public_id']
#             # Create a new Banner record with the public_id and other details
#             banner = Banner(public_id=public_id)
#             db.session.add(banner)
#             db.session.commit()
#             print(banner)
#     return redirect('/')

# @app.route('/delete/<int:id>', methods=['POST'])
# def delete_banner(id):
#     banner = Banner.query.get(id)
#     if banner:
#         # Delete the banner image from Cloudinary
#         cloudinary_url(banner.public_id, format='png')
#         db.session.delete(banner)
#         db.session.commit()
#     return redirect('/')

# if __name__ == '__main__':
#     app.run(debug=True)
#     app.run()
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from cloudinary.uploader import upload
from cloudinary.utils import cloudinary_url
import cloudinary

app = Flask(__name__)

cloudinary.config(
    cloud_name='dkocmifft',
    api_key='479515447813437',
    api_secret='IEX3f2GQWssMdy7MmheqF9Rd8Cc'
)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banner.db'
db = SQLAlchemy(app)

class Banner(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(100), nullable=False)
    # Add more fields for your banner

@app.route('/uploadbanner', methods=['POST'])
def upload_banner():
    if request.method == 'POST':
        image = request.files['image']
        if image:
            response = upload(image)
            public_id = response['public_id']
            banner = Banner(public_id=public_id)
            db.session.add(banner)
            db.session.commit()
            return jsonify({"message": "Banner uploaded successfully", "banner_id": banner.id}), 201
    return jsonify({"error": "No image uploaded"}), 400

@app.route('/deletebanner/<int:id>', methods=['DELETE'])
def delete_banner(id):
    banner = Banner.query.get(id)
    if banner:
        cloudinary_url(banner.public_id, format='png')
        db.session.delete(banner)
        db.session.commit()
        return jsonify({"message": "Banner deleted successfully"}), 200
    return jsonify({"error": "Banner not found"}), 404

@app.route('/getbanners', methods=['GET'])
def get_banners():
    print("Njan Flask Ethi")
    banners = Banner.query.all()
    banner_list = [{"id": banner.id, "public_id": banner.public_id} for banner in banners]
    return jsonify(banner_list)

if __name__ == '__main__':
    app.run(debug=True)

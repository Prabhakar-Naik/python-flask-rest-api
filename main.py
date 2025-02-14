from flask import Flask, request, jsonify
from flask_restful import Api, Resource, abort, reqparse, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)


class VideoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100),nullable= False)
    views = db.Column(db.Integer, nullable= False)
    likes = db.Column(db.Integer, nullable = False)
    
    def __repr__(self):
        return f"Video(name = {name}, views = {views}, likes = {likes})"
    

# db.create_all()

""" Example 1 """
# names = {"prabha":{"name":"prabha","age":25,"gender":"male"},
#          "sudha":{"name":"sudha","age":30,"gender":"male"},
#          "priya":{"name":"priya","age":22,"gender":"female"}}

# class HelloWorld:
    
#     def get(self,name):       
#         return {"data":"Hello Universe","record":names[name]}

""" Example 2 """  
# videos = {"youtube":{"video":"python","tutorial":"Biggener","time":"2 hours"},
#           "udemy":{"video":"java","tutorial":"Advance","time":"1 hour"},
#           "coursera":{"video":"java script","tutorial":"Biggenner","time":"3 hours"}}

# class Video(Resource):
#     def get(self,video_id):
#         return {"data":videos[video_id]}

""" Example 3 """

video_put_args = reqparse.RequestParser()
video_put_args.add_argument("name", type=str, help = "Name of the video is required", required = True)
video_put_args.add_argument("views", type=int, help = "Views of the video", required = True)
video_put_args.add_argument("likes", type=int, help = "Likes on the video", required = True)


video_update_args = reqparse.RequestParser()
video_update_args.add_argument("name", type=str, help = "Name of the video is required")
video_update_args.add_argument("views", type=int, help = "Views of the video")
video_update_args.add_argument("likes", type=int, help = "Likes on the video")


# videos = {}
resource_fields = {
    'id':fields.Integer,
    'name':fields.String,
    "views":fields.Integer,
    "likes":fields.Integer
}

# def abort_if_videos_doesnot_exist(video_id):
#     if video_id not in videos:
#         abort(404, message="Video id not valid")
        
# def abort_if_video_exist(video_id):
#     if video_id in videos:
#         abort(409, message= "Video Already Exist with this Id...")

class Video(Resource):
    @marshal_with(resource_fields)
    def get(self,video_id):
        # abort_if_videos_doesnot_exist(video_id)
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, message = "could not find video with given id")
        return result

class VideoList(Resource):
    @marshal_with(resource_fields)
    def get(self):
        videos = VideoModel.query.all()
        if not videos:
            abort(404, message = "could not find any records")
        else:
            return videos
            # return jsonify([video.json() for video in videos])
    
    @marshal_with(resource_fields)
    def put(self,video_id):
        # abort_if_video_exist(video_id)
        args = video_put_args.parse_args()
        # videos[video_id] = args
        result = VideoModel.query.filter_by(id=video_id).first()
        if result:
            abort(409,message = "Video id taken..")
        video = VideoModel(id=video_id, name = args['name'], views = args['views'], likes = args['likes'])
        db.session.add(video)
        db.session.commit()
        
        return video, 201
    
    @marshal_with(resource_fields)
    def patch(self, video_id):
        args = video_update_args.parse_args()
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, message = "video doesn't exist, cannot update")
        
        if args['name']:
            result.name = args['name']
        if args['views']:
            result.views = args['views']
        if args['likes']:
            result.likes = args['likes']
        
        
        db.session.commit()
        return result
    
    def delete(self,video_id):
        result = VideoModel.query.filter_by(id=video_id).first()
        del result[video_id]
        return ' ',204


# api.add_resource(HelloWorld,"/helloworld/<string:name>")
# api.add_resource(Video,"/videos/<string:video_id>")
api.add_resource(Video,"/videos/<int:video_id>")
api.add_resource(VideoList, '/videos/getAll') 


if __name__ == "__main__":
    app.run(debug=True)
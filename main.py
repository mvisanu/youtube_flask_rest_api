from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class VideoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    views = db.Column(db.Integer, nullable=False)
    likes = db.Column(db.Integer, nullable=False)
    
      
    def __repr__(self):
        return f"Video(name={self.name}, views={self.views}, likes={self.likes})"

db.create_all()

video_put_args = reqparse.RequestParser()
video_put_args.add_argument("name", type=str, help="Name of video is required", required=True)
video_put_args.add_argument("views", type=int, help="Views of video", required=True)
video_put_args.add_argument("likes", type=int, help="Likes of video", required=True)

#User can send what ever argument they want not requiring all
video_update_args = reqparse.RequestParser()
video_update_args.add_argument("name", type=str, help="Name of video is required")
video_update_args.add_argument("views", type=int, help="Views of video")
video_update_args.add_argument("likes", type=int, help="Likes of video")

resource_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'views': fields.Integer,
    'likes': fields.Integer
}

videos = {}
def abort_if_video_id_doesnt_exist(video_id):
    if video_id not in videos:
        abort(404, message="Could not find video...")

def abort_if_video_exits(video_id):
    if video_id in videos:
        abort(409, message="Video already exists with that ID...")
        


class Video(Resource):
    
    @marshal_with(resource_fields)
    def get(self, video_id):
        #abort_if_video_id_doesnt_exist(video_id)
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, message=f"Could not find video with that id...{str(video_id)}")
        return result
    
    @marshal_with(resource_fields) #serialize the object
    def put(self, video_id):
        #abort_if_video_exits(video_id)
        #args = video_put_args.parse_args()
        #videos[video_id] = args
        #video = VidelModel(id)
        args = video_put_args.parse_args()
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(409, message="Video with that id exists...")   
                  
        video = VideoModel(id=video_id, name=args['name'], likes=args['views'], views=args['likes'])
        db.session.add(video)
        #db.session.flush()
        db.session.commit()
        return video, 201
    
    @marshal_with(resource_fields) 
    def patch(self, video_id):
        args = video_update_args.parse_args()
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, message="Video does not exist, cannot update...")
            
        if args['name']:
            result.name = args['name']
        if args['views']:
            result.views = args['views']
        if args['likes']:
            result.likes = args['likes']
               
        db.session.commit()
        
        return result, 200
        
    
    def delete(self, video_id):
        #abort_if_video_id_doesnt_exist(video_id)
        #del videos[video_id]
        result = VideoModel.query.filter_by(id=video_id).delete()
        db.session.commit()
        
        return '', 204
   
    
api.add_resource(Video, "/video/<int:video_id>")



if __name__== "__main__":
    app.run(debug=True)
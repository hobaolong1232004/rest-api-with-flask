from flask import Flask,request
from flask_restful import Api,Resource,reqparse,abort,fields,marshal_with # fields and marshal to serialize
                                                                     # data from db into json format
from flask_sqlalchemy import SQLAlchemy   # use sqlite database to store data

app=Flask(__name__) # create flask app
api=Api(app) # put flask app into api
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///database.db' # config database to flask app
db=SQLAlchemy(app) # create db using sqlachemy for app flask

class VideoModel(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100),nullable=False)
    views=db.Column(db.Integer,nullable=False)
    likes=db.Column(db.Integer,nullable=False)

    def __repr__(self):
        return f"Video(name={self.name},likes={self.likes},views={self.views}"

#db.create_all() # create database on first  initialize not run on second time to avoid overrided

# names={"long":{"age":22,"gender":"M"},"binh":{"age":23,"gender":"F"}}
# class HelloWorld(Resource): # demo resource
#     def get(self,name): # test request
#         return names[name]
#     def post(self):
#         return {"data":"posted"}
# api.add_resource(HelloWorld,"/helloworld/<string:name>") # register it as a resource to api, /helloworld is a root of this url
#                                           # <type:agrument name> is parameter to pass in


videos_put_args=reqparse.RequestParser() # use reqparse alternative to request.form from client
videos_put_args.add_argument('name',type=str,help="type in name of the video required",required=True)
videos_put_args.add_argument('views',type=str,help="type in views of the video")
videos_put_args.add_argument('likes',type=str,help="type in likes of the video")

# def abort_if_videoid_notexist(video_id):
#     if video_id not in videos:
#         abort(404,message="Video id not exist") # avoid crash  on sever and print error back to client
#
# def abort_if_videoid_exist(video_id):
#     if video_id in videos:
#         abort(409,message="Video id already exist") # avoid crash  on sever and print error back to client

resource_fields={
    'id':fields.Integer(),'name':fields.String(),'views':fields.Integer(),'likes':fields.Integer()
}
class Video(Resource):
    @marshal_with(resource_fields) # use decorator with this function to convert data to json format
                                   # from previous get result
    def get(self,video_id): # get request
        result=VideoModel.query.filter_by(id=video_id).first() # return object instance of VideoModel match sql result
        if not result:
            abort(404,message='video id not exist')
        return result

    @marshal_with(resource_fields)
    def put(self,video_id): # put request
        # access data from request sent
        #print(request.form['likes']) # use request.form to access data sent from client
        args=videos_put_args.parse_args() # alternative use reqparse and print information for client
        result = VideoModel.query.filter_by(id=video_id).first()
        if result:
            abort(409, message="Video id already exist...")
        video=VideoModel(id=video_id,name=args['name'],views=args['views'],likes=args['likes'])
        db.session.add(video) # add this object to database
        db.session.commit() # save this action
        return video,201 # you can send status code response after return for client
                                    # , 201 stand for created

    @marshal_with(resource_fields)
    def patch(self,video_id): # update request
        args=videos_put_args.parse_args()
        result = VideoModel.query.filter_by(
            id=video_id).first()  # return object instance of VideoModel match sql result
        if not result:
            abort(404, message='video id not exist,cant update')
        if args['name']:
            result.name = args['name']
        if args['views']:
            result.views = args['views']
        if args['likes']:
            result.likes = args['likes']

        db.session.commit() # save db

        return result
    def delete(self,video_id):
        result = VideoModel.query.filter_by(
            id=video_id).first()  # return object instance of VideoModel match sql result
        if not result:
            abort(404, message='video id not exist,cant delete')
        db.session.remove(result)
        return '',204 # 204 is deleted success


api.add_resource(Video,"/videos/<string:video_id>")

if __name__== "__main__":
    app.run(debug=True)

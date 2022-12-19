import requests

base="http://127.0.0.1:5000/"


# response=requests.get(base+"helloworld/long")
data=[{"name":"long","views":87,"likes":20},{"name":"binh","views":44,"likes":20},{"name":"long22","views":44,"likes":20},
      {"name":"sd","views":12,"likes":55},{"name":"ww","views":55,"likes":44}]

# for i in range(len(data)):
#
#     response_video=requests.put(base+"videos/"+str(i),data=data[i]) # put
#     print(response_video.json())

# response_video=requests.delete(base+"videos/0")
# print(response_video)
# input()

response_video=requests.patch(base+"videos/1",data={"name":"baolongng","views":9999,"like":884}) #
print(response_video.json())

response_video=requests.get(base+"videos/1") #
print(response_video.json())


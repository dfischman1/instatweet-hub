from instagram import client, subscriptions
import pythontwitter2
import storage
import app


def user_pics(uname):
    result = ""
    result = storage.getHash(uname)
    print "Your instagram hashtag:" + result
    clientstuff = getInstaInfo(uname)
    client_id = clientstuff[0]
    client_token = clientstuff[1]
    pics = get_pics(client_id, client_token, result)
    return pics
    
    


def get_pics(user_id, access_token, user_hashtag):
    instagram_client = client.InstagramAPI(access_token=access_token)
    recent_media, next = instagram_client.user_recent_media(user_id=user_id, count = 5)
    photos = []
    tags = []
    for media in recent_media:
        tags = []
        if hasattr(media, 'tags'):
            for tag in media.tags:
                tags.append(tag.name.lower())
            if user_hashtag in tags:
                photos.append(media.images['standard_resolution'].url)
    return photos

    

        #images = []
        #tags = []
        #for tag in media.tags:
         #   if tag == app.user_hashtag:
          #      images[tag] = media.standard_resolution.url
    #print images
    #return images

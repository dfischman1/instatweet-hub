from instagram import client, subscriptions
import pythontwitter2
import storage
import app


def user_pics(uname):
    result = ""
    result = storage.getHash(uname)
    clientstuff = storage.getInstaInfo(uname)
    client_id = clientstuff[0]
    client_token = clientstuff[1]
    pics = get_pics(client_id, client_token, result)
    return pics

def oauth():
    try:
        code = request.values.get('code')
    except:
        res = "Missing Code"
        return res
    try:
        code = request.values.get('code')
        access_token, instagram_user = instagram_client.exchange_code_for_access_token(code)
    except:
        res = "no token"
        return res
    user_id = instagram_user['id']
    user_token = access_token
    print user_id + user_hashtag + 'YAY!'
    res = instagramhub.get_pics(user_id, user_token, user_hashtag)
    print taggedimages
    return res


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

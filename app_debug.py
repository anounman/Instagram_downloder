from flask import Flask , request , render_template , url_for , send_file , jsonify
import requests
from datetime import datetime
import os
#make a cookie.py file and set your cookie data there
from cookie import *
download_link = ""
title = ""
app = Flask(__name__)


@app.route('/', methods=["POST", "GET"])
def download():
    # try:
        url = str(request.args.get("link"))
        url = url.split("?")
        url = str(url[0])+"?__a=1"
        print(url)
        responce = requests.get(url , cookies=crsf_data).json()
        state = True
        try:
            try:
                    like = responce["graphql"]["shortcode_media"]["edge_media_preview_like"]["count"]
                    comment = responce["graphql"]["shortcode_media"]["edge_media_preview_comment"]["count"]
                    # caption = responce["graphql"]["shortcode_media"]["edge_media_to_caption"]["edges"][0]["node"]["text"]
                    username = responce["graphql"]["shortcode_media"]["owner"]["username"]
            except Exception as e:
                print("Error>"+e)
                state = False
            video_link = responce["graphql"]["shortcode_media"]["video_url"]
            image_url = responce["graphql"]["shortcode_media"]["display_resources"]
            image_url = image_url[2].get("src")
            like = responce["graphql"]["shortcode_media"]["edge_media_preview_like"]["count"]
            if video_link != None:
                if state != False:

                   return  jsonify(type="video",src_image=str(image_url),like=str(like),username=str(username),comments=str(comment), link=str(video_link) , error="Click On The Download Button For Download The Video")
                else:
                    state = True
                     
                    return jsonify(error="unable to fetch post info",link=str(video_link))
            else:
                error = "This media is not downloadbel"
                return jsonify(error)
        except Exception:
            like = responce["graphql"]["shortcode_media"]["edge_media_preview_like"]["count"]
            image_url = responce["graphql"]["shortcode_media"]["display_resources"]
            image_url = image_url[2].get("src")
            if image_url != None:
                if state != False:
                    return jsonify(type="image",src_image=str(image_url),error=None,like=str(like),username=str(username),comment=str(comment),link=str(image_url))
                else:
                    return jsonify(error="unable to fetch post info",link=str(image_url))
            else:
                error = "This media is not downloadbel"
                return jsonify(error)
    # except Exception as e:
        # print(e)
        # error = "We are unabel to fetch your data"
        # return  str(e)

if __name__ == '__main__':
    app.run(debug=True , port=80 , host="192.168.1.101")

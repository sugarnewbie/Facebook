import requests
import csv
import pandas as pd


def get_list_cards(list_id):
    url = "https://api.trello.com/1/lists/"+str(list_id)+"/cards?attachments=true&attachment_fields=all&labels=true"

    query = {
        'key': 'bfa52e2d772f57fce7d6a60861927bdf',
        'token': '7895538dfc20c1327747f71ba76951f0f25864eb11971a014b5ce65d94b98235'
    }

    response = requests.request(
        "GET",
        url,
        params=query
    )

    data_out = []
    for item in response.json():
        idAttachmentCover = item['idAttachmentCover']
        imageCover = [x['url'] for x in item['attachments'] if x['id'] == idAttachmentCover][0]
        imageThumb = [{'url':x['url'],'name':x['name']} for x in item['attachments'] if x['id'] != idAttachmentCover]
        data_out.append({
            "thumbs": imageThumb,
            "image": imageCover.strip(),
            "name": item["name"].strip().replace("\n","").replace("\t",""),
            "tags": item["desc"].strip().replace("\n","").replace("\t",""),
            "label": [i["name"] for i in item["labels"]][0]
            })

    return data_out

def filterThumb(listKeyDesign,listKeyThumb,image):
    imageName = image["name"]
    for key in listKeyDesign:
        if key in imageName:
            return ("design_1",image["url"])
    for key in listKeyThumb:
        if key in imageName:
            return (listKeyThumb[key],image["url"])
    return (None,image["url"])

def _run(list_id):
    data = get_list_cards(list_id)
    listKeyDesign = ["BESE","PPOLO","AOP-Baseball","HWSH2"]
    listKeyThumb = {
        "---front": "image_1",
        "---back": "image_2",
        "Detail": "image_3",
    }
    data_out = []

    for item in data:
        temp = {
            "title": item['name'],
            "handle": item['name'].split(" ")[-1],
            "tags": item['tags'],
            "image_main": item['image'],
            "product_type": item['label'],
        }

        index_thumb = 0
        for image in item["thumbs"]:
            (_type,imageUrl) = filterThumb(listKeyDesign,listKeyThumb,image)
            print(_type,imageUrl)

            if _type is not None:
                temp[_type] = imageUrl
            else:
                index_thumb +=1
                temp["image_"+str(index_thumb)] = imageUrl
        data_out.append(temp)
    return data_out


_main_data = []
list_ids=[
    "609202c9ee5ea436b0c8b221",
    "609202c9ee5ea436b0c8b223",
    "60db053e98dcf856d01e53ea",
]
for list_id in list_ids:
    _main_data += _run(list_id)

# keys = data_out[0].keys()
# print(keys)
# csv.DictWriter(x, keys)
# print(x)
df = pd.DataFrame(_main_data)
df.to_csv('shopbase.csv',index=False)


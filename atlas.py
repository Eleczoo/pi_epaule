import base64
import json
import random
from io import BytesIO

import requests
from loguru import logger
from PIL import Image


def send_pick_request(x, y):
    pick_url = "http://lifesciencedb.jp/bp3d/API/pick"
    pick_payload = {
        "Part": [
            {"PartName": "humerus", "PartColor": "0000FF", "PartOpacity": 0.7},
            {"PartName": "scapula", "PartColor": "0000FF", "PartOpacity": 0.7},
            {"PartName": "clavicle", "PartColor": "0000FF", "PartOpacity": 0.7},
            {"PartName": "supraspinatus", "PartColor": "FFFF00", "PartOpacity": 0.7},
            {"PartName": "brachial plexus", "PartColor": "FF0000", "PartOpacity": 0.7},
            {"PartName": "axillary nerve", "PartColor": "FF0000", "PartOpacity": 0.7},
            {"PartName": "musculocutaneous nerve", "PartColor": "FF0000", "PartOpacity": 0.7},
            {"PartName": "dorsal scapular nerve", "PartColor": "FF0000", "PartOpacity": 0.7},
            {"PartName": "long thoracic nerve", "PartColor": "FF0000", "PartOpacity": 0.7},
            {"PartName": "suprascapular nerve", "PartColor": "FF0000", "PartOpacity": 0.7},
            {"PartName": "nerve to subclavius", "PartColor": "FF0000", "PartOpacity": 0.7},
            {"PartName": "lateral pectoral nerve", "PartColor": "FF0000", "PartOpacity": 0.7},
            {"PartName": "medial pectoral nerve", "PartColor": "FF0000", "PartOpacity": 0.7},
            {"PartName": "upper subscapular nerve", "PartColor": "FF0000", "PartOpacity": 0.7},
            {"PartName": "lower subscapular nerve", "PartColor": "FF0000", "PartOpacity": 0.7},
            {"PartName": "thoracodorsal nerve", "PartColor": "FF0000", "PartOpacity": 0.7},
            {"PartName": "pectoralis minor", "PartColor": "FFFF00", "PartOpacity": 0.7},
            {"PartName": "rhomboid major", "PartColor": "FFFF00", "PartOpacity": 0.7},
            {"PartName": "rhomboid minor", "PartColor": "FFFF00", "PartOpacity": 0.7},
            {"PartName": "levator scapulae", "PartColor": "FFFF00", "PartOpacity": 0.7},
            {"PartName": "serratus anterior", "PartColor": "FFFF00", "PartOpacity": 0.7},
            {"PartName": "subscapularis", "PartColor": "FFFF00", "PartOpacity": 0.7},
            {"PartName": "infraspinatus", "PartColor": "FFFF00", "PartOpacity": 0.7},
            {"PartName": "teres minor", "PartColor": "FFFF00", "PartOpacity": 0.7},
            {"PartName": "teres major", "PartColor": "FFFF00", "PartOpacity": 0.7},
            {"PartName": "deltoid", "PartColor": "FFFF00", "PartOpacity": 0.7},
            {"PartName": "biceps brachii", "PartColor": "FFFF00", "PartOpacity": 0.7},
            {"PartName": "coracobrachialis", "PartColor": "FFFF00", "PartOpacity": 0.7},
            {"PartName": "trapezius", "PartColor": "FFFF00", "PartOpacity": 0.7},
            {"PartName": "latissimus dorsi", "PartColor": "FFFF00", "PartOpacity": 0.7},
            {"PartName": "tendon of long head of biceps brachii", "PartColor": "D2B48C", "PartOpacity": 0.7},
            {"PartName": "tendon of long head of triceps brachii", "PartColor": "D2B48C", "PartOpacity": 0.7},
            {"PartName": "axillary fascia", "PartColor": "00FF00", "PartOpacity": 0.7},
            {"PartName": "pectoral fascia", "PartColor": "00FF00", "PartOpacity": 0.7},
            {"PartName": "deltoid fascia", "PartColor": "00FF00", "PartOpacity": 0.7},
            {"PartName": "infraspinous fascia", "PartColor": "00FF00", "PartOpacity": 0.7},
            {"PartName": "supraspinous fascia", "PartColor": "00FF00", "PartOpacity": 0.7},
            {"PartName": "subscapular fascia", "PartColor": "00FF00", "PartOpacity": 0.7},
            {"PartName": "glenohumeral ligaments", "PartColor": "A9A9A9", "PartOpacity": 0.7},
            {"PartName": "coracohumeral ligament", "PartColor": "A9A9A9", "PartOpacity": 0.7},
            {"PartName": "transverse humeral ligament", "PartColor": "A9A9A9", "PartOpacity": 0.7},
            {"PartName": "coracoacromial ligament", "PartColor": "A9A9A9", "PartOpacity": 0.7},
            {"PartName": "acromioclavicular ligament", "PartColor": "A9A9A9", "PartOpacity": 0.7},
            {"PartName": "costoclavicular ligament", "PartColor": "A9A9A9", "PartOpacity": 0.7},
            {"PartName": "glenoid labrum", "PartColor": "808080", "PartOpacity": 0.7},
        ],
        "Window": {"ImageWidth": 500, "ImageHeight": 500},
        "Pick": {"ScreenPosX": x, "ScreenPosY": y},
    }
    logger.debug("send pick request")
    logger.debug("📤 Pick Request Payload:", json.dumps(pick_payload, separators=(",", ":")))
    pick_response = requests.post(pick_url, data=json.dumps(pick_payload), headers={"Content-Type": "application/json"})
    if pick_response.status_code != 200:
        logger.error("❌ Pick request failed with status:", pick_response.status_code)
        logger.error("Response text:", pick_response.text)
        exit()

    try:
        result = pick_response.json()
    except json.JSONDecodeError:
        logger.error("❌ Failed to decode JSON from response:")
        logger.error("Raw response:", pick_response.text)
        exit()

    logger.debug("✅ Pick API Result:")
    logger.debug(json.dumps(result, indent=2))
    result = pick_response.json()
    part_names = list({pin["PinPartName"] for pin in result.get("Pin", [])})
    '''
    image_url = "http://lifesciencedb.jp/bp3d/API/image"
    image_payload = {
        "Part": [{"PartName": "anatomical entity", "PartColor": "F0D2A0", "PartOpacity": 0.1}],
        "Window": {"ImageWidth": 500, "ImageHeight": 500},
    }
    '''
    to_return =[]
    for name in part_names:
        '''
        image_payload["Part"].append(
            {"PartName": name, "PartColor": "".join([random.choice("0123456789ABCDEF") for _ in range(6)]), "PartOpacity": 0.7}
        )
        '''
        to_return.append(name)
    '''
    print("image response ")
    print("URL:", image_url)
    print("📤 Pick response Payload:", json.dumps(image_payload, separators=(",", ":")))
    image_response = requests.post(image_url, data=json.dumps(image_payload), headers={"Content-Type": "application/json"})

    logger.debug("Image response status code:", image_response.status_code)
    logger.debug("Image response headers:", image_response.headers)
    logger.debug("Image response content (first 500 chars):", image_response.text[:1000])
    if image_response.ok:
        try:
            response_json = image_response.json()
            data_uri = response_json["data"]

            base64_str = data_uri.split(",")[1]
            image_data = base64.b64decode(base64_str)
            image = Image.open(BytesIO(image_data))
            image.show()

        except (KeyError, ValueError, json.JSONDecodeError) as e:
            logger.error("Error extracting image from response:", e)
    else:
        logger.error("Image request failed with status:", image_response.status_code)
    '''
    return to_return
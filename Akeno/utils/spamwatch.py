import requests

from Akeno.utils.logger import LOGS
from config import FEDBAN_API_KEY as api_key


async def auto_post_gban(user_id, reason):
    url = "https://randydev-ryuzaki-api.hf.space/user/fedban"
    headers = {"accept": "application/json", "api-key": api_key}
    payload = {
        "user_id": user_id,
        "hashtag": "#Spammer",
        "reason": reason,
    }
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code != 200:
        LOGS.error("Error response status")
        return "Error response status"
    response_data = response.json()
    is_banned = response_data["randydev"].get("is_banned")
    get_message = response_data["randydev"].get("message")
    return is_banned, get_message

async def auto_check_gban(user_id):
    url = "https://randydev-ryuzaki-api.hf.space/user/get-fedban"
    headers = {"accept": "application/json", "api-key": api_key}
    payload = {"user_id": user_id}
    response = requests.get(url, json=payload, headers=headers)
    if response.status_code != 200:
        LOGS.error("Error response status")
        return "Error response status"
    response_data = response.json()
    is_banned = response_data["randydev"].get("is_banned")
    reason = response_data["randydev"].get("reason")
    return [is_banned, reason]

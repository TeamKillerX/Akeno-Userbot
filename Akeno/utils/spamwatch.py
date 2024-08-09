import requests
from Akeno.utils.logger import LOGS

async def auto_post_gban(user_id, reason):
    url = "https://randydev-ryuzaki-api.hf.space/user/fedban"
    headers = {"accept": "application/json", "api-key": api_key}
    payload = {
        "user_id": user_id,
        "hashtag": "#Spammer",
        "reason": reason,
    }
    response = requests.post(url, json=payload, headers=headers)
    if not response.status_code != 200:
        LOGS.error("Error response status")
        return "Error response status"
    response_data = response.json()
    return response_data["is_banned"]

### Akeno-Userbot
![Screenshot_20240809-132044_Chrome](https://github.com/user-attachments/assets/2baee270-ae25-44f4-9cc4-101e89db51d4)

### Deploy on VPS:
```console
@root: git clone https://github.com/TeamKillerX/Akeno-Userbot
@root: cd Akeno-Userbot
@root: pip3 install -r requirements.txt
@root: mv .env_sample .env
@root: nano .env
@root: python3 -m Akeno
```
### Support Hosting (bypass)
- Heroku
- Railway app
- Render
- Koyeb
- Bypass server API + Userbot

### Docker Run
```Dockerfile
docker run -it -p 7860:7860 --platform=linux/amd64 \
	-e API_ID="YOUR_VALUE_HERE" \
	-e API_HASH="YOUR_VALUE_HERE" \
	-e SESSION="YOUR_VALUE_HERE" \
	-e HUGGING_TOKEN="YOUR_VALUE_HERE" \
	-e GOOGLE_API_KEY="YOUR_VALUE_HERE" \
	-e FEDBAN_API_KEY="YOUR_VALUE_HERE" \
	rendyprojects/akeno:dev
```

### IMPORTANT NOTICE:

This project is no longer maintained. __Use at your own risk__.

### Custom Modules
- you can check [`custom-modules`](https://github.com/TeamKillerX/custom_modules)

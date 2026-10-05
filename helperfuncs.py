def delete_message(channel, msgid):
    path = f"channels/{channel}.json"

    with open(path, "r") as f:
        lines = f.readlines()

    with open(path, "w") as f:
        for line in lines:
            if json.loads(line).get("msgid") != msgid:
                f.write(line)

def find_message(channel, msgid):
    with open(f"channels/{channel}.json", "r") as f:
        for line in f:
            message = json.loads(line)
            if message.get("msgid") == msgid:
                return message
    return None

def savetofile(channel, data):
    path = Path("channels", f"{channel}.json")  
    with open(path, "a") as file:
        file.write(data)
        file.write("\n")

def retrievelines(channel, count):
    path = Path("channels", f"{channel}.json") 
    with open(path, 'r', encoding='utf-8') as f:
        lines = [json.loads(line) for line in deque(f, maxlen=count)]
    return lines

def chatauth(userid, username, wsobj):
    authpairs.append((userid, username, wsobj))

def makejsonerror(input):
    return {"cmd": "error", "message": input}

def makejsonsuccess(input):
    return {"cmd": "success", "message": input}

def validate(token):
    url = 'https://cami.barfpile.dev/validate'
    payload = {'token': token}
    response = requests.post(url, json=payload)

    if response.status_code == 200:
        return (response.json())["message"]
    else:
        return False
    pass
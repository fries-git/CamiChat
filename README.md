# CamiChat  
this is rushed cause i gtg like right now, but basically,  

## Sends
connect to the ws server: official at chat.barfpile.dev.  
`{"cmd": "auth","token": "cami token}`  
Once authed:  
`{"cmd": "new_message","channel": "general","body": "Hello world!}`  
This might also work but I literally havent tested lol.  
`{"cmd": "delete_message","channel": "general","msgid": "msg123..."}`
This works to get n message history gonna be capped to 20 soon:  
`{"cmd": "gethistory","channel": "general","length": 50}`

## Recieve
When you first connect (customizable message across servers gonna make a basic little language to embed timestamps and stuff like <H> becomes the current server hour):  
`{"motd": "><> Good morning! Welcome to fries dungeon! <><"}`  
Whenever someone sends a message it literally sends down:  
`{"cmd": "new_message", "username": username, "userid": user, "channel": channel, "timestamp": time.time(), "id": msgid, "body": content}`  
If someone joins:
`{"cmd": "connect","id": "...","username": "fries}`  
but it can also be disconnect if they leave.  

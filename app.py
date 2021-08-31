import asyncio
import websockets
import json 

USERS = set()
URI_="0.0.0.0"
PORT_=5590

class Sys():
    def __init__(self):
        self.values = {
            "id" : 0,
            "name": "sistema"
        }

def getargs(path):
    try:
        args = path.split("?")[-1]
        args = args.split("&")
        values = {}
        for a in args:
            v = a.split("=")
            values[v[0]] = v[1]
        
        return values
    except:
        return ""
    
async def register(websocket):
    USERS.add(websocket)
    # print(USERS)
    
async def unregister(websocket):
    try:
        USERS.remove(websocket)
        # await broadcast("%s saiu!" % websocket.values['name'])
    except:
        print("Erro ao remover usuário!")
    
async def broadcast(websocket, message):
    if USERS:  
        data = json.dumps({
            "user": websocket.values['name'],
            "id": websocket.values['id'],
            "message": message
        }, indent=4,)
        await asyncio.wait([user.send(data) for user in USERS])

async def private(websocket, message, id):
    if USERS:  
        print("private to: %s" %str(id))
        data = json.dumps({
            "user": websocket.values['name'],
            "id": websocket.values['id'],
            "message": message
        }, indent=4)
        for user in USERS:
            if str(user.values['id'])==str(id):
                await user.send(data)

async def serv(websocket, path):
    await register(websocket)
    websocket.values = getargs(path)
    print("%s entrou!" % websocket.values['name'])
    # await broadcast(Sys(), "%s entrou!" % websocket.values['name'])
    while(1):
        try:
            message = await websocket.recv()
            message = json.loads(message)
            if 'private' in message:
                await private(websocket,message['message'], message['private'])
            else:
                await broadcast(websocket, message['message'])
        except Exception as e:
            print(e)
            await unregister(websocket)
            break

if __name__ == '__main__':
    print("Server: %s:%s" %(URI_, str(PORT_)))
    start_server = websockets.serve(serv, URI_, PORT_)

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
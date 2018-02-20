# Tools used by both server and client
def formalizedata(msg, cmd):
    return msg.replace(cmd, "").replace("\n", "")

def split_data(data):
    try:
        return data.split('\n')
    except:
        return data.decode().split('\n')

def sendAll(clients, msg):
    for client in clients:
        client.send(msg)


def sendError(client, msg):
    client.send("ERROR " + msg)

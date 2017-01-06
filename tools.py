# Tools used by both server and client
def formalizedata(msg, cmd):
    return msg.replace(cmd, "").replace("\n", "")

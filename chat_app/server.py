import socket
from json import dump, load
import threading

chats = {}
lock = threading.Lock()


def ld():
    with open("chat/serv.json", "r") as f:
        return load(f)


user = ld()


def dmp(user):
    with open("chat/serv.json", "w") as f:
        dump(user, f)


def id_ld():
    with open("chat/id.json", "r") as f:
        return load(f)


generate = {"generate": id_ld()}


def id_dmp(generate):
    with open("chat/id.json", "w") as f:
        dump(generate["generate"], f)


def sign(password, user, ID, generate):
    if len(password) > 10:
        return "Error: Password exceeds maximum length of 10 characters."
    with lock:
        generate["generate"] += 1
        ids = str(generate["generate"])
    user[ids] = [password, []]
    ID["ID"] = ids

    return f"signed in as {ids}"


def login(id, password, user, ID):
    if id not in user:
        return "Error: User ID does not exist."
    elif password != user[id][0]:
        return "Error: Invalid password."
    ID["ID"] = id
    return f"logined as {id}"


def msg(reciever, chat, id, user):
    frozen = frozenset((id, reciever))
    if reciever not in user:
        return "Error: Recipient user ID does not exist."
    elif reciever in user[id][1]:
        return "Error: Message blocked. You have blocked this user."
    elif id in user[reciever][1]:
        return "Error: Message rejected. Recipient has blocked you."

    with lock:
        if frozen in chats:
            chats[frozen] += f"{id} : {chat}\n"
        else:
            chats[frozen] = f"{id} : {chat}\n"
    return "sended"


def bloc(reciever, id, user):
    if reciever not in user or reciever == id:
        return "Error: Invalid user ID or self-block operation."
    with lock:
        if reciever in user[id][1]:
            return "Error: User is already blocked"
        user[id][1].append(reciever)
    return "Blocked"


def unblock(reciever, id, user):
    with lock:
        if reciever not in user[id][1]:
            return "Error: Invalid user ID or self-unblock operation."
        user[id][1].remove(reciever)
    return "Unblocked"


def history(reciever, id, user):
    frozen = frozenset((id, reciever))

    if reciever not in user or reciever == id:
        return "Error: Invalid user ID or self-block operation."
    elif frozen not in chats:
        return "Error: Invalid user ID or self-block operation."

    return chats[frozen]


def server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind(("0.0.0.0", 5000))
        server.listen()
        server.settimeout(50)
        while True:
            try:
                connection, _ = server.accept()
            except socket.timeout:
                print("Shuting down")
                break
            threading.Thread(target=handle, args=(connection,)).start()


def handle(connection):
    with connection:
        ID = {"ID": None}

        while True:
            ops = {
                "s": [sign, 1, user, ID, generate],
                "l": [login, 2, user, ID],
                "m": [msg, 2, ID["ID"], user],
                "b": [bloc, 1, ID["ID"], user],
                "u": [unblock, 1, ID["ID"], user],
                "h": [history, 1, ID["ID"], user],
            }
            raw = connection.recv(1024).decode()
            if raw == "":
                break
            data = raw.split(" ", ops[raw[0]][1])

            if len(data) != ops[data[0]][1]:
                connection.sendall("Error: Invalid request format.".encode())
                continue
            op = data[0]
            if ID["ID"] is None:
                ops = {
                    "s": [sign, 0, user, ID, generate],
                    "l": [
                        login,
                        1,
                        user,
                        ID,
                    ],
                }

            if op not in ops:
                connection.sendall(
                    "Error: Unknown operation. Request command is not recognized by the server.".encode()
                )
                continue
            connection.sendall(
                f"server : {ops[op][0](*data[1:],*ops[op][2:])}\n".encode()
            )


server()
dmp(user)
id_dmp(generate)

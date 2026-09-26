from hashlib import pbkdf2_hmac
from os import urandom
from json import dump, load

vault = []


def save(promt, vault):
    with open("storage.json", "w") as f:
        dump(vault, f)
    print(promt)


def loadin():
    global vault
    try:
        with open("storage.json", "r") as f:
            vault = load(f)
    except FileNotFoundError:
        vault = []


def data():
    while True:
        raw = input("\nDomain | Username/Name | Password : ").split("|", 2)

        if raw == ["q"]:
            quits()

        elif len(raw) != 3:
            print("Invalid. Requirement is 3")
            continue
        domain, username, password = map(str.strip, raw)
        salt = urandom(16)
        return [
            domain,
            username,
            pbkdf2_hmac("sha512", password.encode(), salt, 100000).hex(),
            salt.hex(),
        ]


def number(prompt, vault):
    while True:
        try:
            rawd = int(input(f"Enter ID of the password to be {prompt} : "))
            index = rawd - 1
            vault[index]
            return index
        except (ValueError, IndexError):
            print("Invalid Number")


def add(vault):
    vault.append(data())
    save("Added!", vault)


def delete(vault):
    vault.pop(number("deleted!", vault))
    save("Deleted", vault)


def edit(vault):
    vault[number("edited!", vault)] = data()
    save("Updated!", vault)


def verification(vault):
    while True:
        index = number("verified", vault)
        id = index + 1
        password = input(f"Enter the password of {id} : ").strip()
        if password == "q":
            quits()
        elif (
            pbkdf2_hmac(
                "sha512", password.encode(), bytes.fromhex(vault[index][3]), 100000
            ).hex()
            == vault[index][2]
        ):
            print(f"{password} is the right password for ID {id}")
            break
        print("wrong password")


def view(vault):
    print(f"\n{'ID':<8} {'Domain':<20} {'Username/Gmail':<25} {'Password'}\n{"─"*65}")
    for i, data in enumerate(vault, start=1):
        print(f"{i:<8} {data[0]:<20} {data[1]:<25} ********")


def quits():
    exit()


def main():
    loadin()
    while True:
        if not vault:
            options = {"1": add, "2": quits}
        else:
            options = {
                "1": add,
                "2": delete,
                "3": edit,
                "4": view,
                "5": quits,
                "6": verification,
            }
        option = input(
            "\n"
            + "\n".join(f"{i}. {v.__name__.title()}" for i, v in options.items())
            + "\n: "
        )
        if option not in options:
            print("Invalid")
            continue
        options[option](vault)


main()

import base64
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import tools
import sys
import os 
import re
import json
def run(acc_fname='acc.txt'):
    """
    Initializes the environment and gets the user password.  Responsible for running the entire program.
    """ 
    usr_select = 'a'
    acc_path = os.path.join(sys.path[0], 'acc.txt')
    salt_path = os.path.join(sys.path[0], 'salt.txt')
    fernet = initialize(acc_path, salt_path)
    while usr_select != 'a' or usr_select != 'b':
        
        usr_info = decrypt_info(acc_path, fernet)

        if usr_info is not None:
            usr_select = input("Would you like to: (a) add a password, (b) change one of [acc, uname, pass, all], (c) delete one, or (q) quit? ")
            if usr_select == 'a':
                acc_entry = get_acc_and_pword()
                usr_info.append(acc_entry)
                encrypt_info(acc_path, fernet, usr_info)

            elif tools.check_modifier_input(usr_select):
                index = tools.get_integer_input_for_list(len(usr_info))
                usr_info = modify_entry(usr_info, index, usr_select.split(' ')[1])
                encrypt_info(acc_path, fernet, usr_info)

            elif usr_select == 'c':
                inf_to_remove = tools.get_integer_input_for_list(len(usr_info))
                usr_info.pop(inf_to_remove)
                encrypt_info(acc_path, fernet, usr_info)

            elif usr_select == 'q':
                return
            
            else:
                print("Invalid input")
                
        else:
            fernet = initialize(acc_path, salt_path)
        
    

def set_password():
    pword = bytes(input("set password pls -- this is permanent do not forgot or you will lose data in acc.txt: "), 'utf-8')
    return pword

def initialize(acc_path, salt_path):

    if not os.path.exists(salt_path):
        salt = os.urandom(16)
        with open(salt_path, 'wb') as f:
            f.write(salt)
    else:
        with open(salt_path, 'rb') as f:
            salt = f.read()

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    pword = set_password() if not os.path.exists(acc_path) else get_password()
    key = base64.urlsafe_b64encode(kdf.derive(pword))
    fernet = Fernet(key)
    if not os.path.exists(acc_path):
        first_entry = get_acc_and_pword()
        encrypt_info(acc_path, fernet, [first_entry])

    return Fernet(key)

def get_password():
    pword = input("Enter your password pls: ")
    return bytes(pword, 'utf-8')

def get_acc_and_pword():
    acc_inf = input("Enter website account, name and pword (separated by a space): ")

    while len(acc_inf.split(' ')) != 3:
        print("Invalid input. Try again.")
        acc_inf = input("Enter website account, name and pword (separated by a space): ")
    
    acc_inf = acc_inf.split(' ')
    acc_entry = {"acc": acc_inf[0], "uname": acc_inf[1], "pass": acc_inf[2]}
    return acc_entry

def modify_entry(usr_info, index, type):
    if type == 'all':
        usr_info[index] = get_acc_and_pword()
        return usr_info
    elif type == 'uname':
        prompt = 'user name'
    elif type == 'acc':
        prompt = 'account name'
    else:
        prompt = 'pass'
    new_input = input(f"Enter your new {prompt}: ")
    usr_info[index].update({type:new_input})
    return usr_info

def decrypt_info(acc_path, fernet):

    with open(acc_path, 'rb') as f:
        token = f.read()

    try:
        usr_info = fernet.decrypt(token)
        
    except InvalidToken:
        print("You have not entered the right password")
        return None
    usr_info = json.loads(usr_info.decode('utf-8').replace("'", '"'))
    for i, element in enumerate(usr_info):
        print(f'{i} -- acc: {element["acc"]} \t uname: {element["uname"]} \t pass: {element["pass"]}')
    return usr_info

def encrypt_info(acc_path, fernet, info):
    with open(acc_path, 'wb') as f:
        token = fernet.encrypt(bytes(str(info), 'utf-8'))
        f.write(token)

if __name__=="__main__":
    run()
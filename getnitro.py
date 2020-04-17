import requests
import random
import json

def file_writer(filename, data):
    opnr = open(filename, "a+")
    opnr.write(data)
    opnr.close()


def randomChar():
    rand = random.randint(0, 3)
    
    if rand == 1:
        return random.randint(65, 90)
    elif rand == 0:
        return random.randint(48, 57)
    
    return random.randint(97, 122)


def gencodes():
    st = ""
    for x in range(0, 16):
        st += chr(randomChar())
    
    return st


def proxy_select():
    opnr = open("webreq.json", "r")
    loads = json.load(opnr)
    opnr.close()
    return random.choice(loads["proxy"])


def randUserAgent():
    opnr = open("webreq.json", "r")
    loads = json.load(opnr)
    opnr.close()
    return random.choice(loads["User-Agent"])


if __name__ == "__main__":
    proxy_get = proxy_select()
    proxy = {
        "https":proxy_get,
        "http":proxy_get
    }

    useragent = {"User-Agent":randUserAgent()}
    print("[+]Using proxy: {0}".format(proxy_get))
    while True:
        code = gencodes()
        try:
            req = requests.get("https://discordapp.com/api/v6/entitlements/gift-codes/{0}?with_application=false&with_subscription_plan=true".format(code), useragent, proxies=proxy)
            readJson = json.loads(req.content)
            
            if "message" not in readJson:
                file_writer("foundnitro.txt", "\n"+code+"\n")
                print("[+]Found Nitro Code: {0}".format(code))
            else:
                if readJson["message"] != "Unknown Gift Code" and readJson["message"] != "You are being rate limited.":
                    file_writer("foundnitro.txt", code)
                    print("[+]Found Nitro Code: {0}".format(code))
                elif readJson["message"] == "You are being rate limited.":
                    print("[-]You are being rate limited.")
                    print("[+]Changing proxy")
                    proxy_get = proxy_select()
                    proxy["https"] = proxy_get
                    proxy["http"] = proxy_get
                    print("[+]Proxy: {0}".format(proxy_get))
                else:
                    print("[-]Invalid Code: {0}".format(code))
        except Exception as error:
            print("[-]Error Occurred")
            print("[+]Changing Proxy")
            proxy_get = proxy_select()
            proxy["https"] = proxy_get
            proxy["http"] = proxy_get
            print("[+]Proxy: {0}".format(proxy_get))
            pass
        

import json

if __name__ == '__main__':
    req_key = "main"
    with open('requirement.json', 'r') as fp:
        req = json.load(fp)
        req = req[req_key]

    print(req)
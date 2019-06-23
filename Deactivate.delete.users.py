import requests, json

# GENERAL INFO:
token = ""
tenant = "muraru.okta"
headers = {"Authorization": "SSWS " + token,
           "Accept": "application/json",
           "Content-Type": "application/json"}
first_name = 0
last_name = 0
deactivate_flow = 0

def main():
    global deactivate_flow
    deactivate_flow = 0
    login = input("User's login: ")

    content = getUser(login)

    # print the API call's body
    # print(json.dumps(content, indent=4, sort_keys=True))

    id = content["id"]
    print("User's ID is:\t\t\t\t {:>30}".format(id))

    email = content["profile"]["email"]
    print("User's Email is:\t\t\t {:>30}".format(email))

    fn = content["profile"]["firstName"]
    print("User's firstName value is:\t {0:>30}".format(fn))
    global first_name
    first_name = fn

    ln = content["profile"]["lastName"]
    print("User's lastName value is:\t {:>30}".format(ln))
    global last_name
    last_name = ln

    print("User's status is\t\t\t {:>30}\n".format(content["status"]))

    # print the API call's body (second way):
    # print(json.dumps(getUser(login), indent=4, sort_keys=True))

    if content["status"] != "DEPROVISIONED":
        choice = input("Deactivate user and then delete?\n(y/n)")
        if choice == "y" or choice == "Y":
            deactivateUser(id)
            deleteUser(id)
        else:
            choice = input("Do you want to just deactivate the user?\n(y/n)")
            deactivate_flow = 1
            if choice == "y" or choice == "Y":
                deactivateUser(id)
            else:
                main()
    else:
        choice = input("User already DEACTIVATED. \nDo you want to DELETE IT?\n(y/n)")
        if choice == "y" or choice == "Y":
            deleteUser(id)
        else:
            main()

def getUser(login):
    r = requests.get(f'https://{tenant}.com/api/v1/users?filter=profile.login%20eq%20"{login}"', headers = headers)
    if r.status_code == requests.codes['ok'] or r.status_code == requests.codes['not_modified']:
        # print(r.__sizeof__())
        print("Response code is:\t\t\t {:>30}".format(r.status_code))
        req = json.loads(r.text)
        # req is a list here with 1 indice, the element being a dictionary of dictionaries

        # print(type(req)) - <class 'list'>
        # print(type(req[0])) - <class 'dict'>
        # print(type(req[0]["statusChanged"])) - <class 'str'>
        # print(type(r)) - <class 'requests.models.Response'>
        # print(type(r.headers)) - <class 'requests.structures.CaseInsensitiveDict'>
        # print(type(r.json())) - <class 'list'>

        return req[0]
    # elif ((r.status_code == requests.codes['ok'] or r.status_code == requests.codes['not_modified'])
    #     and r.__sizeof__() < 5):
    #     print("The login you entered is not to be found within the {}'s database".format(tenant))
    else:
        print("Error Occurred! Cannot read / find user.\nRESPONSE CODE IS: {}\nMake sure you have a valid API token used in the code, especially if the error response is 401".format(r.status_code))
        return


def deactivateUser(id):
    global first_name
    global last_name
    r = requests.post("https://{}.com/api/v1/users/{}/lifecycle/deactivate".format(tenant, id), headers=headers)
    if r.status_code == requests.codes['ok'] or
    r.status_code == requests.codes['not_modified'] or
    r.status_code == requests.codes['no_content']:
        print("""Response code is:\t\t\t {0:>30}\n User {2} {1} has just been DEACTIVATED""".format(r.status_code, last_name, first_name))
        if deactivate_flow == 1:
            main()
    else:
        print("Error occurred. Response code:\n {}".format(r.status_code))

def deleteUser(id):
    r = requests.delete("https://{}.com/api/v1/users/{}".format(tenant, id), headers=headers)
    if (r.status_code == requests.codes['ok'] or
        r.status_code == requests.codes['not_modified'] or
        r.status_code == requests.codes['no_content']):
    #if r.status_code == requests.codes['no_content']:
        print("Response code is:\t\t\t {:>30}\n User has just been DELETED".format(r.status_code))
        main()
    else:
        print("Error occurred. Response code:\n {}".format(r.status_code))
        main()
main()

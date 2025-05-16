print("hello")

def list_to_string(list):
    temp = ""
    for x in list:
        if x == "":
            x = " "
        temp = temp + x
    return temp

def string_to_list(string):
    temp = list(string)
    for x in range(len(temp)):
        if temp[x] == " ":
            temp[x] = ""
    return temp

templist = ['', '', 'O', 'O', '', 'O', '', 'O', '']
print(list_to_string(templist))
print(string_to_list(list_to_string(templist)))




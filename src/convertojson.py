import json
with open(r"C:\Users\Vennela\Downloads\project.txt",'r') as us:
    json_data=us.read()
us=json.loads(json_data)
with open('project.json','w') as we:
    json.dump(us,we,indent=4,sort_keys=False)



import requests

Base = "http://127.0.0.1:5000/"

data = [{"likes":100, "name":"prabha","views":100},
        {"likes":70, "name":"sudhakar","views":1000},
        {"likes":18, "name":"How to learn Rest api","views":8000},
        {"likes":10, "name":"Food festival","views":23000}]

# response = requests.get(Base+"helloworld/priya")
# response = requests.get(Base+"videos/youtube")

for i in range(len(data)):
    response = requests.put(Base+"videos/"+ str(i), data[i])
    print(response.json())


id = input("Enter id for deletion: ")
response = requests.delete(Base+"videos/"+id)
print(response)

id = input("Enter Id: ")
response = requests.get(Base+"videos/"+id)
print(response.json())

response = requests.get(Base+"/videos/getAll")
print(response.json())

response = requests.patch(Base+"videos/6",{"views":493})
print(response.json())
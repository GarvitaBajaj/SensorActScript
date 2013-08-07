import requests
import json

#The user enters the username and password
username=input("Enter username:")
password=input("Enter password:")

#JSON object to be sent in the http request for login
userlogin={"username":username,"password":password}

#Login url
userloginurl="http://sensoract.iiitd.edu.in:9001/user/login"

#Http Request for user login
loginrequest=requests.post(userloginurl,json.dumps(userlogin))

#converting the response to a JSON object
res=loginrequest.json()
print("the returned json object is \r\n",res,"\r\n")

#Extracting the owner/user key from the response object
message=res['message'].split(" ")
usertype=message[0]
userkey=message[1]

print("The user type is ",usertype," and his key is: ",userkey)

print("\r\n\r\n\r\n******* WELCOME ",usertype," *******\r\n\tThe list of vpds registered with your account are:")

#Http request for getting the list of registered vpds
getvpds=requests.post("http://sensoract.iiitd.edu.in:9001/vpds/list",json.dumps({"secretkey":userkey}))

#Converting the response of request to JSON object
getvpdslist=getvpds.json()
names,keys=[],[]

#Extracting the names and keys of all the vpds registered with the user
i=0
for vpds in getvpdslist['vpdslist']:
	i=i+1
	names.append(vpds['vpdsname'])
	keys.append(vpds['vpdsownerkey'])
	print(i,": ",vpds['vpdsname'])

#User selects a vpds from the list
vpdsindex=int(input("Enter the vpds number: "))

#Set the accesss key accordingly--for owner, it is the vpdsownerkey and for others it is the access key obtained by getaccesskey http request
if(usertype=="OWNER:"):
	accesskey=keys[vpdsindex-1]
	print(accesskey)
else:
	print("Access key is yet to be defined")
	secretkey=userkey
	vname=input("Enter the vpds name: ")
	data={"secretkey":secretkey,"vpdsname":vname}
	r=requests.post("http://sensoract.iiitd.edu.in:9001/accesskey/get",json.dumps(data))
	rs=r.json()
	accesskey=rs['accesskey']
	print("Access key is now defined",accesskey)

print("Please provide some more information to fetch data:\r\n")
devname=input("Device Name: ")
sensname=input("Sensor Name: ")
chname=input("Channel Name: ")
sensid=int(input("Sensor ID: "))
fromtime=int(input("From(in UNIX epochs): "))
to=int(input("Till(in UNIX epochs): "))

#Data to be sent in the dataquery request
info={
"secretkey":accesskey,
"username":username,
"devicename":devname,
"sensorname":sensname,
"sensorid":sensid,
"channelname":chname,
"conditions":
{
"fromtime":fromtime,
"totime":to
}
}

#Http request for querying the data from the broker using the access key
dataqueryurl="http://sensoract.iiitd.edu.in:9000/data/query"
dataqueryobj=json.dumps(info)
dataqueryrequest=requests.post(dataqueryurl,dataqueryobj)
print(dataqueryrequest.text)
wavesegarray=dataqueryrequest.json()

f=open('readings1.txt','w')
for element in wavesegarray['wavesegmentArray']:
	temp=str(element['data']['timestamp'])+":"+str(element['data']['channels'][0]['readings'])+"\n"
	f.write(temp)

f.close()
f=open("readings1.txt");
data=f.read();
f.close()
line = data.split("\n");
f=open("Readings.txt","w+");
for i in range(0,len(line)-1):
	temp=line[i];
	item = temp.split(":");
	timestamp_str = item[0];
	#print(timestamp_str);
	timestamp=int(timestamp_str);
	readings=item[1];
	readings=readings.strip("[");
	readings=readings.strip("]");
	newlist=readings.split(", ");
	for j in range(len(newlist)):
		f.write(str(timestamp));
		f.write("::");
		f.write(newlist[j]);
		f.write("\n")
		timestamp= timestamp+1;
	
f.close()
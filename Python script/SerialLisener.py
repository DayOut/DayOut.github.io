import time
import json
import sys
import serial # pip install serial
import requests # pip install requests

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
	
def showAllbgColors():
	print (bcolors.HEADER + "Warning: No active frommets remain. Continue?" + bcolors.ENDC)
	print (bcolors.OKBLUE + "Warning: No active frommets remain. Continue?" + bcolors.ENDC)
	print (bcolors.OKGREEN + "Warning: No active frommets remain. Continue?" + bcolors.ENDC)
	print (bcolors.WARNING + "Warning: No active frommets remain. Continue?" + bcolors.ENDC)
	print (bcolors.FAIL + "Warning: No active frommets remain. Continue?" + bcolors.ENDC)
	print (bcolors.ENDC + "Warning: No active frommets remain. Continue?" + bcolors.ENDC)
	print (bcolors.BOLD + "Warning: No active frommets remain. Continue?" + bcolors.ENDC)
	print (bcolors.UNDERLINE + "Warning: No active frommets remain. Continue?" + bcolors.ENDC)
	
def okGreenMess(text):
	return bcolors.OKGREEN + text + bcolors.ENDC
	
def okBlueMess(text):
	return bcolors.OKBLUE + text + bcolors.ENDC
	
def warningMess(text):
	return bcolors.WARNING + text + bcolors.ENDC

def failMess(text):
	return bcolors.FAIL + text + bcolors.ENDC
	
def debugAlert():
	mess = bcolors.WARNING + 'DEBUG data: ' + bcolors.ENDC
	return mess

def sendToThingsSpeak(humidity, temperature, ppm):
	url = 'https://api.thingspeak.com/update'
	payload = {'api_key':'WBN27S7HHZZ5SAGC','field1': humidity, 'field2':temperature, 'field3':ppm}
	# GET
	#r = requests.get(url)
	# GET with params in URL
	response = requests.get(url, params=payload)
	#print(response.content)
	#print('sended: ' + url + payload)
	#print('sended: ' + response.url)
	return response.content

DEBUG = True	
#DEBUG = False	
	
ser = serial.Serial(port='COM7',baudrate=9600,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS,timeout=0)

print(okGreenMess("Connected to: ") + ser.portstr)

tempForMin = 0.0 	#for collecting temp for 1 minute
humidForMin = 0.0	#for collecting humidity for 1 minute
ppmForMin = 0.0		# CO2
counter = 0			# 30 iterations ~1 minute

while True:
	try:
		arduinoMsg = ser.readline() #reading from arduino
		arduinoMsg = arduinoMsg.decode("utf-8") #make it string
		arduinoMsg = arduinoMsg[:-2] #removing /n/r
	except UnicodeDecodeError: # catch error and ignore it
		print(failMess('Error reading port...') + warningMess('\t Trying again...'))
	
	
	if arduinoMsg: #if response exists
		print('Collecting ' + str(counter) + ' of 30 packages of data   ', end='\r')
	
		# for debug, we receive it from arduino
		#print("origin string: \n" + str(count) + str(': ') + arduinoMsg)
		
		if arduinoMsg != "" and arduinoMsg[-1] == "}" and arduinoMsg[0] == "{": #if this response completed
			jsonMsg = json.loads(arduinoMsg) #create json
			humidForMin += float(jsonMsg['humidity']) # collecting data
			tempForMin += float(jsonMsg['temperature'])
			ppmForMin += float(jsonMsg['ppm'])
			
			if DEBUG: #debug show all data
				print(debugAlert() + okBlueMess('\tcounter: ') + str(counter) \
				+ okBlueMess('\thumidForMin:') 		+ str(round(humidForMin, 2)) \
				+ okBlueMess('\ttempForMin:') 		+ str(round(tempForMin, 2)) \
				+ okBlueMess(' \tcurrent humid:') 	+ jsonMsg['humidity'] \
				+ okBlueMess('\tcurrent temp:') 	+ jsonMsg['temperature'] \
				+ okBlueMess('\tcurrent ppm:') 		+ jsonMsg['ppm'])
			
			#print(json.dumps(jsonMsg, indent=4)) # json debug 
			if counter >= 30: # 30 iterations ~1 minute
				
				middleTemperature = tempForMin/counter #calculate mid value
				middleHumidity = humidForMin/counter #calculate mid value
				middlePpm = ppmForMin/counter
				
				if DEBUG:
					print(warningMess('Sending data to server...'))
					
				status = sendToThingsSpeak(middleHumidity, middleTemperature, middlePpm) # sending data to thingspeak
				status = status.decode('utf-8')
				
				if status != '0':
					print(okBlueMess(time.strftime("%H:%M:%S", time.localtime())) + '--Sending status: ' + okGreenMess('Success;    ') + okBlueMess('Sended data:\t') + arduinoMsg) # show what we have
					tempForMin = 0.0
					humidForMin = 0.0
					ppmForMin = 0.0
					counter = 0					
				else:
					print(okBlueMess(time.strftime("%H:%M:%S", time.localtime())) + '--Sending status: ' + failMess('Fail;       ') + okBlueMess('Sended data:\t') + arduinoMsg + warningMess('\t Trying again')) # show what we have	

			counter = counter +1
			
	time.sleep(2)

ser.close()
# Версия скрипта: 2020.01.21.0745
# Скрипт работает в паре с Электронным реестром микрокодов
#
# Поддерживается следующее оборудование:
# IMMv2 - доступ по SNMP
# XCC - доступ по SNMP
# Fibre Channel - доступ по SNMP
# IBM PDU - доступ по SNMP
# AMM - доступ по SNMP
# Storwize - доступ по SSH
# TS4300 Tape Library - доступ по SNMP
# APC PDU - доступ по SNMP
# ESXi - доступ по SNMP

from pysnmp.hlapi import *
import json
import requests
import base64
import paramiko
import time

# ГЛОБАЛЬНЫЕ ПЕРЕМЕННЫЕ:

# Необходимо выбрать филиал, с оборудованием которого скрипт будет работать.  
# Список поддерживаемых филиалов можно получить, используя ссылку:
# https://vs-assistant.oduvs.so/ords/firmwares/data/offices/
# По этой ссылке в формате JSON будет выведен массив филиалов в виде [{"id":1,"office_name":"..."}..]
# Необходимо правильно определить id своего филиала и указать его в переменной ниже:
office_id = 21

# Необходимо указать папку, в которой будут записываться логи
filepath = "C:\Scripts\logs"


# !!! В этих переменных править ничего не надо !!!
# Фиксируем время начала скрипта, это необходимо для файла логов
timestamp = time.strftime("%Y%m%d-%H%M%S") 
# URL для получения списка хостов филиала:
url_hosts = 'https://vs-assistant.oduvs.so/ords/firmwares/data/hosts/' + str(office_id)
# URL для отправки данных по IMMv2
url_imm2 = 'https://vs-assistant.oduvs.so/ords/firmwares/data/imm2/' 
# URL для отправки данных по FibreChannel
url_fc = 'https://vs-assistant.oduvs.so/ords/firmwares/data/fc/'  
# URL для отправки данных по PDU IBM
url_pdu = 'https://vs-assistant.oduvs.so/ords/firmwares/data/pdu/'  
# URL для отправки данных по XCC
url_xcc = 'https://vs-assistant.oduvs.so/ords/firmwares/data/xcc/'  
# URL для отправки данных по AMM
url_amm = 'https://vs-assistant.oduvs.so/ords/firmwares/data/amm/'  
# URL для отправки данных по Storwize
url_storwize = 'https://vs-assistant.oduvs.so/ords/firmwares/data/storwize/'  
# URL для отправки данных по TAPE
url_tape = 'https://vs-assistant.oduvs.so/ords/firmwares/data/tape/' 
# URL для отправки данных по PDU APC
url_pdu_apc = 'https://vs-assistant.oduvs.so/ords/firmwares/data/pdu_apc/'
# URL для отправки данных по ESXi
url_esxi = 'https://vs-assistant.oduvs.so/ords/firmwares/data/esxi/'
# URL для отправки данных по vCenter
url_vCenter = 'https://vs-assistant.oduvs.so/ords/firmwares/data/vcenter/'


# Скрипт активно использует библиотеку http://snmplabs.com/pysnmp для доступа по SNMP. 
# на сайте есть большое количество примеров, по ним при необходимости можно разобраться как тут все работает 

def fn_immv1(ip, community):
#----------------- IMMv1 - wellknown OIDs -----------------------
	oid_immv1_model = ".1.3.6.1.4.1.2.3.51.3.1.5.2.1.5.0"
	oid_immv1_imm = ".1.3.6.1.4.1.2.3.51.3.1.5.1.1.3.1" 
	oid_immv1_uefi = ".1.3.6.1.4.1.2.3.51.3.1.5.1.1.3.2"
	oid_immv1_dsa = ".1.3.6.1.4.1.2.3.51.3.1.5.1.1.3.3"
#----------------------------------------------------------------
	error = ''
	imm = ''
	uefi = ''
	dsa = '' 
	errorIndication, errorStatus, errorIndex, varBinds = next(
		getCmd(SnmpEngine(),
			   CommunityData(community),
			   UdpTransportTarget((ip, 161)),
			   ContextData(),
			   ObjectType(ObjectIdentity(oid_immv1_imm)),
			   ObjectType(ObjectIdentity(oid_immv1_uefi)),
			   ObjectType(ObjectIdentity(oid_immv1_dsa))
			   ) 
	)
	if errorIndication:
		error = errorIndication
	else:
		name, imm =  varBinds[0]
		name, uefi =  varBinds[0]
		name, dsa =  varBinds[0]
	
	# Last function string:
	return str(error), imm, uefi, dsa

def fn_immv2(ip, community):
#----------------- IMMv2 - wellknown OIDs -----------------------
	oid_immv2_model = ".1.3.6.1.4.1.2.3.51.3.1.5.2.1.5.0"
	oid_immv2_immactive = ".1.3.6.1.4.1.2.3.51.3.1.5.1.1.3.1"
	oid_immv2_uefiactive = ".1.3.6.1.4.1.2.3.51.3.1.5.1.1.3.4" 
	oid_immv2_dsa = ".1.3.6.1.4.1.2.3.51.3.1.5.1.1.3.7"
	oid_immv2_immprimary = ".1.3.6.1.4.1.2.3.51.3.1.5.1.1.3.2"
	oid_immv2_immbackup = ".1.3.6.1.4.1.2.3.51.3.1.5.1.1.3.3" 
	oid_immv2_uefiprimary = "1.3.6.1.4.1.2.3.51.3.1.5.1.1.3.5" 
	oid_immv2_uefibackup = ".1.3.6.1.4.1.2.3.51.3.1.5.1.1.3.4"
#----------------------------------------------------------------

	error = ''
	immprimary = ''
	immbackup = ''
	immactive = ''
	uefiprimary = ''
	uefibackup = ''
	uefiactive = ''
	dsa = ''
	model = ''
	errorIndication, errorStatus, errorIndex, varBinds = next(
		getCmd(SnmpEngine(),
			   CommunityData(community),
			   UdpTransportTarget((ip, 161)),
			   ContextData(),
			   ObjectType(ObjectIdentity(oid_immv2_immprimary)),
			   ObjectType(ObjectIdentity(oid_immv2_immbackup)),
			   ObjectType(ObjectIdentity(oid_immv2_immactive)),
			   ObjectType(ObjectIdentity(oid_immv2_uefiprimary)),
			   ObjectType(ObjectIdentity(oid_immv2_uefibackup)),
			   ObjectType(ObjectIdentity(oid_immv2_uefiactive)),
			   ObjectType(ObjectIdentity(oid_immv2_dsa)),
				ObjectType(ObjectIdentity(oid_immv2_model))
			   ) 
	)
	if errorIndication:
		error = errorIndication
	elif errorStatus:
		print('%s at %s' % (errorStatus.prettyPrint(),
							errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
	else:
		name, immprimary =  varBinds[0]
		name, immbackup =  varBinds[1]
		name, immactive =  varBinds[2]
		name, uefiprimary =  varBinds[3]
		name, uefibackup =  varBinds[4]
		name, uefiactive =  varBinds[5]
		name, dsa =  varBinds[6]
		name, model = varBinds[7]

	# Last function string:
	return error, immprimary, immbackup, immactive, uefiprimary, uefibackup, uefiactive, dsa, model
	
def fn_xcc(ip, user):
#----------------- XCC - wellknown OIDs -----------------------
	oid_xcc_bmcactive = "1.3.6.1.4.1.19046.11.1.1.5.1.1.3.1"
	oid_xcc_uefi = "1.3.6.1.4.1.19046.11.1.1.5.1.1.3.4" 
	oid_xcc_lxpm = "1.3.6.1.4.1.19046.11.1.1.5.1.1.3.5"
	oid_xcc_bmcprimary = "1.3.6.1.4.1.19046.11.1.1.5.1.1.3.2"
	oid_xcc_bmcbackup = "1.3.6.1.4.1.19046.11.1.1.5.1.1.3.3" 
	oid_xcc_lxpmwindows = "1.3.6.1.4.1.19046.11.1.1.5.1.1.3.6" 
	oid_xcc_lxpmlinux = "1.3.6.1.4.1.19046.11.1.1.5.1.1.3.7"
	oid_xcc_model = ".1.3.6.1.4.1.19046.11.1.1.5.2.1.5.0"
#----------------------------------------------------------------
	error = ''							# Обнуляем рабочие переменные
	bmcactive = ''						# Обнуляем рабочие переменные
	uefi = ''							# Обнуляем рабочие переменные
	lxpm = ''							# Обнуляем рабочие переменные
	bmcprimary = ''						# Обнуляем рабочие переменные
	bmcbackup = ''						# Обнуляем рабочие переменные
	lxpmwindows = ''					# Обнуляем рабочие переменные
	lxpmlinux = ''						# Обнуляем рабочие переменные
	model = ''							# Обнуляем рабочие переменные
	errorIndication, errorStatus, errorIndex, varBinds = next(
		getCmd(SnmpEngine(),
			   UsmUserData(user),       # Скрипт написан так, что поддерживает в настоящий момент вариант noAuth, noPriv. Необходимо только имя пользователя
			   UdpTransportTarget((ip, 161)),
			   ContextData(),
			   ObjectType(ObjectIdentity(oid_xcc_bmcactive)),
			   ObjectType(ObjectIdentity(oid_xcc_uefi)),
			   ObjectType(ObjectIdentity(oid_xcc_lxpm)),
			   ObjectType(ObjectIdentity(oid_xcc_bmcprimary)),
			   ObjectType(ObjectIdentity(oid_xcc_bmcbackup)),
			   ObjectType(ObjectIdentity(oid_xcc_lxpmwindows)),
			   ObjectType(ObjectIdentity(oid_xcc_lxpmlinux)),
				ObjectType(ObjectIdentity(oid_xcc_model))
			   ) 
	)
	if errorIndication:
		error = errorIndication
	else:
		name, bmcactive =  varBinds[0]
		name, uefi =  varBinds[1]
		name, lxpm =  varBinds[2]
		name, bmcprimary =  varBinds[3]
		name, bmcbackup =  varBinds[4]
		name, lxpmwindows =  varBinds[5]
		name, lxpmlinux =  varBinds[6]
		name, model = varBinds[7]

	# Last function string:
	return error, bmcactive, bmcprimary, bmcbackup, uefi, lxpm, lxpmwindows, lxpmlinux, model			# Возвращаем данные из функции

def fn_fc(ip, community):
#----------------- Fibre Channel - wellknown OIDs ---------------
	oid_fc = ".1.3.6.1.4.1.1588.2.1.1.1.1.6.0"
#----------------------------------------------------------------
	error = ''
	firmware = ''
	errorIndication, errorStatus, errorIndex, varBinds = next(
		getCmd(SnmpEngine(),
			   CommunityData(community),
			   UdpTransportTarget((ip, 161)),
			   ContextData(),
			   ObjectType(ObjectIdentity(oid_fc))) 
	)
	if errorIndication:
		error = errorIndication
	else:
		name, firmware =  varBinds[0]
			
	# Last function string:
	return str(error), firmware

def fn_pdu(ip, community):
#-------- Power Distributed Unit - wellknown OIDs ---------------
	oid_pdu = ".1.3.6.1.4.1.2.6.223.7.3.0"
#----------------------------------------------------------------
	error = ''
	firmware = ''
	errorIndication, errorStatus, errorIndex, varBinds = next(
		getCmd(SnmpEngine(),
			   CommunityData(community),
			   UdpTransportTarget((ip, 161)),
			   ContextData(),
			   ObjectType(ObjectIdentity(oid_pdu))) 
	)
	if errorIndication:
		error = errorIndication
	else:
		name, firmware =  varBinds[0]
			
	# Last function string:
	return str(error), firmware
	
def fn_pdu_apc(ip, community):
#-------- APC Power Distributed Unit - wellknown OIDs ---------------
	oid_rackpdu = ".1.3.6.1.4.1.318.1.4.2.4.1.4.1"
	oid_apcos = ".1.3.6.1.4.1.318.1.4.2.4.1.4.2"
	oid_bootmonitor = ".1.3.6.1.4.1.318.1.4.2.4.1.4.3"
#----------------------------------------------------------------
	error = ''
	rackpdu = ''
	apcos = ''
	bootmonitor = ''
	errorIndication, errorStatus, errorIndex, varBinds = next(
		getCmd(SnmpEngine(),
			   CommunityData(community),
			   UdpTransportTarget((ip, 161)),
			   ContextData(),
			   ObjectType(ObjectIdentity(oid_rackpdu)),
			   ObjectType(ObjectIdentity(oid_apcos)),
			   ObjectType(ObjectIdentity(oid_bootmonitor)),
			   ) 
	)
	if errorIndication:
		error = errorIndication
	else:
		name, rackpdu =  varBinds[0]
		name, apcos =  varBinds[1]
		name, bootmonitor =  varBinds[2]
			
	# Last function string:
	return str(error), rackpdu, apcos, bootmonitor

def fn_tape(ip, community):
#-------- IBM Tape Library - wellknown OIDs ---------------
	oid_tape = ".1.3.6.1.4.1.14851.3.1.3.4.0"
	oid_model = ".1.3.6.1.4.1.2.6.211.1.1.0"
#----------------------------------------------------------------
	error = ''
	firmware = ''
	model = ''
	errorIndication, errorStatus, errorIndex, varBinds = next(
		getCmd(SnmpEngine(),
			   CommunityData(community),
			   UdpTransportTarget((ip, 161)),
			   ContextData(),
			   ObjectType(ObjectIdentity(oid_tape))
			   )
	)
	if errorIndication:
		error = errorIndication
	else:
		name, firmware =  varBinds[0]
			
	# Last function string:
	return str(error), firmware

def fn_amm(ip, community):
#----------------- AMM - wellknown OIDs -----------------------
	oid_amm1_build = ".1.3.6.1.4.1.2.3.51.2.2.21.3.1.1.3.1"
	oid_amm1_rev = ".1.3.6.1.4.1.2.3.51.2.2.21.3.1.1.4.1"
	oid_amm2_build = ".1.3.6.1.4.1.2.3.51.2.2.21.3.1.1.3.2"
	oid_amm2_rev = ".1.3.6.1.4.1.2.3.51.2.2.21.3.1.1.4.2"
#----------------------------------------------------------------
	error = ''					# Обнуляем рабочие переменные
	build1 = ''					
	build2 = ''					
	rev1 = ''
	rev2 = ''
	errorIndication, errorStatus, errorIndex, varBinds = next(
		getCmd(SnmpEngine(),
			   CommunityData(community, mpModel=0),
			   UdpTransportTarget((ip, 161)),
			   ContextData(),
			   ObjectType(ObjectIdentity(oid_amm1_build)),
			   ObjectType(ObjectIdentity(oid_amm1_rev)),
			   ObjectType(ObjectIdentity(oid_amm2_build)),
			   ObjectType(ObjectIdentity(oid_amm2_rev))
			   ) 
	)
	if errorIndication:
		error = errorIndication
	else:
		name, build1 =  varBinds[0]
		name, rev1 =  varBinds[1]
		name, build2 =  varBinds[2]
		name, rev2 =  varBinds[3]

	# Last function string:
	return str(error), build1, rev1, build2, rev2

def fn_storwize(ip, user, password):    # Функция для сбора данных со сторвайзов
	stdin = ''             # Обнуляем рабочие переменные
	stdout = ''             # Обнуляем рабочие переменные
	stderr = ''             # Обнуляем рабочие переменные
	firmware = ''           # Обнуляем рабочие переменные
	client = paramiko.SSHClient()           # Используем библиотеку paramiko для сбора данных по SSH
	client.set_missing_host_key_policy(paramiko.AutoAddPolicy())            # Необходимо для автоматического импорта ключей новых хостов. Без этого не работает
	try:            # Используем это для обработки исключений при неудачном подключении к хосту
		client.connect(ip, username=user, password=password)
		stdin, stdout, stderr = client.exec_command('lssystem')         # Выполняем на сторвайзе одну команду
		if stdout:
			for line in stdout:                     #  Построчно парсим данные со сторвайза, если они были получены
				if "code_level" in line:        #  Находим нужную строчку, делим ее символу пробела на три части и берем вторую часть
					firmware = line.split()[1]
		client.close()
		return firmware                 # В случае успеха возвращаем полученные данные
	except Exception:           # Если было исключение при подключении к сторвайзу, то возвращаем пустую строку
		return ''

def fn_esxi(ip, community):
#----------------- ESXi - wellknown OIDs ---------------
	oid_version = ".1.3.6.1.4.1.6876.1.2.0"
	oid_build = ".1.3.6.1.4.1.6876.1.4.0"
#----------------------------------------------------------------
	error = ''
	version = ''
	build = ''
	errorIndication, errorStatus, errorIndex, varBinds = next(
		getCmd(SnmpEngine(),
			   CommunityData(community),
			   UdpTransportTarget((ip, 161)),
			   ContextData(),
			   ObjectType(ObjectIdentity(oid_version)),
			   ObjectType(ObjectIdentity(oid_build))
			)
	)
	if errorIndication:
		error = errorIndication
	else:
		name, version =  varBinds[0]
		name, build =  varBinds[1]
			
	# Last function string:
	return str(error), version, build


def fn_vCenter(ip, community):
	# ----------------- ESXi - wellknown OIDs ---------------
	oid_version = ".1.3.6.1.4.1.6876.1.2.0"
	# ----------------------------------------------------------------
	error = ''
	version = ''
	errorIndication, errorStatus, errorIndex, varBinds = next(
		getCmd(SnmpEngine(),
			   CommunityData(community),
			   UdpTransportTarget((ip, 161)),
			   ContextData(),
			   ObjectType(ObjectIdentity(oid_version))
			   )
	)
	if errorIndication:
		error = errorIndication
	else:
		name, version = varBinds[0]

	# Last function string:
	return str(error), version

def logger(message):    # Функция для логирования событий
	payload = ''     # Обнуляем рабочие переменные
	url_log = 'http://sv-applications/apex/firmwares/data/log/' # URL для отправки логов на сервер
	filename = filepath + "\log-" + timestamp + ".txt"
	
	payload = {"message": message}		# Формируем данные, которые отправим по POST запросу в БД в формате JSON
        # Для логирования надо раскоментировать строчку ниже
	#result = requests.post(url_log, json=payload) # Отправляем данные
        
	print(message)
	with open(filename, "a") as f:
		f.write(message + "\n")
		f.close()
		
	return

#------ MAIN PROGRAM ---------------------------------------------

logger('Script started')										# Логируем действия

response = requests.get(url_hosts, verify=False) # Берем список всех хостов из БД
hosts = response.json() # Возвращает значение типа dict
for host in hosts.get('items'): # Для каждого хоста собираем данные
	logger("--------------------------------------------------")
	logger("Processing host: " + str(host.get('hostname')));
	
	error = '' 					# Обнуляем рабочие переменные
	imm1 = '' 					# Обнуляем рабочие переменные
	imm2 = '' 					# Обнуляем рабочие переменные
	immactive = '' 					# Обнуляем рабочие переменные
	uefi1 = '' 					# Обнуляем рабочие переменные
	uefi2 = '' 					# Обнуляем рабочие переменные
	uefiactive = '' 				# Обнуляем рабочие переменные
	dsa = '' 					# Обнуляем рабочие переменные
	url = ''					# Обнуляем рабочие переменные 
	payload = ''				        # Обнуляем рабочие переменные
	bmcactive = ''                                  # Обнуляем рабочие переменные
	bmcprimary = ''                                 # Обнуляем рабочие переменные
	bmcbackup = ''                                  # Обнуляем рабочие переменные
	uefi = ''                                       # Обнуляем рабочие переменные
	lxpm = ''                                       # Обнуляем рабочие переменные
	lxpmwindows = ''                                # Обнуляем рабочие переменные
	lxpmlinux = ''                                  # Обнуляем рабочие переменные
	firmware = ''                                   # Обнуляем рабочие переменные
	rackpdu = ''                                    # Обнуляем рабочие переменные
	apcos = ''                                      # Обнуляем рабочие переменные
	bootmonitor = ''                                # Обнуляем рабочие переменные
	build1 = ''                                     # Обнуляем рабочие переменные
	rev1 = ''                                       # Обнуляем рабочие переменные
	build2 = ''                                     # Обнуляем рабочие переменные
	rev2 = ''                                       # Обнуляем рабочие переменные
	model = ''  									# Обнуляем рабочие переменные
	
	if host.get('host_type') == 'IMMv2':       # Если тип хоста IMMv2 тогда выполняем этот код
		logger('Host type is IMMv2')
		try:
			error, imm1, imm2, immactive, uefi1, uefi2, uefiactive, dsa, model = fn_immv2(host.get('ipaddress'),host.get('snmp_access_string')) # Сохраняем в переменные полученные по SNMP значения
		except:
			error = '!!! Exception !!!'
		if error: # Если есть ошибки выполняем этот код
			logger('Data received with errors: ' + str(error))
		else: # Если данные по SNMP получены без ошибок выполняем этот код
			logger('Data received successfully')
			url = url_imm2							 # сохраняем ссылку, на которую отправим данные
			payload = { "host_id" : host.get('id'),  # Формируем данные, которые отправим по POST запросу в БД
						 "imm_primary" : str(imm1),  # str - перевод к типу данных String
						 "imm_backup" : str(imm2),
						 "imm_active" : str(immactive),
						 "uefi_primary" : str(uefi1),
						 "uefi_backup" : str(uefi2),
						 "uefi_active" : str(uefiactive),
						 "dsa" : str(dsa),
						"model": str(model)
					   }
	
	if host.get('host_type') == 'XCC':       # Если тип хоста XCC тогда выполняем этот код
		logger('Host type is XCC')
		try:
			error, bmcactive, bmcprimary, bmcbackup, uefi, lxpm, lxpmwindows, lxpmlinux, model = fn_xcc(host.get('ipaddress'),host.get('snmp_access_string')) # Сохраняем в переменные полученные по SNMP значения
		except:
			error = '!!! Exception !!!'
		if error: # Если есть ошибки выполняем этот код
			logger('Data received with errors: ' + str(error))
		else: # Если данные по SNMP получены без ошибок выполняем этот код
			logger('Data received successfully')
			url = url_xcc							 # сохраняем ссылку, на которую отправим данные
			payload = { "host_id" : host.get('id'),  # Формируем данные, которые отправим по POST запросу в БД
						 "bmcactive" : str(bmcactive),  # str - перевод к типу данных String
						 "bmcprimary" : str(bmcprimary),
						 "bmcbackup" : str(bmcbackup),
						 "uefi" : str(uefi),
						 "lxpm" : str(lxpm),
						 "lxpmwindows" : str(lxpmwindows),
						 "lxpmlinux" : str(lxpmlinux),
						"model": str(model)
						}
					   
	if host.get('host_type') == 'FC':       # Если тип хоста FibreChannel тогда выполняем этот код
		logger('Host type is FC')
		try:
			error, firmware = fn_fc(host.get('ipaddress'),host.get('snmp_access_string')) # Сохраняем в переменные полученные по SNMP значения
		except:
			error = '!!! Exception !!!'
		if error: # Если есть ошибки выполняем этот код
			logger('Data received with errors: ' + str(error))
		else: # Если данные по SNMP получены без ошибок выполняем этот код
			logger('Data received successfully')
			url = url_fc							 # сохраняем ссылку, на которую отправим данные
			payload = { "host_id" : host.get('id'),  # Формируем данные, которые отправим по POST запросу в БД
						 "firmware" : str(firmware)  # str - перевод к типу данных String 
					   }
	
	if host.get('host_type') == 'PDU':       # Если тип хоста PDU тогда выполняем этот код
		logger('Host type is PDU')
		try:
			error, firmware = fn_pdu(host.get('ipaddress'),host.get('snmp_access_string')) # Сохраняем в переменные полученные по SNMP значения
		except:
			error = '!!! Exception !!!'
		if error: # Если есть ошибки выполняем этот код
			logger('Data received with errors: ' + str(error))
		else: # Если данные по SNMP получены без ошибок выполняем этот код
			logger('Data received successfully')
			url = url_pdu							 # сохраняем ссылку, на которую отправим данные
			payload = { "host_id" : host.get('id'),  # Формируем данные, которые отправим по POST запросу в БД
						 "firmware" : str(firmware)  # str - перевод к типу данных String 
					   }
	
	if host.get('host_type') == 'PDU_APC':       # Если тип хоста PDU_APC тогда выполняем этот код
		logger('Host type is PDU_APC')
		try:
			error, rackpdu, apcos, bootmonitor = fn_pdu_apc(host.get('ipaddress'),host.get('snmp_access_string')) # Сохраняем в переменные полученные по SNMP значения
		except:
			error = '!!! Exception !!!'
		if error: # Если есть ошибки выполняем этот код
			logger('Data received with errors: ' + str(error))
		else: # Если данные по SNMP получены без ошибок выполняем этот код
			logger('Data received successfully')
			url = url_pdu_apc						 # сохраняем ссылку, на которую отправим данные
			payload = { "host_id" : host.get('id'),  # Формируем данные, которые отправим по POST запросу в БД
						 "rackpdu": str(rackpdu),	 # str - перевод к типу данных String 
						 "apcos": str(apcos),
						 "bootmonitor": str(bootmonitor)
					   }
	
	if host.get('host_type') == 'TAPE':       # Если тип хоста TAPE тогда выполняем этот код
		logger('Host type is TAPE')
		try:
			error, firmware = fn_tape(host.get('ipaddress'),host.get('snmp_access_string')) # Сохраняем в переменные полученные по SNMP значения
		except:
			error = '!!! Exception !!!'
		if error: # Если есть ошибки выполняем этот код
			logger('Data received with errors: ' + str(error))
		else: # Если данные по SNMP получены без ошибок выполняем этот код
			logger('Data received successfully')
			url = url_tape							 # сохраняем ссылку, на которую отправим данные
			payload = { "host_id" : host.get('id'),  # Формируем данные, которые отправим по POST запросу в БД
						 "firmware" : str(firmware)  # str - перевод к типу данных String
					   }
        
					   
	if host.get('host_type') == 'AMM':       # Если тип хоста AMM тогда выполняем этот код
		logger('Host type is AMM')
		try:
			error, build1, rev1, build2, rev2 = fn_amm(host.get('ipaddress'),host.get('snmp_access_string')) # Сохраняем в переменные полученные по SNMP значения
		except:
			error = '!!! Exception !!!'
		if error: # Если есть ошибки выполняем этот код
			logger('Data received with errors: ' + str(error))
		else: # Если данные по SNMP получены без ошибок выполняем этот код
			logger('Data received successfully')
			url = url_amm							 # сохраняем ссылку, на которую отправим данные
			payload = { "host_id" : host.get('id'),  # Формируем данные, которые отправим по POST запросу в БД
						 "build1": str(build1),	     # str - перевод к типу данных String 
						 "build2": str(build2),
						 "revision1": str(rev1),
						 "revision2": str(rev2)
					   }

	if host.get('host_type') == 'Storwize':         
		logger("Host type is Storwize")
		try:
			firmware = fn_storwize(host.get('ipaddress'),host.get('ssh_user'),host.get('ssh_pass'))
		except:
			error = '!!! Exception !!!'
		if firmware:
			logger('Data received')
			url = url_storwize                       # сохраняем ссылку, на которую отправим данные
			payload = { "host_id" : host.get('id'),  # Формируем данные, которые отправим по POST запросу в БД
						 "firmware" : str(firmware)  # str - перевод к типу данных String 
					   }

	if host.get('host_type') == 'ESXi':         # Если тип хоста ESXi тогда выполняем этот код
		logger("Host type is ESXi")
		try:
			error, version, build = fn_esxi(host.get('ipaddress'),host.get('snmp_access_string'))
		except:
			error = '!!! Exception !!!'
		if error:  # Если есть ошибки выполняем этот код
			logger('Data received with errors: ' + str(error))
		else:  # Если данные по SNMP получены без ошибок выполняем этот код
			logger('Data received successfully')
			url = url_esxi  # сохраняем ссылку, на которую отправим данные
			payload = {"host_id": host.get('id'),  # Формируем данные, которые отправим по POST запросу в БД
					   "version": str(version),  # str - перевод к типу данных String
					   "build": str(build)
					   }

	if host.get('host_type') == 'vCenter':         # Если тип хоста vCenter тогда выполняем этот код
		logger("Host type is vCenter")
		try:
			error, version = fn_vCenter(host.get('ipaddress'),host.get('snmp_access_string'))
		except:
			error = '!!! Exception !!!'
		if error:  # Если есть ошибки выполняем этот код
			logger('Data received with errors: ' + str(error))
		else:  # Если данные по SNMP получены без ошибок выполняем этот код
			logger('Data received successfully')
			url = url_vCenter  # сохраняем ссылку, на которую отправим данные
			payload = {"host_id": host.get('id'),  # Формируем данные, которые отправим по POST запросу в БД
					   "version": str(version)  # str - перевод к типу данных String)
					   }
					   
	if payload and url:
		logger('Payload: ' + str(payload))
		logger('URL: ' + url)
		result = requests.post(url, json=payload, verify=False) # Отправляем данные
		logger('HTTP response code: ' + str(result.status_code)) 	# код ответа при отправке данных в БД

logger('----------------------------------------------')
logger('Script stopped')

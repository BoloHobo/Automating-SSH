#!/bin/python3

import pexpect
PROMPT = [">>> ","# ","> ","\$ "]


#escales to su with default kali password
def escalate(child,user,password):
	child.sendline("sudo su")
	ret = child.expect([pexpect.TIMEOUT, "[P|p]assword for " + user])
	if ret == 0:
		print("[-] An error has occurred")
		return False
	if ret == 1:
		child.sendline(input("Admin password: "))
		ret = child.expect(["Sorry, try again", "root@kali"])
		if ret == 0:
			return False
		if ret == 1:
			return True
		
	return False

#sends the command in CLI 
def send_command(child, cmd):
	#print(cmd)
	
	print(child.before)
	print("\n")
	child.sendline(cmd)
	
	child.expect(PROMPT)
	print(child.before)
	#print("\n")
	#print(child.after)
	

#attempts to make the connection and return the child variable used to make the command
def connect(user,host,password):
	ssh_newkey = "Are you sure you want to continue connecting"
	conStr = "ssh "  + user + "@" + host
	child = pexpect.spawn(conStr)
	ret = child.expect([pexpect.TIMEOUT, ssh_newkey, "[P|p]assword: "])
	if ret == 0:
		print("[-] Error connecting")
		return
	if ret == 1:
		child.sendline("yes")
		ret = child.expect([pexpect.TIMEOUT,"[P|p]assword: "])
		if ret == 0:
			print("[-] Error connecting")
			return
	child.sendline(password)
	child.expect(PROMPT)
	return child


#initializes the variables and executes the functions
def main():
	host = input("IP Address: ")
	user = input("Username: ")
	password = input("Password: ")
	child = connect(user,host,password)
	#child.sendline("sudo su")
	#child.sendline(input("Admin Password: "))
	#if escalate(child,user,password):
	#	print("[+] Escalation to root successful")
	#else:
	#	print("[-] Unable to escalate to root")
	send_command(child, "cat /etc/shadow | grep root")
	
	
	
	
if __name__ == "__main__":
	main()


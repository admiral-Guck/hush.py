#!/usr/bin/python
#
# Hush lots of stuff on ze interwebs: install Dan Pollock's hosts file and update if necessary
# gucky 2015
#

import subprocess, arrow, re, os, shutil, sys



local_hosts = '/etc/hosts'
local_pollock_hosts = '/etc/hosts.pol'
user_hosts = '/etc/hosts.user'
tmp_hosts = '/tmp/hosts'


def extract_date(file):
	"""Extract the last update from Pollock's hosts file and return its timestamp."""
	with open(file, 'r') as f:
		txt = f.read()
		data = re.search("# Last updated: (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) (\d{1,2})[a-z]*, (\d{4}) at (\d{2}:\d{2})", txt)
		month = data.group(1)
		day = data.group(2)
		year = data.group(3)
		time = data.group(4)
		# Add a leading 0 to single-digit days
		if len(day) == 1:
			day = '0' + day
		# print(file + ': ' + month, day, year, time)
		return arrow.get(month + day + year + time, 'MMMDDYYYYHH:mm').timestamp

def download_pollock():
	"""Download Pollock's hosts file and store it in /tmp/hosts"""
	with open(tmp_hosts, 'w') as tmp_file:
		print("Downloading Pollock's hosts file...")
		try:
			subprocess.call(['curl', '-s', 'http://someonewhocares.org/hosts/hosts'], stdout=tmp_file)
		except:
			print("!! Download failed")
			exit()

if __name__ == '__main__':
	# Create empty [1] so that 'if or' works
	if len(sys.argv) == 1:
		sys.argv.append('')
# ;drop table users;
	if os.path.isfile(local_hosts) and os.path.isfile(local_pollock_hosts):
		local_pollock_date = extract_date(local_hosts)
		download_pollock()
		remote_pollock_date = extract_date(tmp_hosts)
		if remote_pollock_date > local_pollock_date or sys.argv[1] == '-f':
			print("Local file is outdated, updating...")
			# Backup
			print("Backing up " + local_hosts + " to " + local_pollock_hosts)
			subprocess.call(["/usr/bin/sudo", "/bin/cp", local_hosts, local_pollock_hosts])
			# Patch with user mods
			print("Applying " + user_hosts)
			# Write new hosts
			print("Writing " + local_hosts)
			subprocess.call(["/usr/bin/sudo", "/bin/cp", tmp_hosts, local_hosts])
		else:
			print("Local hosts file is up-to-date.")
	else:
		print("!! Either /etc/hosts or /etc/hosts.pol is missing.\n   This is either because the files are missing\n   or because you just ran this for the first time.")
		download_pollock()
		print("Writing " + local_hosts)
		subprocess.call(["/usr/bin/sudo", "/bin/cp", tmp_hosts, local_hosts])
		print("Writing " + local_pollock_hosts)
		subprocess.call(["/usr/bin/sudo", "/bin/cp", tmp_hosts, local_pollock_hosts])

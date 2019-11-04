import subprocess
import os

print("Please input user-domain file:")
rawdata=input()
print("Please input record type eg A, NS, MX")
record_type=input()
f=open(rawdata,"r")
user_domain=f.read().splitlines()

uniq_user=subprocess.check_output("cat "+rawdata+"| awk -F' ' '{print $1}' | sort | uniq", shell=True).decode("utf-8")
uniq_user=str(uniq_user).splitlines()

#to make user=>domain dictionary
mydict={}
for i in uniq_user:
    for y in user_domain:
      y=y.strip()
      user=y.split()[0]
      domain=y.split()[1]
      
      if i==user:
          if i in mydict:
              mydict[i].append(domain)
          else:
              mydict[i]=[domain]

'''
check ns used
gather all user that has domain pointing to specified ns
'''

for i in mydict:
    for domain in mydict[i]:
        dig_domain=subprocess.check_output("dig "+domain+" "+record_type+" >>temp", shell=True).decode("utf-8")


niaga_user=set()
check=subprocess.check_output("cat temp | grep -w NS | grep 'niagahoster.com' |awk '{print $1}'| sort | uniq | sed s'/.$//'", shell=True).decode("utf-8").splitlines()
for i in check:
    user=subprocess.check_output("grep -w "+i+" user-domain1 | awk '{print $1}' | sort | uniq", shell=True).decode("utf-8")
    niaga_user.add(user.strip())
niaga_user.remove("")

for i in niaga_user:
    subprocess.check_call("/usr/local/cpanel/bin/set_zone_ttl --user $user --newttl 600 --force", shell=True)

#get ip
#grep -w IP /var/cpanel/users/* | awk -F: '{print $2}' | cut -d= -f2 | sort -n -t'.' -k4 |uniq


ip_list=['127.0.0.1', '153.92.11.2', '153.92.11.5', '153.92.11.6', '153.92.11.7', 
    '153.92.11.8', '153.92.11.10', '153.92.11.11', '153.92.11.12', '153.92.11.13', 
    '153.92.11.14', '153.92.11.15', '153.92.11.16', '153.92.11.17', '153.92.11.18', 
    '153.92.11.19', '153.92.11.20', '153.92.11.21', '153.92.11.22', '153.92.11.23', 
    '153.92.11.24', '153.92.11.25', '153.92.11.26', '153.92.11.27', '153.92.11.28', 
    '153.92.11.29', '153.92.11.30', '153.92.11.31', '153.92.11.32', '153.92.11.33', 
    '153.92.11.34', '153.92.11.35', '153.92.11.36', '153.92.11.37', '153.92.11.38', 
    '153.92.11.39', '153.92.11.40', '153.92.11.41', '153.92.11.42', '153.92.11.43', 
    '153.92.11.44', '153.92.11.45', '153.92.11.46', '153.92.11.47', '153.92.11.48', 
    '153.92.11.49', '153.92.11.50']
'''
ip_list=['127.0.0.1', '153.92.11.2', '153.92.11.5', '153.92.11.6', '153.92.11.7', 
    '153.92.11.8', '153.92.11.10', '153.92.11.11', '153.92.11.12', '153.92.11.13', 
    '153.92.11.14', '153.92.11.15', '153.92.11.16', '153.92.11.17', '153.92.11.18', 
    '153.92.11.19', '153.92.11.20', '153.92.11.21', '153.92.11.22', '153.92.11.23', 
    '153.92.11.24', '153.92.11.25']
'''

user_ip={}
y=0

for i in niaga_user:
    
    if y>=len(ip_list)-1:
        y=0
    else:
        y+=1

    #user_ip[i]=ip_list[y]
    change_ip=user=subprocess.check_call("usr/local/cpanel/bin/setsiteip -u "+i+" "+y+"", shell=True)
    

#print(niaga_user)
#print(user_ip)
#print("jumlah user: "+str(len(niaga_user)))
#print("jumlah ip: "+str(len(ip_list)))

    

#akhirnya file user-domain dan dns-record disimpan dalam 1 archive file dengan penamaan IP_ALAMATIP_TANGGAL




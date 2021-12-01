import os
import subprocess

os.system('cat /dev/null > /tmp/poolist.txt')
Server_list = ['server_name']
pool_list = []
for i in Server_list:
    os.system('zpool list | grep -i %s'%(i) + ' | awk "{print \$1}" >> /tmp/poolist.txt')

def create_dir_in_DRNAS(Server_list):
    for i in Server_list:
            os.system('mkdir -p /DR_NAS/Solaris/Snapshots/%s'%(i))

def copy_snapshot(pool):
    size = len(pool)
# Slice string to remove last 2 characters from string
    server = pool[:size - 2]
    os.system('zfs send -Rv %s'%(pool) + '@golden > /DR_NAS/Solaris/Snapshots/%s'%(server) + '/%s'%(pool) + '.snapshot')

d_file = open("/tmp/poolist.txt", "r")
for line in d_file:
    stripped_line = line.strip('\n')
    pool_list.append(stripped_line)
d_file.close()
print(pool_list)

create_dir_in_DRNAS(Server_list)

for pools in pool_list:
    os.system('zfs snapshot -r %s'%(pools) + '@golden')
    copy_snapshot('%s'%(pools))

##copy snapshot

for pools in pool_list:
    os.system('zfs destroy -r %s'%(pools) + '@golden')


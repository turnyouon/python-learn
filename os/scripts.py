import subprocess
import multiprocessing
import time

def shell(cmd):
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    std_out, std_err = process.stdout, process.stderr

    errors = std_err.read()
    if errors:
        pass
    result_str = std_out.read().strip()
    if std_out:
        std_out.close()
    if std_err:
        std_err.close()

    print result_str
    return result_str


def get_zone_uuid():
    cmd = "zstack-cli QueryZone fields=uuid | grep 'uuid' | awk -F ',|:|\"' '{ print $5 }'"
    return shell(cmd)


def create_vxlan_pool(num=100):
    zone_uuid = get_zone_uuid()
    for i in range(num):
        create_vxlan_pool_cmd = "zstack-cli CreateL2VxlanNetworkPool zoneUuid=%s name=test-vxlan-%s" % (zone_uuid, i)
        multiprocessing.Process(target=shell, args=(create_vxlan_pool_cmd,)).start()
    time.sleep(10)

def delete_vxlan_pool():
    vxlan_pool_uuids = "zstack-cli QueryL2VxlanNetworkPool name~=test " \
                       "fields=uuid | grep uuid | awk -F ',|\"|:' '{print $5}'"

    result = shell(vxlan_pool_uuids)
    uuids = result.split('\n')
    for uuid in uuids:
        delete_cmd = "zstack-cli DeleteL2Network uuid=%s" % uuid
        multiprocessing.Process(target=shell, args=(delete_cmd,)).start()
       

init_cmd = "[ -f ~/.bash_profile ] && source ~/.bash_profile " \
           "&& [ -f /etc/profile ] && source /etc/profile " \
           "&& export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/root/bin:$PATH"
shell(init_cmd)
create_vxlan_pool(100)
delete_vxlan_pool()


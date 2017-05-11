import os
import multiprocessing


def shell(cmd):
    try:
        multiprocessing.Process(target=os.system, args=(cmd,)).start()
    except Exception as e:
        raise e


init_cmd = "[ -f ~/.bash_profile ] && source ~/.bash_profile " \
           "&& [ -f /etc/profile ] && source /etc/profile " \
           "&& export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/root/bin:$PATH"

shell(init_cmd)


def get_zone_uuid():
    cmd = "$(zstack-cli QueryZone fields=uuid | awk -F ',|:|\"' '/uuid {print $5}' | head -1)"
    return shell(cmd)


def create_vxlan_pool(num):
    zone_uuid = get_zone_uuid()
    vxlan_pool_name = "test-vxlan-%s"
    for i in range(num):
        create_vxlan_pool_cmd = "zstack-cli CreateL2VxlanNetworkPool zoneUuid=%s" % zone_uuid + \
                                vxlan_pool_name % i
        shell(create_vxlan_pool_cmd)


def delete_vxlan_pool():
    vxlan_pool_uuids = "zstack-cli QueryL2VxlanNetworkPool name~=test fields=uuid " \
                  "| jq '.[\"inventories\"][].\"uuid\"' | sed 's/\"//g'"

    for uuid in vxlan_pool_uuids:
        delete_cmd = "zstack-cli DeleteL2Network uuid=%s" % uuid
        shell(delete_cmd)

create_vxlan_pool(100)
delete_vxlan_pool()


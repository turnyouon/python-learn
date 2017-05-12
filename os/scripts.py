import os
import multiprocessing


def shell(cmd):
    try:
	print cmd
    except Exception as e:
        raise e


def get_zone_uuid():
    cmd = "$(zstack-cli QueryZone fields=uuid " \
	  "| jq '.[\"inventories\"][].\"uuid\"' | sed 's/\"//g'"
    return shell(cmd)


def create_vxlan_pool(num=100):
    zone_uuid = get_zone_uuid()
    vxlan_pool_name = "test-vxlan-%s"
    for i in range(num):
        create_vxlan_pool_cmd = "zstack-cli CreateL2VxlanNetworkPool zoneUuid=%s name=test-vxlan-%s" % (zone_uuid, i) 

        shell(create_vxlan_pool_cmd)


def delete_vxlan_pool():
    vxlan_pool_uuids = "zstack-cli QueryL2VxlanNetworkPool name~=test fields=uuid " \
                  "| jq '.[\"inventories\"][].\"uuid\"' | sed 's/\"//g'"

    uuids = vxlan_pool_uuids.split(' ')
    for uuid in uuids:
        delete_cmd = "zstack-cli DeleteL2Network uuid=%s" % uuid
        shell(delete_cmd)


init_cmd = "[ -f ~/.bash_profile ] && source ~/.bash_profile " \
           "&& [ -f /etc/profile ] && source /etc/profile " \
           "&& export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/root/bin:$PATH"
shell(init_cmd)

create_vxlan_pool(100)
delete_vxlan_pool()


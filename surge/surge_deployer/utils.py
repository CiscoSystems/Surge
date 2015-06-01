import os
import shutil
import yaml

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
VAGRANT_DIR = os.path.join(BASE_DIR, 'basevb/.vagrant')
STORM_VAR_DIR = os.path.join(
    BASE_DIR, 'basevb/playbooks/roles/storm-common/defaults/main.yml')
KAFKA_VAR_DIR = os.path.join(
    BASE_DIR, 'basevb/playbooks/roles/kafka/defaults/kafka.yml')


def get_zookeeper_ip(pipeline_name):
    inventory_dir = os.path.join(
        BASE_DIR, 'pipelines/'
                  +pipeline_name
                  +'/.vagrant/provisioners/ansible/inventory/deployer/vagrant_ansible_inventory')
    try:
        with open(inventory_dir) as f:
            data = f.read()
            for line in data.splitlines():
                if line.startswith("#") or not line.strip():
                    continue
                elif line.startswith("["):
                    break
                host_data = line.split(" ")
                if host_data[0] == "zookeeper":
                    return host_data[1].split("=")[1]
    except IOError:
        pass
    return ""


def is_inventory_exist(pipeline_name):
    inventory_dir = os.path.join(
        BASE_DIR, 'pipelines/'
                  +pipeline_name
                  +'/.vagrant/provisioners/ansible/inventory/deployer/vagrant_ansible_inventory')
    return os.path.exists(inventory_dir)


def remove_inventory():
    try:
        shutil.rmtree(VAGRANT_DIR)
    except OSError:
        pass


def write_storm_vars(zookeeper_ip):
    with open(STORM_VAR_DIR, 'w') as file:
        file.write(yaml.dump(
            {"zookeeper": zookeeper_ip}, default_flow_style=False))
        file.close()


def write_kafka_vars(zookeeper_ip):
    with open(KAFKA_VAR_DIR, 'w') as kafka_vars_file:
        kafka_vars_file.write(
            yaml.dump({"zookeeper": zookeeper_ip}, default_flow_style=False))
        kafka_vars_file.close()


def generate_kafka_component(pipeline_name, number_kafka=0):
    if is_inventory_exist(pipeline_name):
        number_zk = 0
        write_kafka_vars(get_zookeeper_ip())
    else:
        number_zk = 1

    pipeline = {
        'provider': {
            'type': {
                'virtualbox': {
                    'hostname_prefix': "",
                    'ip_start': '10.20.30.10'
                }
            },
        },
        'hosts': {
            "zookeeper": {
                "count": number_zk,
                "provider": {
                    'virtualbox': {
                        'memory': 1024
                    }
                }
            },
            "kafka": {
                "count": number_kafka,
                "provider": {
                    'virtualbox': {
                        'memory': 2048
                    }
                }

            }
        }
    }
    _write_pipeline_file(pipeline_name, pipeline)


def generate_storm_component(pipeline_name, number_supervisor=0):
    if is_inventory_exist(pipeline_name):
        number_zk = 0
        write_storm_vars(get_zookeeper_ip())
    else:
        number_zk = 1

    pipeline = {
        'provider': {
            'type': {
                'virtualbox': {
                    'hostname_prefix': "",
                    'ip_start': '10.20.30.10'
                }
            },
        },
        'hosts': {
            "zookeeper": {
                "count": number_zk,
                "provider": {
                    'virtualbox': {
                        'memory': 1024
                    }
                }
            },
            "storm-nimbus": {
                "count": 1,
                "provider": {
                    'virtualbox': {
                        'memory': 1024,
                            'forwarded_ports': {
                                'guest': 8080,
                                'host': 28080
                        }
                    }
                }
            },
            "storm-supervisor": {
                "count": number_supervisor,
                "provider": {
                    'virtualbox': {
                        'memory': 1024
                    }
                }
            }
        }
    }
    _write_pipeline_file(pipeline_name, pipeline)


def _write_pipeline_file(pipeline_name, pipeline_obj):
    with open(BASE_DIR + "/pipelines/" + pipeline_name + "/pipeline.yml", 'w') as pipeline_file:
        pipeline_file.write(yaml.dump(pipeline_obj, default_flow_style=False))
        pipeline_file.close()


def list_pipelines():
    return os.listdir(BASE_DIR + '/pipelines')

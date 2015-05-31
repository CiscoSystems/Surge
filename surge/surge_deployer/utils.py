import os
import shutil
import yaml

BASE_DIR = os.path.dirname(os.path.realpath(__file__))


def generate_pipeline(number_nimbus=0, number_supervisor=0,
                      number_kafka=0, number_zk=0):

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

            },
            "storm-nimbus": {
                "count": number_nimbus,
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

    with open(BASE_DIR + "/basevb/pipeline.yml", 'w') as pipeline_file:
        pipeline_file.write(yaml.dump(pipeline, default_flow_style=False))
        pipeline_file.close()

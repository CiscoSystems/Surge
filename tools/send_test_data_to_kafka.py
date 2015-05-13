

# Copyright 2015 Cisco Systems, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.


from kafka import SimpleProducer
from kafka import KafkaClient 
from kafka import KafkaConsumer

class Producer(object):

	def __init__(self, broker_ip_port):
		self.kafka = KafkaClient(broker_ip_port)	
       		self.producer = SimpleProducer(self.kafka)
	
	def send_message(self):
		 response = self.producer.send_messages("HEYA","Hello World","Kafka Deployment Worked!")
		 return [("Error ",response[0].error ), response ]

        def close(self):
		self.kafka.close()

class Consumer(object):

	def __init__(self,broker_ip_port):
		self.consumer = KafkaConsumer("HEYA", group_id="my_group",
                         metadata_broker_list=[broker_ip_port])
	
	def consume_message(self):
		print self.consumer
		for message in self.consumer :
			print message 
		print self.consumer
      


if __name__== "__main__":
	producer = Producer("172.17.1.137:9092")
	print producer.send_message()
        producer.close()
	con = Consumer("172.17.1.137:9092")
	con.consume_message()
	

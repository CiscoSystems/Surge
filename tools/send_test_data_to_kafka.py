
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
	

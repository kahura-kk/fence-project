from influxdb import InfluxDBClient


db_client = InfluxDBClient(host='127.0.0.1', port="8086")

db_client.switch_database('fence_project_db')

result = db_client.query('select last("Voltage") from "Fence_project"')
voltage = list(result.get_points())[0]['last']

result = db_client.query('select last("Current") from "Fence_project"')
current = list(result.get_points())[0]['last']


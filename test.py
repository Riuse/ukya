import unittest
import toml
from convert import convert_to_custom_format
class TestConfigConversion(unittest.TestCase):  
    def test_server_config(self):
        with open('web.toml','r') as file:
            data = toml.load(file)
        custom_format = convert_to_custom_format(data)
        expected_output = '''{
 server {
   host := @"localhost"
   port := 8080
 }
 database {
   type := @"postgres"
   host := @"db.local"
   port := 5432
   username := @"admin"
   password := @"secret"
 }
 logging {
   level := @"info"
   output := @"file"
   file_path := @"/var/log/server.log"
   max_connections_expression_problem := 120
 }
}'''
        self.assertEqual(expected_output, custom_format)

    def test_project_config(self):
        with open('project.toml','r') as file:
            data = toml.load(file)
        custom_format = convert_to_custom_format(data)
        expected_output = """{
 project {
   name := @"MyProject"
   version := @"1.0.0"
 }
 team {
   members := #( Alice, Bob, Charlie )
 }
 tasks {
   task1 {
     title := @"Design"
     due_date := @"2023-11-01"
   }
   task2 {
     title := @"Implementation"
     due_date := @"2023-12-01"
   }
   task3 {
     title := @"Testing"
     due_date := @"2024-01-01"
   }
   total_tasks_expression_problem := 6
 }
}"""
        self.assertEqual(expected_output, custom_format)

    def test_home_config(self):
        with open('home.toml','r') as file:
            data = toml.load(file)  
        custom_format = convert_to_custom_format(data)
        expected_output="""{
 home {
   location := @"New York"
   area_sqft := 2500
 }
 devices {
   number := 40
   thermostat {
     model := @"Nest"
     version := @"3.0"
   }
   lights {
     living_room := @"Philips Hue"
     kitchen := @"LIFX"
   }
   security {
     cameras := #( FrontDoor, BackYard )
     alarm := @"Ring"
   }
   total_devices_expression_problem := 43
 }
 automation {
   morning_routine {
     time := @"07:00"
     actions := #( Turn on lights, Set thermostat to 72 )
   }
   night_routine {
     time := @"22:00"
     actions := #( Turn off lights, Set thermostat to 68, Lock doors )
   }
 }
}"""
        self.assertEqual(expected_output, custom_format)

if __name__ == '__main__':
    unittest.main()

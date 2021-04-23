from sensor_generator import generate_sensor_res
import time, argparse

if __name__ == "__main__":

   arg_parser = argparse.ArgumentParser()
   arg_parser.add_argument('sleep_time', action='store', nargs='?', type=int, help = "EN_ID", default='30')
   arg_parser.add_argument('file_size', action='store', nargs='?', type=int, help = "generated file size in KB", default='10')
   args = arg_parser.parse_args()

   print(args.file_size)
   print(args.sleep_time)

   while True:
      generate_sensor_res(args.file_size)
      time.sleep(args.sleep_time)


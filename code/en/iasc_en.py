import os, sys, inspect, logging

# modify PYTHONPATH in order to imprt internal modules from parent directory.
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
from common.iasc_common import *
from en.en_tx_manager import *

if __name__ == "__main__":
    LOG_FILE_NAME = "iasc_en.log"
    logging.basicConfig(filename=LOG_FILE_NAME, level=logging.INFO, format="%(asctime)s:%(levelname)-8s %(message)s")
ignored_files = []
en_id = os.environ.get('EN_ID')


# # Configure RFM9x LoRa Radio
# CS = DigitalInOut(board.CE1)
# RESET = DigitalInOut(board.D25)
# spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
#
# # Import Python System Libraries
# import time
# # Import Blinka Libraries
# import busio
# from digitalio import DigitalInOut, Direction, Pull
# import board
# # Import the SSD1306 module.
# import adafruit_ssd1306
# # Import RFM9x
# import adafruit_rfm9x
#
# # Button A
# btnA = DigitalInOut(board.D5)
# btnA.direction = Direction.INPUT
# btnA.pull = Pull.UP
#
# # Button B
# btnB = DigitalInOut(board.D6)
# btnB.direction = Direction.INPUT
# btnB.pull = Pull.UP
#
# # Button C
# btnC = DigitalInOut(board.D12)
# btnC.direction = Direction.INPUT
# btnC.pull = Pull.UP
#
# # Create the I2C interface.
# i2c = busio.I2C(board.SCL, board.SDA)
#
# # 128x32 OLED Display
# reset_pin = DigitalInOut(board.D4)
# display = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c, reset=reset_pin)
# # Clear the display.
# display.fill(0)
# display.show()
# width = display.width
# height = display.height
#
# # Configure LoRa Radio
# CS = DigitalInOut(board.CE1)
# RESET = DigitalInOut(board.D25)
# spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
# rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, 915.0)
# rfm9x.tx_power = 23
# prev_packet = None
#
# while True:
#     packet = None
#     # draw a box to clear the image
#     display.fill(0)
#     display.text('RasPi LoRa', 35, 0, 1)
#
#     # check for packet rx
#     packet = rfm9x.receive()
#     if packet is None:
#         display.show()
#         display.text('- Waiting for PKT -', 15, 20, 1)
#     else:
#         # Display the packet text and rssi
#         display.fill(0)
#         prev_packet = packet
#         packet_text = str(prev_packet, "utf-8")
#         display.text('RX: ', 0, 0, 1)
#         display.text(packet_text, 25, 0, 1)
#         time.sleep(1)
#
#     if not btnA.value:
#         # Send Button A
#         display.fill(0)
#         button_a_data = bytes("Button A!\r\n","utf-8")
#         rfm9x.send(button_a_data)
#         display.text('Sent Button A!', 25, 15, 1)
#     elif not btnB.value:
#         # Send Button B
#         display.fill(0)
#         button_b_data = bytes("Button B!\r\n","utf-8")
#         rfm9x.send(button_b_data)
#         display.text('Sent Button B!', 25, 15, 1)
#     elif not btnC.value:
#         # Send Button C
#         display.fill(0)
#         button_c_data = bytes("Button C!\r\n","utf-8")
#         rfm9x.send(button_c_data)
#         display.text('Sent Button C!', 25, 15, 1)
#
#
#     display.show()
#     time.sleep(0.1)
##################################################

# initialization


def get_timestamp_lst(filename):
    logging.debug("[{}][{}][Entered function] filename is {}".format(__name__, inspect.currentframe().f_code.co_name, filename))
    original_filename = filename
    filename.replace("temperature_humidity_records_", "")
    filename = filename.replace(".csv", "")
    filename = filename.replace('-', '.')
    filename = filename.replace(':', '.')
    filename = filename.replace('T', '.')
    timestamp_lst = filename.split('.')
    timestamp_lst.append(original_filename)
    return timestamp_lst


def get_pending_files_queue():
    logging.debug("[{}][{}][Entered function]".format(__name__, inspect.currentframe().f_code.co_name))
    # ignored_files = []
    pending_files = []
    timestamp_lsts = []
    sorted_pending_files = []
    for filename in os.listdir(pending_dir):
        if filename in ignored_files or not filename.endswith(".csv"):
            continue
        else:
            pending_files.append(filename)
    for pending_file in pending_files:
        timestamp_lst = get_timestamp_lst(pending_file)
        timestamp_lsts.append(timestamp_lst)

    timestamp_lsts.sort()

    for lst in timestamp_lsts:
        sorted_pending_files.append(lst[-1])
    return sorted_pending_files


def send_file_to_gw(filename):
    logging.debug("[{}][{}][Entered function] filename is {}".format(__name__, inspect.currentframe().f_code.co_name, filename))
    send_file_to_gw_with_lora(filename)


pending_files_queue = get_pending_files_queue()
logging.info("[{}]: The sorted pending queue is: {}".format(__name__, str(pending_files_queue)))
for pending_file in pending_files_queue:
    send_file_to_gw(pending_file)
    # insert to pending queue

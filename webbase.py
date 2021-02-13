from enum import Enum
import subprocess
import random
import sys
import os
import shutil


class Direction(Enum):
    ONLY_DOWN = "only-down"
    ONLY_UP = "only-up"
    SINGLE = "single"
    ANY = "any"


process_counter = 0
origin_address = ""
destiny_address = ""
external_depth = 3
direction_param = ""
direction = Direction.ANY

options_read = open('webbase.txt', 'r')
options = options_read.readlines()
options_read.close()

if len(options) <= 0:
    print("[ERROR] There's no option.")
    sys.exit(-1)

index = 0
option = ""
while True:
    index = random.randint(0, len(options) - 1)
    option = options[index].strip()
    if option.startswith('#'):
        continue
    else:
        break

if option == "":
    print("[ERROR] The option is empty.")
    sys.exit(-2)

params = option.split(";")
if len(params) > 0:
    process_counter = int(params[0].strip())
if len(params) > 1:
    origin_address = params[1].strip()
if len(params) > 2:
    destiny_address = params[2].strip()
if len(params) > 3:
    external_depth = int(params[3].strip())
if len(params) > 4:
    direction_param = params[4].strip().lower()
    if direction_param == Direction.ONLY_DOWN.value:
        direction = Direction.ONLY_DOWN
    elif direction_param == Direction.ONLY_UP.value:
        direction = Direction.ONLY_UP
    elif direction_param == Direction.SINGLE.value:
        direction = Direction.SINGLE

if origin_address == "":
    print("[ERROR] The origin address is empty.")
    sys.exit(-3)

if destiny_address == "":
    print("[ERROR] The destiny address is empty.")
    sys.exit(-4)

if not destiny_address.startswith("data" + os.path.sep):
    destiny_address = "data" + os.path.sep + destiny_address

command_option = "--mirror"
if direction == Direction.SINGLE:
    command_option = "--get"
elif process_counter > 10:
    command_option = "--update"
elif process_counter > 0:
    command_option = "--continue"
command_size = "--max-files=5000000"
command_depth = "--ext-depth=" + str(external_depth)
command_walker = ""
if direction == Direction.ONLY_DOWN:
    command_walker = "--can-go-down"
elif direction == Direction.ONLY_UP:
    command_walker = "--can-go-up"

print("Making WebBase of :")
print("Process Counter   : " + str(process_counter))
print("Origin Address    : " + origin_address)
print("Destiny Address   : " + destiny_address)
print("External Depth    : " + str(external_depth))
print("Direction Walker  : " + direction.value)
print("Command Option    : " + command_option)
print("Command Walker    : " + command_walker)

if os.path.exists(destiny_address):
    if os.path.isdir(destiny_address):
        if process_counter == 0:
            shutil.rmtree(destiny_address)
            print("[INFO] Removed destiny address.")
    else:
        print("[ERROR] The destiny address is a file.")
        sys.exit(-5)
else:
    os.makedirs(destiny_address)

process_counter += 1
option = (str(process_counter) + ";" + origin_address + ";" + destiny_address +
          ";" + str(external_depth) + ";" + direction.value + "\n")
options[index] = option

options_write = open('webbase.txt', 'w')
options_write.writelines(options)
options_write.flush()
options_write.close()

subprocess.run(["httrack", command_option, origin_address, command_size,
                command_depth, command_walker, "-O", destiny_address, "-v"])

print("Finished to process one base.")

import serial
import time
import struct

# --- CONFIGURATION ---
# Remplace 'COM3' par le port de ton adaptateur USB-RS485 (ex: '/dev/ttyUSB0' sur Linux)
PORT_SERIE = '/dev/ttyUSB0' 
BAUDRATE = 115200

#select command to test
cmd_to_test = CMD_KILL
# cmd_to_test = CMD_MISSION


# --- DEFINITIONS DU PROTOCOLE ---
START_BYTE = 0x3A
END_BYTE = 0x0D
SLAVE_KILLMISSION = 4
CMD_KILL = 1
CMD_MISSION = 0

def calculate_checksum(slave, cmd, nb_byte, data_bytes):
    # Basé sur ta fonction RS485::calculateCheckSum
    checksum = START_BYTE + slave + cmd + nb_byte + END_BYTE
    for b in data_bytes:
        checksum += b
    return checksum

def send_command(ser, slave, cmd, data_bytes=[]):
    nb_byte = len(data_bytes)
    checksum = calculate_checksum(slave, cmd, nb_byte, data_bytes)
    
    # Séparation du checksum en MSB et LSB (16 bits)
    chk_msb = (checksum >> 8) & 0xFF
    chk_lsb = checksum & 0xFF
    
    # Construction de la trame binaire
    frame = bytearray([START_BYTE, slave, cmd, nb_byte])
    frame.extend(data_bytes)
    frame.extend([chk_msb, chk_lsb, END_BYTE])
    
    print(f"-> Envoi de la trame : {[hex(x) for x in frame]}")
    ser.write(frame)

def receive_command(data_bytes):
    nb_byte = len(data_bytes)

    start_byte = data_bytes[0]
    slave = data_bytes[1]
    cmd = data_bytes[2]
    size = data_bytes[3]

    end_data = 4+size
    data = data_bytes[4:end_data]

    checksum = (data_bytes[end_data] * 256) + data_bytes[end_data+1]
    end_byte = data_bytes[end_data+2]

    test_result = True
    print("==================================")

    if start_byte == START_BYTE:
        print("    start byte OK")
    else:
        print("    start byte ERROR")
        test_result = False

    if slave == SLAVE_KILLMISSION:
        print("    addr byte OK")
    else:
        print("    addr byte ERROR")
        test_result = False


    if cmd == CMD_KILL:
        print("    cmd kill OK")
        print("    kill state : {}".format(data[0]))
    elif cmd == CMD_MISSION:
        print("    cmd mission OK")
        print("    mission state : {}".format(data[0]))
    else:
        print("    cmd ERROR")
        test_result = False

    if size == nb_byte - 7:
        print("    size byte OK")
    else:
        print("    size byte ERROR")
        test_result = False


    expected_checksum = calculate_checksum(slave,cmd,size,data)
    if checksum == expected_checksum:
        print("    checksum byte OK")
    else:
        print("    checksum byte ERROR")
        test_result = False


    if end_byte == END_BYTE:
        print("    end byte OK")
    else:
        print("    end byte ERROR")
        test_result = False

    if test_result:
        print("MSG: OK")
    else:
        print("MSG: ERROR")
    print("==================================")

def main():


    try:
        # Ouverture du port série
        with serial.Serial(PORT_SERIE, BAUDRATE, timeout=1) as ser:
            print(f"Port {PORT_SERIE} ouvert avec succès à {BAUDRATE} bauds.")
            while True:
                # On demande l'état du KillSwitch (CMD_KILL) avec 0 octet de donnée
                send_command(ser, SLAVE_KILLMISSION, CMD_KILL, [])
                
                # Attente et lecture de la réponse de la carte
                time.sleep(0.1) 
                if ser.in_waiting > 0:
                    response = ser.read(ser.in_waiting)
                    print(f"<- Réponse reçue : {[hex(x) for x in response]}")
                    receive_command(response)
                else:
                    print("<- Aucune réponse de la carte...")
                
                time.sleep(1) # Pause d'une seconde avant le prochain ping

    except serial.SerialException as e:
        print(f"Erreur d'ouverture du port série : {e}")
    except KeyboardInterrupt:
        print("\nTest arrêté par l'utilisateur.")

if __name__ == "__main__":
    main()
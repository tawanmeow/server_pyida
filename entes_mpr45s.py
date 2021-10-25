from pyModbusTCP.client import ModbusClient
import json
import win_inet_pton
import struct

def converter(startingAddress, IP_ADDRESS, UNIT_ID):
    client = ModbusClient()
    client.host(IP_ADDRESS)
    client.port(502)
    client.unit_id(UNIT_ID)
    client.debug()
    if not client.is_open():
        if not client.open():
            return ""

    if client.is_open():
        payloadDict = {"voltage": {}, "current": {}, "frequency": {}}
        voltage = startingAddress
        voltageValue = client.read_holding_registers(voltage, 14) # Return list that contains integer.
        counter = 0
        for i in range(0,len(voltageValue)):
            if i % 2 != 0:
                counter +=  1
                result = float(voltageValue[i]) * 0.1
                result = ("%.1f" % result)
                payloadDict["voltage"]["V" + str(counter)] = float(result)

        current = startingAddress + 14
        currentValue = client.read_holding_registers(current, 10) # Return list that contains integer.
        counter = 0
        for i in range(0,len(currentValue)):
            if i % 2 != 0:
                counter +=  1
                result = float(currentValue[i]) * 0.001
                result = ("%.1f" % result)
                payloadDict["current"]["A" + str(counter)] = float(result)

        frequency = current + 2
        frequencyValue = client.read_holding_registers(frequency, 2) # Return list that contains integer.
        counter = 0
        result = float(frequencyValue[1]) * 0.01
        result = ("%.2f" % result)
        payloadDict["frequency"] = float(result)
        client.close()

        return payloadDict

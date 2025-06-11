# modbus_tcp.py - MyScan v1.0.1 - Custom Build
# Developed by Mustafa AYDIN for SAVRONIK

from pymodbus.client import ModbusTcpClient
from pymodbus.exceptions import ModbusException

def read_registers_by_type(ip, port, unit_id, address, count, register_type):
    try:
        client = ModbusTcpClient(host=ip, port=port)
        if not client.connect():
            return "Connection failed"
        
        if register_type == "Holding":
            response = client.read_holding_registers(address=address, count=count, slave=unit_id)
        elif register_type == "Input":
            response = client.read_input_registers(address=address, count=count, slave=unit_id)
        elif register_type == "Coil":
            response = client.read_coils(address=address, count=count, slave=unit_id)
        elif register_type == "Discrete":
            response = client.read_discrete_inputs(address=address, count=count, slave=unit_id)
        else:
            client.close()
            return f"Unsupported register type: {register_type}"

        client.close()

        if response.isError():
            return f"Modbus Error: {response}"

        # Correct data extraction based on register type
        if hasattr(response, 'registers'):
            return response.registers
        elif hasattr(response, 'bits'):
            return response.bits
        else:
            return f"No data returned for {register_type}"

    except ModbusException as e:
        return f"Modbus Exception: {str(e)}"
    except Exception as e:
        return f"Exception: {str(e)}"

def write_single_register(ip, port, unit_id, address, value):
    try:
        client = ModbusTcpClient(ip, port=port)
        if not client.connect():
            return "Connection failed"

        response = client.write_register(address=address, value=value, slave=unit_id)
        client.close()

        return "Success" if not response.isError() else f"Modbus Error: {response}"
    except Exception as e:
        return f"Exception: {str(e)}"

def write_single_coil(ip, port, unit_id, address, value):
    try:
        client = ModbusTcpClient(ip, port=port)
        if not client.connect():
            return "Connection failed"

        response = client.write_coil(address=address, value=bool(value), slave=unit_id)
        client.close()

        return "Success" if not response.isError() else f"Modbus Error: {response}"
    except Exception as e:
        return f"Exception: {str(e)}"

def write_multiple_registers(ip, port, unit_id, address, values):
    try:
        client = ModbusTcpClient(ip, port=port)
        if not client.connect():
            return "Connection failed"

        response = client.write_registers(address=address, values=values, slave=unit_id)
        client.close()

        return "Success" if not response.isError() else f"Modbus Error: {response}"
    except Exception as e:
        return f"Exception: {str(e)}"

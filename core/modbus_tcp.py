# core/modbus_tcp.py
from pymodbus.client import ModbusTcpClient

def read_holding_registers(ip, port=502, unit_id=1, address=0, count=5):
    try:
        client = ModbusTcpClient(ip, port=port)
        connection = client.connect()

        if not connection:
            return "Connection failed"

        response = client.read_holding_registers(address=address, count=count, unit=unit_id)
        client.close()

        if response.isError():
            return f"Modbus Error: {response}"
        else:
            return response.registers

    except Exception as e:
        return f"Exception: {str(e)}"
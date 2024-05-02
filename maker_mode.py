import usb.core
import usb.util
import time

def findDevice(vendor_id, product_id):
    dev = usb.core.find(idVendor=vendor_id, idProduct=product_id)
    if dev is None:
        raise ValueError(f"Device with Vendor ID {vendor_id} and Product ID {product_id} not found")
    return dev

def printDescription(device):
    try:
        device_desc = bytearray(device.ctrl_transfer(0x80, 0x06, 0x0100, 0x00, 0x40)).hex()
        other_desc = bytearray(device.ctrl_transfer(0x80, 0x06, 0x0200, 0x00, 0x40)).hex()
        print(f"Device descriptor: {device_desc}")
        print(f"Other descriptor: {other_desc}")
    except usb.core.USBError as e:
        print(f"Error getting device descriptors: {e}")

def printDevinfo(device):
    try:
        print(f"Serial number: {device.serial_number}")
        print(f"Manufacturer: {device.manufacturer}")
    except usb.core.USBError as e:
        print(f"Error getting device info: {e}")

def ctrlTransRd(device, bmRequestType, bRequest, wValue, wIndex, data_or_wLength, read_endpoint, read_length):
    try:
        device.ctrl_transfer(bmRequestType, bRequest, wValue, wIndex, data_or_wLength)
        return bytearray(device.read(read_endpoint, read_length)).hex()
    except usb.core.USBError as e:
        print(f"Error in control transfer or read: {e}")
        return None
    
def sendData(device, endpoint, data):
    try:
        device.write(endpoint, data)
        print(f"Data Transfered: {data.hex()}")
    except usb.core.USBError as e:
        print(f"Error sending data to device: {e}")

def readResp(device, endpoint, length):
    try:
        resp = bytearray(device.read(endpoint, length)).hex()
        print(f"Response: {resp}")
    except usb.core.USBError as e:
        print(f"Error reading response: {e}")

def main():
    VENDOR_ID = 0x04dd
    PRODUCT_ID = 0x92d1

    dev = findDevice(VENDOR_ID, PRODUCT_ID)
    printDescription(dev)
    printDevinfo(dev)

    epidx = 0
    epdst = 0x81
    epindata = 3
    
    epdst_resp = 0x82

    mode_support = ctrlTransRd(dev, 0x41, 0x62, 0x00, epidx, b"\x02\xC0", epdst, 256)
    if mode_support:
        print("Mode Support: " + mode_support)

    mode_set = ctrlTransRd(dev, 0x41, 0x60, 0xC0, epidx, None, epdst, 256)
    if mode_set:
        print("Mode Set: " + mode_set)

    payload_systemset = bytes.fromhex("FF 55 56 42 00 03 C1 01 01 FE")
    sendData(dev, epindata, payload_systemset)
    readResp(dev, epdst_resp, 256)
    
    time.sleep(10)

    #payload_imeird = bytes.fromhex("FF 55 56 42 00 02 C1 03 FE")
    #sendData(dev, epindata, payload_imeird)
    #readResp(dev, epdst_resp, 256)
    
    #payload_0x5 = bytes.fromhex("FF 55 56 42 00 02 C1 05 FE")
    #sendData(dev, epindata, payload_0x5)
    #readResp(dev, epdst_resp, 256)
    
    #payload_manurd = bytes.fromhex("FF 55 56 42 00 02 C1 07 FE")
    #sendData(dev, epindata, payload_manurd)
    #readResp(dev, epdst_resp, 256)
    
    #payload_0x9 = bytes.fromhex("FF 55 56 42 00 02 C1 09 FE")
    #sendData(dev, epindata, payload_0x9)
    #readResp(dev, epdst_resp, 256)
    
    payload_reboot = bytes.fromhex("FF 55 56 42 00 03 C1 01 FE")
    sendData(dev, epindata, payload_reboot)
    readResp(dev, epdst_resp, 256)

if __name__ == "__main__":
    main()

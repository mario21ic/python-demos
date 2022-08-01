import usb.core

dev = usb.core.find(idVendor=0x0810, idProduct=0xe501)
if not dev:
    print("Could not find device :(")
    exit(1)

ep = dev[0].interfaces()[0].endpoints()[0]
i = dev[0].interfaces()[0].bInterfaceNumber
print("dev:", dev)
print("ep:", ep)
print("i:", i)
dev.reset()

# To detach
if dev.is_kernel_driver_active(i):
    print("detach")
    dev.detach_kernel_driver(i)

dev.set_configuration()
eaddr = ep.bEndpointAddress

r = dev.read(eaddr, 1024)
print("r:", r)
print(len(r))

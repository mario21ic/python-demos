import usb.core

dev = usb.core.find(idVendor=0x0781, idProduct=0x5597)
ep = dev[0].interfaces()[0].endpoints()[0]
i = dev[0].interfaces()[0].bINterfaceNumber
print("i:", i)
exit()
dev.reset()

if dev.is_kernel_driver_active(i):
    dev.detach_kernel_driver(i)

dev.set_configuration()
eaddr = ep.bEndpointAddress

r = dev.read(eaddr, 1024)
print(len(r))

import explorerhat
from time import sleep

print ("motor one")
explorerhat.motor.one.forward(100)
sleep(2)
explorerhat.motor.one.stop()

print ("motor two")
explorerhat.motor.two.forward(100)
sleep(2)
explorerhat.motor.two.stop()

print ("stop")

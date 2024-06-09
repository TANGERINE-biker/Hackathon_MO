from pymavlink import mavutil
import os
import time
import vlc
import RPi.GPIO as IO
import time  

os.system("gpio mode 0 out")
os.system("gpio mode 2 out")


def check(temp, current_arr):
    is_continue = 0
    #if(temp.chan1_raw != current_arr.chan1_raw):
    #    is_continue = False
    #elif(temp.chan2_raw != current_arr.chan2_raw):
    #    is_continue = False
    #elif(temp.chan3_raw != current_arr.chan3_raw):
    #    is_continue = False
    #elif(temp.chan4_raw != current_arr.chan4_raw):
    #    is_continue = False
    if(temp.chan5_raw != current_arr.chan5_raw):
        is_continue = 5
    elif(temp.chan6_raw != current_arr.chan6_raw):
        is_continue = 6
    elif(temp.chan7_raw != current_arr.chan7_raw):
        is_continue = 7
    elif(temp.chan8_raw != current_arr.chan8_raw):
        is_continue = 8
    #elif(temp.chan9_raw != current_arr.chan9_raw):
    #    is_continue = False
    #elif(temp.chan10_raw != current_arr.chan10_raw):
    #    is_continue = False
    return is_continue


# Start a connection listening on a UDP port
the_connection = mavutil.mavlink_connection('/dev/ttyAMA2')

# Wait for the first heartbeat
#   This sets the system and component ID of remote system for the link
the_connection.wait_heartbeat()
#print("Heartbeat from system (system %u component %u)" % (the_connection.target_system, the_connection.target_component))

#print(the_connection.messages["RC_CHANNELS"])

temp = the_connection.recv_match(type="RC_CHANNELS",blocking=True)
#print(type(temp.chan7_raw))
#print(temp)
hello1 = vlc.MediaPlayer("/home/admin/button/suunds/0001.mp3")
music1 = vlc.MediaPlayer("/home/admin/button/suunds/Pulse of the Maggots.mp3")

IO.setwarnings(False)            # отключаем показ любых предупреждений
IO.setmode (IO.BCM)              # мы будем программировать контакты GPIO по их функциональным номерам (BCM), то есть мы будем обращаться к PIN35 как ‘GPIO19’
IO.setup(19,IO.OUT)              # инициализируем GPIO19 в качестве цифрового выхода

p = IO.PWM(19,1000)               # настраиваем GPIO19 в качестве ШИМ выхода с частотой ШИМ сигнала 100 Гц
p.start(0)  
IO.setup(18,IO.OUT) 
pz = IO.PWM(18,1000)               # настраиваем GPIO19 в качестве ШИМ выхода с частотой ШИМ сигнала 100 Гц
pz.start(0)                     # начинаем формирование ШИМ сигнала с коэффициентом заполнения 0%
#print(dir(p))


while True:
    current_arr = the_connection.recv_match(type="RC_CHANNELS",blocking=True)
    is_continue = check(temp, current_arr)
    #print(is_continue)
    if(is_continue == 0):
        continue

    if(is_continue == 5):
        if(current_arr.chan5_raw == 240):
            music1.play()
        else:
            music1.stop()
        print("5")
    elif(is_continue == 6):
        IO.setup(18,IO.OUT) 
        IO.setup(19,IO.OUT) 
        while (current_arr.chan6_raw == 240):
            print(current_arr.chan6_raw)
            if(current_arr.chan6_raw == 1807):
                p.stop()  
                pz.stop()
                IO.cleanup()
                GPIO.output(18, GPIO.LOW)
                GPIO.output(19, GPIO.LOW)
                p.ChangeFrequency(0)
                pz.ChangeFrequency(0)
                break
            p.ChangeDutyCycle(40)  
            pz.ChangeDutyCycle(40)  
            p.ChangeFrequency(300)
            pz.ChangeFrequency(300)
            time.sleep(0.4)
            p.ChangeFrequency(100)
            pz.ChangeFrequency(100)
            time.sleep(0.4)
            current_arr = the_connection.recv_match(type="RC_CHANNELS",blocking=True)
        print("6")
    elif(is_continue == 7):
        #print(current_arr.chan7_raw)
        if(current_arr.chan7_raw == 240):
            os.system("gpio write 0 1")
            os.system("gpio write 2 0")
        elif(current_arr.chan7_raw == 1807):
            os.system("gpio write 0 0")
            os.system("gpio write 2 1")
        else:
            os.system("gpio write 0 0")
            os.system("gpio write 2 0")

        print("7")
    elif(is_continue == 8):
        if(current_arr.chan8_raw == 240):
            #p = vlc.MediaPlayer("0001.mp3")
            #p.play()
            hello1.play()
        else:
            hello1.stop()

        print("8")


    temp = current_arr
    

    #msg = the_connection.recv_match(type="RC_CHANNELS",blocking=True).chan7_raw
    #print(f"{msg}\r")
    time.sleep(0.2)
    #print(the_connection.messages["RC_CHANNELS"])

the_connection.close()

# Once connected, use 'the_connection' to get and send messages

# chan1_raw joy2 lr
# chan2_raw joy2 up down
# chan3_raw joy1 up down
# chan4_raw joy1 lr
# chan5_raw swa
# chan6_raw swb
# chan7_raw swc
# chan8_raw swd
# chan9_raw vra
# chan10_raw vrb
# chan11_raw
# chan12_raw
# chan13_raw
# chan14_raw
# chan15_raw
# chan16_raw
# chan17_raw
# chan18_raw

# 1807
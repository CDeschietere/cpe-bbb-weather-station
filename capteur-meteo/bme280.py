
import Adafruit_BBIO.GPIO as GPIO
from Adafruit_I2C import Adafruit_I2C

def set_bme280_config(i2c):
	#Humidite
	i2c.write8(0xF2, 0x05 & 0x07) #Ecrit dans le registre de conf de l'humidite
	#MEA
	i2c.write8(0xF4, ((0x05 & 0x07) << 5) | ((0x05 & 0x07) << 2) | (0x03 & 0x03))
	#config
	i2c.write8(0xF5, ((0x01 & 0x07) << 5) | ((0x00 & 0x07) << 2))

def prepare_read_for_temp_20(list_bytes):
	#temp = ((list_bytes[0] & 0xFF) << 12) | ((list_bytes[1] & 0xFF) << 4) | ((list_bytes[2] & 0xF0) >> 4)
	concat = str("%X" % list_bytes[0]) + str( "%X" % list_bytes[1]) + str( "%X" % (list_bytes[2] & 0xF0))
	#print("val hex: 0x" + concat[0:5])
	return int(concat[0:5], 16)

def prepare_read_for_hum_16(list_bytes):
	concat = str("%X" % list_bytes[0]) + str( "%X" % list_bytes[1]) + str( "%X" % (list_bytes[2] & 0xF0))
	#print("val hex: 0x" + concat[0:4])
	return int(concat[0:4], 16)

def compensate_hum(temp, hum, i2c):
	uhum = prepare_read_for_hum_16(hum)
	utemp = prepare_read_for_temp_20(temp)
	temp1 = ((((utemp >> 3) - (i2c.readU16(0x88) << 1))) * (i2c.readS16(0x8A))) >> 11
	temp2 = (((((utemp >> 4) - i2c.readU16(0x88)) * ((utemp >> 4) - i2c.readU16(0x88))) >> 12) * i2c.readS16(0x8C)) >> 14
	t_fine = temp1 + temp2
	v_xl_u32r = (t_fine - 76800)
	v_xl_u32r = (((((hum << 14) - ((i2c.readS16(0xE4)) << 20) - ((i2c.readS16(0xE5)) * v_xl_u32r)) + (16384) >> 15) * (((((((v_x1_u32r * (i2c.readS16(0xE7))) >> 10) * (((v_x1_u32r * ((i2c.readS16(0xE3))) >> 11) + (32768))) >> 10) + (2097152)) * ((v_x1_u32r * (i2c.readS16(0xE1)) + 8192) >> 14))))))

def compensate_temp(temp, i2c):
	utemp = prepare_read_for_temp_20(temp)
	
	temp1 = ((((utemp >> 3) - (i2c.readU16(0x88) << 1))) * (i2c.readS16(0x8A))) >> 11
	temp2 = (((((utemp >> 4) - i2c.readU16(0x88)) * ((utemp >> 4) - i2c.readU16(0x88))) >> 12) * i2c.readS16(0x8C)) >> 14
	t_fine = temp1 + temp2
	temperature = (((temp1 + temp2) * 5) + 128) >> 8
	return temperature

def compensate_press():
	pass

def get_temperature():
	i2c = Adafruit_I2C(0x76, 2, True)
	set_bme280_config(i2c)
	#print("Humidite non compensee : " + str(i2c.readS16(0xFE))) #lecture de l'humidite
	#print("Temperature : " + str(compensate_temp(i2c.readList(0xFA, 3), i2c))) #lecture de la temp
	#print("Pression non compensee : " + str(i2c.readU16(0xF8))) #lecture de la pression
	temp = str(compensate_temp(i2c.readList(0xFA, 3), i2c))
	string = '{:.2}'.format(temp) + "." + temp[-2:]
	return "{temperature:'"+string+"'}"


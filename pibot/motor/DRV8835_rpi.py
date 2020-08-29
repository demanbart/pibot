import wiringpi as wiringpi2
import pibot.motor.motor

# Motor speeds for this library are specified as numbers
# between -MAX_SPEED and MAX_SPEED, inclusive.
_max_speed = 480  # 19.2 MHz / 2 / 480 = 20 kHz
MAX_SPEED = _max_speed

io_initialized = False
def io_init():
  global io_initialized
  if io_initialized:
    return

  wiringpi2.wiringPiSetupGpio()
  wiringpi2.pinMode(12, wiringpi2.GPIO.PWM_OUTPUT)
  wiringpi2.pinMode(13, wiringpi2.GPIO.PWM_OUTPUT)

  wiringpi2.pwmSetMode(wiringpi2.GPIO.PWM_MODE_MS)
  wiringpi2.pwmSetRange(MAX_SPEED)
  wiringpi2.pwmSetClock(2)

  wiringpi2.pinMode(5, wiringpi2.GPIO.OUTPUT)
  wiringpi2.pinMode(6, wiringpi2.GPIO.OUTPUT)

  io_initialized = True

class DRV8835RpiMotor(object):
    MAX_SPEED = _max_speed

    def __init__(self, pwm_pin, dir_pin):
        self.pwm_pin = pwm_pin
        self.dir_pin = dir_pin

    def setSpeed(self, speed):
        if speed < 0:
            speed = -speed
            dir_value = 1
        else:
            dir_value = 0

        if speed > MAX_SPEED:
            speed = MAX_SPEED

        io_init()
        wiringpi2.digitalWrite(self.dir_pin, dir_value)
        wiringpi2.pwmWrite(self.pwm_pin, speed)

class DRV8835RpiMotors(object):
    MAX_SPEED = _max_speed

    def __init__(self):
        self.motor1 = DRV8835RpiMotor(12, 5)
        self.motor2 = DRV8835RpiMotor(13, 6)

    def setSpeeds(self, m1_speed, m2_speed):
        self.motor1.setSpeed(m1_speed)
        self.motor2.setSpeed(m2_speed)

class DRV8835(pibot.motor.motor.Motor):
    def __init__(self):
         self.__driverName = "DRV8835"
         self.__driverBrand = "Pololu"
         self.__driverDescription = "Dual motor driver kit for Raspberry Pi B+, DRV8835 dual H-bridge motor driver IC, Continuous output current per channel: 1.2A, PWM frequency: 250 kHz (maximum) ,The DRV8835 Dual Motor Driver Kit for Raspberry Pi B+ provides an easy and low-cost solution for driving a pair of small brushed DC motors with a Raspberry Pi Model B+. The expansion board features Texas Instruments' DRV8835 dual H-bridge motor driver IC."
         self.__driverUrl = "https://www.pololu.com/product/2753"
         self.__commandStructure = {"motor1": "int:0-248", "motor2": "int:0-248"}
         self.motors = DRV8835RpiMotors()
     
    
    def execute(self,command):
        #check if given command complies with the commandstructure before sending"
        if self.validate_command_structure(command, self.__commandStructure):
            self.motors.setSpeeds(command["motor1"], command["motor2"])



# pip install pid
from pid import Pid

class PID:

    def __init__(self, setpoint=27, Kp=1, Ki=0, Kd=0) -> None:
        self.setpoint = setpoint
        self.Kp = Kp 
        self.Ki = Ki 
        self.Kd = Kd
        self.controller = Pid(self.Kp, self.Ki, self.Kd)
         
    def GetActuatorOutput(self, feedback):
        output = self.controller(feedback, self.setpoint)
        return output
        
    def set_parameters(self, setpoint, Kp, Ki, Kd):
            self.setpoint = setpoint
            self.Kp = Kp
            self.Ki = Ki
            self.Kd = Kd
            self.controller.setKp(self.Kp)
            self.controller.setKi(self.Ki)
            self.controller.setKd(self.Kd)
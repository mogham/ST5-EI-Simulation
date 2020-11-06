from enum import Enum
from random import random

P = lambda x: random() < x

class System:
    def __init__(self, numberMachine, machines, buffers):
        self.numberMachine = numberMachine
        self.numberBuffer = numberMachine - 1
        self.historicState = []
        self.machines = machines
        self.buffers = buffers
    
class MachineLineNode:
    
    def __init__ (self, name):
        self.name = name
    
    def __str__ (self):
        return f'NODE:{self.name}'

class Machine (MachineLineNode):
    
    def __init__ (self, breakdown_prob, repair_prob, upstream_buf, downstream_buf, name):
        self.up_to_down, self.down_to_up = breakdown_prob, repair_prob
        self.upstream, self.downstream = upstream_buf, downstream_buf
        super(Machine, self).__init__(name)
        
        self.reset()
    
    def reset (self):
        self.is_up = True

    def is_blocked (self):

        return self.downstream.is_full() or self.upstream.is_empty()
    
    def phase_1_rand (self):
        self.work = False       # States if machine will work on time slot
        self.release = False    # States if machine will release its object on time slot
        
        if self.is_up and not self.is_blocked():
            self.is_up = not P(self.up_to_down)
            self.work = True
            self.release = self.is_up
            
        elif not self.is_up:
            self.is_up = P(self.down_to_up)
            self.work = False
            self.release = self.is_up
    
    def phase_1_manu (self):
        if self.is_up and not self.is_blocked():
            pass # Break machine?
        elif not self.is_up:
            pass # Repair machine?
    
    def phase_2 (self):
        if self.work:
            self.upstream.pop()
        if self.release:
            self.downstream.push()
    
    def __str__ (self):
        return f'MACHINE:{self.name}' + f' - {"UP" if self.is_up else "DOWN"}'

class Buffer (MachineLineNode):
    
    class Type (Enum):
        MIDDLE = 0
        INPUT = 1
        OUTPUT = 2
    
    def __init__ (self, buffer_type, capacity, name):
        self.type = buffer_type
        if self.type == Buffer.Type.MIDDLE: self.capacity = capacity
        super(Buffer, self).__init__(name)  
        self.reset()
    
    def reset (self):
        if self.type == Buffer.Type.MIDDLE: self.current = 0
    
    def is_full (self):
        if self.type == Buffer.Type.MIDDLE:
            return self.current == self.capacity
        elif self.type == Buffer.Type.OUTPUT:
            return False
    
    def is_empty (self):
        if self.type == Buffer.Type.MIDDLE:
            return self.current == 0
        elif self.type == Buffer.Type.INPUT:
            return False
    
    def pop (self):
        if self.type == Buffer.Type.MIDDLE:
            self.current -= 1

    def push (self):
        if self.type == Buffer.Type.MIDDLE:
            self.current += 1

    def __str__ (self):
        if self.type == Buffer.Type.MIDDLE:
            return f'BUFFER:{self.name}' + f' - {self.current}/{self.capacity}'
        else:
            return f'BUFFER:{self.name}' + f' - {"INPUT" if self.type == Buffer.Type.INPUT else "OUTPUT"}'

INPUT_BUF = Buffer(Buffer.Type.INPUT, 0, "INPUT")       # MUST BE USED AS INPUT BUFFER OF THE MACHINE LINE
OUTPUT_BUF = Buffer(Buffer.Type.OUTPUT, 0, "OUTPUT")    # MUST BE USED AS OUTPUT BUFFER OF THE MACHINE LINE
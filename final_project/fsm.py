class FSM :
    def __init__(self) :
        self.fsm = {}
        self.current_state = 1
    
    def add_transtition(self, input_symbol, input_state, action, new_state) :
        self.fsm[(input_symbol, input_state)] = (action, new_state)

    def get_transition(self, input_state) :
        return self.fsm[(input_state, self.current_state)]

    def process(self, input_state) :
        (action, new_state) = self.get_transition(input_state)
        if action != None :
            action()
        self.current_state = new_state

    def get_state(self) :
        return self.current_state
    
        
    
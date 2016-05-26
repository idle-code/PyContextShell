
class State:
    def __init__(on_enter = None, on_exit = None):
        self.on_enter = on_enter if on_enter != None else lambda: pass
        self.on_exit = on_exit if on_exit != None else lambda: pass

    def enter(self):
        self.on_enter()

    def exit(self):
        self.on_exit()

class StateMachine:
    def __init__(self, start_state, end_state):
        self.states = [start_state, end_state]
        self.current_state = start_state
        self.current_state.enter()


start_of_line = State(lambda: print("Entering start"), lambda: print("Exiting start"))
end_of_line = State(lambda: print("End reached"))

sm = StateMachine(start_of_line, end_of_line)
sm.add_transition(start_of_line,  end_of_line)




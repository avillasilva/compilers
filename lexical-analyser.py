def prime(fn):
    def wrapper(*args, **kwargs):
        v = fn(*args, **kwargs)
        v.send(None)
        return v
    return wrapper

class LexicalAnalyser:
    def __init__(self):
        self.q1 = self._create_q1()
        self.q2 = self._create_q2()
        self.q3 = self._create_q3()
        self.q4 = self._create_q4()
        self.q5 = self._create_q5()
        self.q6 = self._create_q6()

        self.current_state = self.q1
        self.stopped = False

        self.keywords = ['program', 'var', 'integer', 'real', 'boolean', 
        'procedure', 'begin', 'end', 'if', 'then', 'else', 'while', 
        'do', 'not']
        self.delimiters = [';', '.', '(', ')', ':', ',']
        self.buffer = ''
        self.lines = 1

    def send(self, char):
        try:
            self.current_state.send(char)
        except StopIteration:
            self.stopped = True

    def does_match(self):
        if self.stopped:
            return False

        if self.current_state == self.q3:
            if self.buffer in self.keywords:
                print(self.buffer, '\t', 'keyword', '\t', self.lines)
            else:
                print(self.buffer, '\t', 'identifier', '\t', self.lines)
        
        elif self.current_state == self.q4:
            print(self.buffer, '\t', 'integer number', '\t', self.lines)
        
        elif self.current_state == self.q5:
            print(self.buffer, '\t', 'real number', '\t', self.lines)
        
        elif self.current_state == self.q6:
            print(self.buffer, '\t', 'real number', '\t', self.lines)

        elif self.buffer in self.delimiters:
            print(self.buffer, '\t', 'delimiter', '\t', self.lines)
        
        self.buffer = ''

    @prime
    def _create_q1(self):
        # Initial state
        while True:
            char = yield
            if char == ' ':
                self.current_state = self.q1
            
            elif char == '\n':
                self.lines += 1
                self.current_state = self.q1
            
            elif char == '{':
                self.current_state = self.q2
            
            elif char.isalpha():
                self.buffer += char
                self.current_state = self.q3
            
            elif char.isdigit():
                self.buffer += char
                self.current_state = self.q4
            
            # elif char == ':':
            #     self.buffer += char
            #     self.current_state = self.q6
            
            # elif char == '<' or char == '>':
            #     self.buffer += char
            #     self.current_state = self.q6
            
            # elif char in self.delimiters:
            #     self.buffer += char
            #     self.current_state = self.q6
            
            else:
                break
    
    @prime
    def _create_q2(self):
        # check if the input is a comment
        while True:
            char = yield
            if char == '}':
                self.current_state = self.q1
            else:
                self.current_state = self.q2
    
    @prime
    def _create_q3(self):
        # check if the input is an identifier or a keyworld
        while True:
            char = yield
            if char == '_' or char.isalpha() or char.isdigit():
                self.buffer += char
                self.current_state = self.q3
            else:
                self.does_match()
                self.current_state = self.q1
                self.current_state.send(char)
    
    @prime
    def _create_q4(self):
        # check if the input is an integer number
        while True:
            char = yield
            if char.isdigit():
                self.buffer += char
                self.current_state = self.q4
            elif char == '.':
                self.buffer += char
                self.current_state = self.q5
            else:
                self.does_match()
                self.current_state = self.q1
                self.current_state.send(char)

    @prime
    def _create_q5(self):
        # check if the input is a real number
        while True:
            char = yield
            if char.isdigit():
                self.buffer += char
                self.current_state = self.q5
            else:
                self.does_match()
                self.current_state = self.q1
                self.current_state.send(char)
    
    @prime
    def _create_q6(self):
        # check if the input is a delimiter or a assignment command
        while True:
            char = yield
            if char == '=' and self.buffer == ':':
                self.buffer += char
                self.does_match()
                self.current_state = self.q1
                self.current_state.send(char)
            else:
                self.does_match()
                self.current_state = self.q1
                self.current_state.send(char)

def analyse(text):
    evaluator = LexicalAnalyser()
    for ch in text:
        evaluator.send(ch)
    return evaluator.does_match()

program = open('program.txt', 'r')
analyse(program.read())
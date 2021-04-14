def prime(fn):
    def wrapper(*args, **kwargs):
        v = fn(*args, **kwargs)
        v.send(None)
        return v
    return wrapper

class LexicalAnalyser:
    def __init__(self, input):
        self.q1 = self._create_q1()
        self.q2 = self._create_q2()
        self.q3 = self._create_q3()
        self.q4 = self._create_q4()
        self.q5 = self._create_q5()
        self.q6 = self._create_q6()
        self.q7 = self._create_q7()
        self.q8 = self._create_q8()
        self.q9 = self._create_q9()
        self.q10 = self._create_10()
        
        self.reader = open(input, 'r')
        self.current_state = self.q1
        self.stopped = False

        self.keywords = ['program', 'var', 'integer', 'real', 'boolean', 
        'procedure', 'begin', 'end', 'if', 'then', 'else', 'while', 
        'do', 'not']
        self.delimiters = [';', '.', '(', ')', ':', ',']
        self.buffer = ''
        self.lines = 1

        self.output = open('output/output.txt', 'w')
    
    def analyse(self):
        while True:
            char = self.reader.read(1)
            self.send(char)
            if not char:
                self.send(None)
                break
        self.reader.close()
        self.output.close()

    def send(self, char):
        try:
            self.current_state.send(char)
        except StopIteration:
            self.stopped = True

    def does_match(self):
        if self.stopped:
            if self.current_state == self.q2:
                print('Missing comment delimiter: }')
            else:
                print('Error at line', self.lines, ' - token not recognized: ', self.buffer)
            return False

        if self.current_state == self.q3:
            if self.buffer in self.keywords:
                self.output.write(self.buffer + ' keyword ' + str(self.lines) + '\n')
            else:
                self.output.write(self.buffer + ' identifier ' + str(self.lines) + '\n')
        
        elif self.current_state == self.q4:
            self.output.write(self.buffer + ' integer ' + str(self.lines) + '\n')
        
        elif self.current_state == self.q5:
            self.output.write(self.buffer + ' real ' + str(self.lines) + '\n')
        
        elif self.current_state == self.q6:
            if self.buffer == ':=':
                self.output.write(self.buffer + ' assignment ' + str(self.lines) + '\n')
            else:
                self.output.write(self.buffer + ' delimiter ' + str(self.lines) + '\n')

        elif self.current_state == self.q7:
            self.output.write(self.buffer + ' relational ' + str(self.lines) + '\n')
        
        elif self.current_state == self.q8:
            self.output.write(self.buffer + ' additive ' + str(self.lines) + '\n')
        
        elif self.current_state == self.q9:
            self.output.write(self.buffer + ' multiplicative ' + str(self.lines) + '\n')
        
        elif self.current_state == self.q10:
            self.output.write(self.buffer + ' boolean ' + str(self.lines) + '\n')

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
            
            elif char in self.delimiters:
                self.buffer += char
                self.current_state = self.q6
            
            elif char == '=' or char == '<' or char == '>':
                self.buffer += char
                self.current_state = self.q7

            elif char == '+' or char == '-':
                self.buffer += char
                self.current_state = self.q8
            
            elif char == '*' or char == '/':
                self.buffer += char
                self.current_state = self.q9

            elif not char:
                break

            else:
                self.buffer += char
                self.stopped = True
                self.does_match()
                break
    
    @prime
    def _create_q2(self):
        # check if the input is a comment
        while True:
            char = yield
            if char == '}':
                self.current_state = self.q1
            elif char == None:
                self.stopped = True
                self.does_match()
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
            
            elif self.buffer == 'or':
                self.current_state = self.q8
                self.send(char)
            
            elif self.buffer == 'and':
                self.current_state = self.q9
                self.send(char)
            
            elif self.buffer == 'true' or self.buffer == 'false':
                self.current_state = self.q10
                self.send(char)
            
            else:
                self.does_match()
                self.current_state = self.q1
                self.send(char)
    
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
                self.send(char)

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
                self.send(char)
    
    @prime
    def _create_q6(self):
        # check if the input is a delimiter or a assignment command
        while True:
            char = yield
            if char == '=' and self.buffer == ':':
                self.buffer += char
                self.current_state = self.q6
            else:
                self.does_match()
                self.current_state = self.q1
                self.send(char)
    
    @prime
    def _create_q7(self):
        # check if the input is a relational operator
        while True:
            char = yield
            if char == '=' or char == '<' or char == '>':
                if char != self.buffer and char != '<':
                    self.buffer += char
                    self.does_match()
                    self.current_state = self.q1
                else:
                    self.buffer += char
                    self.stopped = True
                    self.does_match()
            else:
                self.does_match()
                self.current_state = self.q1
                self.send(char)
    
    @prime
    def _create_q8(self):
        # Check if the input is an additive operator
        while True:
            char = yield
            self.does_match()
            self.current_state = self.q1
            self.send(char)
    
    @prime
    def _create_q9(self):
        # Check if the input is a multiplicative operator
        while True:
            char = yield
            self.does_match()
            self.current_state = self.q1
            self.send(char)
    
    @prime
    def _create_10(self):
        # Check if the input is a boolean
        while True:
            char = yield
            self.does_match()
            self.current_state = self.q1
            self.send(char)

analyser = LexicalAnalyser('input/program.txt')
analyser.analyse()
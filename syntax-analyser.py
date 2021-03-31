class SyntaxAnalyser:
    def __init__(self, input):
        self.reader = open(input, 'r')
        self.index = 0
        self.buffer = None

    def next(self):
        self.buffer = self.reader.readline().replace('\n', '').split()
        if not self.buffer:
            self.reader.close()
            return
    
    def analyse(self):
        self.next()
        self.program()

    def error(self, received, expected):
        print('Error: received ' + received + ', ' + expected)
    
    def program(self):
        if self.buffer[0] == 'program':
            print('leu: ' + self.buffer[0])
        #     self.next()

        #     if self.buffer[1] == 'identifier':
        #         self.next()
            
        #         if self.buffer[0] == ';':
        #             self.next()
        #             self.var_declarations()
        #             self.subprograms_declarations()
        #             self.compound_cmd()
            
        #             if self.buffer[0] == '.':
        #                 return
        #             else:    
        #                 self.error(self.buffer[0], '.')
        #         else:
        #             self.error(self.buffer[0], ';')
        #     else:
        #         self.error(self.buffer[1], 'identifier')
        # else:
        #     self.error(self.buffer[0], 'program declaration')
    
    def var_declarations(self):
        if self.buffer[0] == 'var':
            self.next()
            self.list_var_dec1()
        else:
            self.error(self.buffer[0], 'var, procedure, compound command declaration')


    def subprograms_declarations(self):
        pass

    def compound_cmd(self):
        pass
    
    def list_var_dec1(self):
        self.list_identifiers()
        if self.buffer[0] == ':':
            self.next()
            self.type()
            if self.buffer[0] == ';':
                return self.next()
            else:
                self.error(self.buffer[0], ';')
        
    def list_identifiers(self):
        if self.buffer[1] == 'identifier':
            self.next()
            if self.buffer[0] == ',':
                self.next()
                self.list_identifiers()
            else:
                return self.next()
        else:
            self.error(self.buffer[1], 'identifier')
            
    def type(self):
        if self.buffer[0] in ['integer', 'real', 'boolean']:
            return self.next()
        else:
            self.error(self.buffer[0], 'integer, real or boolean')
    
sa = SyntaxAnalyser('output.txt')
sa.analyse()
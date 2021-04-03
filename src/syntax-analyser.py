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
            self.next()

            if self.buffer[1] == 'identifier':
                self.next()
            
                if self.buffer[0] == ';':
                    self.next()
                    self.var_declarations()
                    self.subprograms_declarations()
                    # self.compound_cmd()
            
                    if self.buffer[0] == '.':
                        return
                    else:    
                        self.error(self.buffer[0], '.')
                else:
                    self.error(self.buffer[0], ';')
            else:
                self.error(self.buffer[1], 'identifier')
        else:
            self.error(self.buffer[0], 'program declaration')
    
    def var_declarations(self):
        if self.buffer[0] == 'var':
            self.next()
            self.list_var_dec1()
        else:
            self.error(self.buffer[0], 'var, procedure, compound command declaration')
    
    def list_var_dec1(self):
        self.list_identifiers1()
        if self.buffer[0] == ':':
            self.next()
            self.type()
            if self.buffer[0] == ';':
                self.next()
            else:
                self.error(self.buffer[0], ';')
        else:
            self.error(self.buffer[0],':')
            
        self.list_var_dec2()

    def list_var_dec2(self):
        self.list_identifiers1()
        if self.buffer[0] == ':':
            self.next()
            self.type()
            if self.buffer[0] == ';':
                self.next()
            else:
                self.error(self.buffer[0], ';')
        else:
            self.error(self.buffer[0],':')
        if self.buffer[1] == 'identifier':
            self.list_var_dec2()
        else:
            return
        
    def list_identifiers1(self):
        if self.buffer[1] == 'identifier':
            self.next()
            return
        else:
            self.error(self.buffer[1], 'identifier1')
        self.list_identifiers2()
    
    def list_identifiers2(self):
        if self.buffer[0] != '':
            if self.buffer[0] == ',':
                self.next()
                if self.buffer[1] == 'identifier':
                    self.next()
                else:
                    self.error(self.buffer[0], 'identifier')
            else:
                return self.next()
        self.list_identifiers2()

            
    def type(self):
        if self.buffer[0] in ['integer', 'real', 'boolean']:
            return self.next()
        else:
            self.error(self.buffer[0], 'integer, real or boolean')
    
    def subprograms_declarations(self):
        if self.buffer[0] == 'procedure':
            self.subprog_declaration()
        else:
            return


    def subprog_declaration(self):
        if self.buffer[0] == 'procedure':
            self.next()
            if self.buffer[1] == 'identifier':
                self.next()
                self.arguments()
                if self.buffer[0] == ';':
                    self.next()
                    self.var_declarations()
                    self.subprograms_declarations()
                    # self.compound_cmd()
                else:
                    self.error(self.buffer,';')
            else:
                self.error(self.buffer[1], 'identifier')
        else:
            return
                
    def arguments(self):
        if self.buffer[0] == '(':
            self.next()
            self.list_param()
            if self.buffer[0] == ')':
                self.next()
            else:
                self.error(self.buffer[0], ')')
        else:
            return

    def list_param(self):
        self.list_identifiers1()
        if self.buffer[0] == ':':
            self.next()
            self.type


    
sa = SyntaxAnalyser('output/output.txt')
sa.analyse()
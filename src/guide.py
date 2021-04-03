class SyntacticAnalyser:
    def __init__(self):
        #le proximo
        #program()

    # def program(self):
    #     if x.token == "program"
    #         #le proximo
    #         if x.class == "identifier"
    #             #le proximo
    #             if x.token == ";"
    #                 #le proximo
    #                 # var_dec()
    #                 # subprog_dec()
    #                 # compost_com()
    #                 if x.token != "."
    #                     error("Was expecting the token '.' instead of " x.token)
    #             else error("Was expecting the token ';' instead of " x.token)
    #         else error("Was expecting a identifier instead of a" x.class)
    #     else error("Was expecting the token 'program' instead of " x.token)

    # def var_dec():
    #     if x.token == "var"
    #         #le proximo
    #         var_dec_list()
    #     elif x.token == ''
    #         #le proximo
    #     else error("Variable declaration contains errors")

    # def var_dec_list1():
    #     id_list()
    #     if x.token == ":"
    #         #le proximo
    #         _type()
    #         if x.token == ";"
    #         #le proximo
    #         else error("Missing ';'")
    #     else error("':' expected")
    #     ver_dec_list2

    # def var_dec_list2():
    #     if x.token != ''
    #         var_dec_list1()

    # def id_list1():
    #     if x.class == "identifier"
    #         #le proximo
    #         id_list2()
    #     else error("expecting a identifier")
    
    # def id_list2():
    #     if x.token != ''
    #         if x.token == ","
    #         #le proximo
    #         if x.class == "identifier"
    #         #le proximo
    #         id_list2()

    # def _type():
    #     if x.token == "integer" or x.token == "real" or x.token == "boolean"
    #         #le proximo
    #     else error("unidentified type")

    # def subprogs_dec():
    #     if x.token != ''
    #         subprog_dec()
    
    # def subprog_dec():
    #     if x.token == "procedure"
    #         #le proximo
    #         if x.class == "identifier"
    #             #le proximo
    #             arg()
    #             if x.token == ";"
    #                 #le proximo
    #                 var_dec()
    #                 subprog_dec()
    #                 compost_com()
    #             else error("expected ';'")
    #         else error("expexted identifier")
    #     else error("expected 'procedure'")

    # def arg():
    #     if x.token != ''
    #         if x.token == '('
    #             #le proximo
    #             param_list()
    #             if x.token == ")"
    #                 #le proximo
    #             else error("missing ')'")
    #         else error("expecting '('")

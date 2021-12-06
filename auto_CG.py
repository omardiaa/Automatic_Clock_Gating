import pyverilog.vparser.ast as vast
from pyverilog.vparser.parser import parse
from pyverilog.ast_code_generator.codegen import ASTCodeGenerator
import sys

def parseFile(fileName): 
    return parse(fileName) 

def createCG(): 
    clkgateArgs = [
    vast.PortArg("GCLK", vast.Identifier("_clockgate_output_gclk")),
    vast.PortArg("GATE", vast.Identifier("EN")),
    vast.PortArg("CLK", vast.Identifier("CLK"))
    ]

    cG = vast.Instance("sky130_fd_sc_hd_dlclkp","clockgate_cell_", tuple(clkgateArgs), tuple())

   

    return cG


def main(): 

    cG = createCG() 
    print(cG.name); 
    print(cG.module);
    cGOutput = vast.Wire('_clockgate_output_gclk')
    ast,_= parseFile([sys.argv[1]]) #root node of the abstract syntax tree  
    description = ast.description  #moduleDef node 
    definition = description.definitions[0]

    newrtl =[] 
    newrtl.append(cG)

    # definition.items = tuple(newrtl)
    # codegen = ASTCodeGenerator()
    # rslt = codegen.visit(ast)
    # f = open("testUpdated.v", "w+")
    # f.write(rslt)
    # f.close()

    
    for itemDeclaration in definition.items:
        item_type = type(itemDeclaration)._name_
        if item_type == "InstanceList":
            instance = itemDeclaration.instances[0]
            inputD = ""
            outputQ = ""
            clk = ""
            if(instance.module == "sky130_fd_sc_hd__dfxtp_1"):
                
                for getPort in instance.portlist:
                    if(getPort.portname == "D"):
                        inputD = getPort.argname
                    elif(getPort.portname == "Q"):
                        outputQ = getPort.argname
                    elif(getPort.portname == "CLK"):
                        clk = getPort.argname
                # print("Q: {} D:{}".format(inputD, outputQ))
                muxIn=""
                en=""
                for itemDeclaration2 in definition.items:
                    item_type2 = type(itemDeclaration2)._name_
                    if item_type2 == "InstanceList":
                        instance2 = itemDeclaration2.instances[0]
                        if(instance2.module == "sky130_fd_sc_hd_mux2_1" or instance2.module ==  "sky130_fd_sc_hda21oi_1" or instance2.module == "sky130_fd_sc_hd_a21oi_2"):
                            for portout in instance2.portlist:
                                if(portout.argname == inputD):
                                    for getPort in instance2.portlist:
                                        if(getPort.portname=="S"):
                                            en=getPort.argname
                                        elif(getPort.portname =="A0" and getPort.argname != outputQ):
                                            muxIn = getPort.argname
                                        elif(getPort.portname =="A1" and getPort.argname != outputQ):
                                            muxIn = getPort.argname
                                    
                                    print("Module: {} - {} Mux Input: {} Enabler: {} clk: {} input D: {}".format(instance.module, instance.name,muxIn, en, clk, inputD))
            # if(instance.module == "sky130_fd_sc_hd_mux2_1" or instance.module ==  "sky130_fd_sc_hda21oi_1" or instance.module == "sky130_fd_sc_hd_a21oi_2"):
            #     print(instance.module)
            #     for getPort in instance.portlist: 
            #         print("Port name: ") 
            #         print(getPort.portname)
            #         print("Arg name: ") 
            #         print(getPort.argname)






    
           
main()
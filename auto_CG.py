import pyverilog.vparser.ast as vast
from pyverilog.vparser.parser import parse
from pyverilog.ast_code_generator.codegen import ASTCodeGenerator
import sys

def parseFile(fileName): 
    
    return parse(fileName) 

def createCG(): 
    clkgateArgs = [
    vast.PortArg("GCLK", vast.Identifier("__clockgate_output_gclk_")),
    vast.PortArg("GATE", vast.Identifier("EN")),
    vast.PortArg("CLK", vast.Identifier("CLK"))
    ]

    cG = vast.Instance("sky130_fd_sc_hd__dlclkp","__clockgate_cell__", tuple(clkgateArgs), tuple())
    return cG


def main(): 

    cG = createCG() 
    cGOutput = vast.Wire('__clockgate_output_gclk_')
    ast,_= parseFile([sys.argv[1]]) #root node of the abstract syntax tree  
    description = ast.description  #moduleDef node 
    definition = description.definitions[0]
    
    for itemDeclaration in definition.items:
        item_type = type(itemDeclaration).__name__
        if item_type == "InstanceList":
            instance = itemDeclaration.instances[0]
            if(instance.module == "sky130_fd_sc_hd__mux2_1" or instance.module ==  "sky130_fd_sc_hd__a21oi_1" or instance.module == "sky130_fd_sc_hd__a21oi_2"):
                print(instance.module)
                for getPort in instance.portlist: 
                    print("Port name: ") 
                    print(getPort.portname)
                    print("Arg name: ") 
                    print(getPort.argname)
    
           
main()

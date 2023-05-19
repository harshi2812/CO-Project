# CO-Project
Co-project to convert ISA assembly language to Opcode(binary code)-IIITD
 Done by:
 Kartik Prasad-2022240
 Harshil Handoo-2022206
 Harshit Sagar-2022210
 MAHANAMA SIRIWARDHANA-2022271
 It reads an input file called "input.txt" which contains assembly instructions and generates the corresponding machine code in an output file called "out.txt".
Here is a breakdown of the code:
The opcodes dictionary stores the opcode mappings for different assembly instructions.
The register dictionary stores the binary representations for different registers.
The dectobinary function converts decimal numbers to 7-bit binary strings.
The input file is read and processed to remove empty lines and newline characters.
The program extracts the assembly instructions and their operands into the l3proper list.
The program generates binary addresses for the instructions and stores them in the lbinaryaddress list.
Various helper functions are defined to convert different types of instructions into machine code.
The program assigns binary addresses to variables encountered in the code.
The program assigns binary addresses to labels encountered in the code.
The convmachinecode function converts each instruction into machine code and writes it to the output file.
Error checking functions are defined to validate the instructions and operands.
The program checks for errors such as overflow, invalid registers, incorrect number of operands, missing labels, missing variables, and invalid immediate values.
The program writes error messages to the output file if any errors are found.
The program checks for specific restrictions such as manipulating the flag register and the position of the halt instruction.
Finally, the program processes each instruction, converts it into machine code, and writes it to the output file.
The output file "out.txt" contains the generated machine code.

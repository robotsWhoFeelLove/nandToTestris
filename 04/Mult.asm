// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/4/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)
// The algorithm is based on repetitive addition.


//Multiply in asm machine language
// Multiply ro and r1 and store in r2
// for (i=1; i< r2; i++)
// r0 + r0
@0
D=A
@R2
M=D
@R0 
D=M 
@x
M=D
@R1 
D=M 
@y
M=D
@0
D=A 
@i 
M=D
@sum
M=D
(Loop)
@i 
D=M 
@y 
D=D-M 
@OUT
D;JEQ
@x
D=M 
@sum 
M=D+M
@i 
M=M+1
@Loop
0;JMP
(OUT)
@sum
D=M
@R2 
M=D
(END)
@END
0;JMP
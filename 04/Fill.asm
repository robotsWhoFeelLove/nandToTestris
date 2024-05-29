// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/4/Fill.asm

// Runs an infinite loop that listens to the keyboard input. 
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel. When no key is pressed, 
// the screen should be cleared.

//// Replace this comment with your code.

//CONSTANTS
// set n to 8192 (32 cols * 256 rows)
@8192
D=A
@n
M=D


(LISTEN)
// set i to 0
@0
D=A
@i
M=D
@KBD
D=M
@fill
M=D

// Main Loop
(MAINLOOP)
// if i = n go to OuterListen
@i
D=M
@n
D=D-M
@LISTEN
D;JEQ
// else 
// if fill = 0
// jump to clear
@fill
D=M
@CLEAR
D;JEQ
// else write -1 to Address
// // go to SCREEN Address + i
@SCREEN
D=A
@i
D=D+M
A=D
M=-1
// i++

@i
M=M+1
// Jump to Main Loop
@MAINLOOP
0;JMP
// Clear
(CLEAR)
// write 0 to Address
@SCREEN
D=A
@i
D=D+M
A=D
M=0
// i++
@i
M=M+1
// Jump to Main Loop
@MAINLOOP
0;JMP
.data 
promptA: .asciiz "Enter an int A: "
promptB: .asciiz "Enter an int B: "
promptC: .asciiz "Enter an int C: "
resultAdd: .asciiz "A + B + C = "
newline: .asciiz "\n"

.globl main
.text

main: 
	# Prints string to ask for integer A
	li $v0, 4		      
	la $a0, promptA
	syscall    
	# Reads input for int A
	li $v0, 5
	syscall 
	# Puts entered value into t0
	move $t0, $v0
	# Prints string to ask for integer B
	li $v0, 4
	la $a0, promptB
	syscall
	
    
    	# Reads input for int B
	li $v0, 5
	syscall 
	# Moves value read for B into t1
	move $t1, $v0
	
	# Prints string to ask for integer C
	li $v0, 4		      
	la $a0, promptC
	syscall    
	# Reads input for int A
	li $v0, 5
	syscall 
	# Puts entered value into t0
	move $t2, $v0

	
	add $t3, $t2, $t1
	add $t4, $t0, $t3


	# Prints out A + B
	li $v0, 4
	la $a0, resultAdd
	syscall
    	
    	# Prints integer value in t2 which is A+B
	li $v0, 1
	move $a0, $t4	
	syscall 

	li $v0, 4
	la $a0, newline
	syscall 

	li $v0, 10
	syscall

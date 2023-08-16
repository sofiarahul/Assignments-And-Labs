.data 
# TODO: What are the following 5 lines doing?
promptA: .asciiz "Enter an int A: "
promptB: .asciiz "Enter an int B: "
resultAdd: .asciiz "A + 42 = "
resultSub: .asciiz "B - A = "
newline: .asciiz "\n"

.globl main
.text

main: 
	#Prompt for A
	li $v0, 4		      
	la $a0, promptA
	syscall    
	
	# Read A put into t0
	li $v0, 5
	syscall 
	move $t0, $v0

	#Prompt for B
	li $v0, 4
	la $a0, promptB
	syscall

 	#Read B put into t1
	li $v0, 5
	syscall 
	move $t1, $v0

	# Add and sub
	addi $t2, $t0, 42 
	sub $t3, $t1, $t0

	# Print results for add
	li $v0, 4
	la $a0, resultAdd
	syscall

	li $v0, 1
	move $a0, $t2	
	syscall 
	
	li $v0, 4
	la $a0, newline
	syscall 

	# Print results for sub
	li $v0, 4
	la $a0, resultSub
	syscall

	move $a0, $t3	
	li $v0, 1
	syscall 

	li $v0, 4
	la $a0, newline
	syscall 

	li $v0, 10
	syscall

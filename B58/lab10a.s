.data
array1: .word 5,8,3,4,7,2
newline: .asciiz "\n"

.globl main
.text

main:
	la $a1 array1 #Load array into a1
	li $t0 1 #counter
	li $s0 6 #length of array
	lw $t1, 0($a1) #Load first value into t1
	addi $a1, $a1, 4 # move to next value in array
	lw $t2, 0($a1) # store 2nd val in t2
	mul $t3, $t1, $t2 #muktiply and store in t3
	addi $t0, $t0, 2
	
	WHILE:
		bgt $t0,$s0, DONE
		addi $a1, $a1, 4
		lw $t2, 0($a1)
		mul $t3, $t3, $t2
		addi $t0, $t0, 1 #Increment counter
		j WHILE
	DONE:
	
	li $v0, 1
	move $a0, $t3	
	syscall 
	
	li $v0, 4
	la $a0, newline
	syscall

	li $v0, 10
	syscall
		

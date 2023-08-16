.data
newline: .asciiz "\n"
promptN: .asciiz "Enter a number: "

.text
main:
	li $v0, 4		# system call code for print_string
	la $a0, promptN  	# address of string N to print
	syscall			# print the string

	li $v0, 5		# system call code for read_int
	syscall 		# Read the int
	move $a0, $v0		# Load N into $t0
	
	jal mystery
	
mystery:
	addi $sp, $sp, -8 # room for $ra and one temporary
	sw $ra, 4($sp) # save $ra
	move $v0, $a0 # pre-load return value as n
	beq $a0, 0, recurse # if(n == 2) return 0
	sw $a0, 0($sp) # save a copy of n
	addi $a0, $a0, -1 # n - 1
	jal mystery # mystery(n - 1)
	lw $a0, 0($sp) # retrieve n
	sw $v0, 0($sp) # save result of mystery(n - 1)
	lw $v1, 0($sp) # retrieve mystery(n - 1)
	mul $t3, $v1, 2 #Compute 2n
	add $v0, $v1, $t3 # mystery(n-1) + 2n
	sub $v0, $v0, 1 # result + 1

recurse:
	lw $ra, 4($sp) #resture $ra
	addi $sp, $sp, 8 #restore $sp
	jr $ra
	
	
	

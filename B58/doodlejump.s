#####################################################################
#
# CSCB58 Fall 2020 Assembly Final Project
# University of Toronto, Scarborough
#
# Student: Sofia, 1004900342
#
# Bitmap Display Configuration:
# - Unit width in pixels: 8					     
# - Unit height in pixels: 8
# - Display width in pixels: 256
# - Display height in pixels: 256
# - Base Address for Display: 0x10008000 ($gp)
#
# Which milestone is reached in this submission?
# (See the assignment handout for descriptions of the milestones)
# - Milestone 2 and some of 3
#
# Which approved additional features have been implemented?
# (See the assignment handout for the list of additional features)
# 1. 
# 2. 
# 3. 
# 
#
# Link to video demonstration for final submission:
# - (insert YouTube / MyMedia / other URL here). 
#
# Any additional information that the TA needs to know:
# - 
#
#####################################################################

.data
	displayAddress:	.word	0x10008000
	doodleColour: .word  0xDF371D
	skyColour: .word  0xD1EEFC
	platform_length: .word 20
	#stepsColour .word  0x8D580C
.text
	#Random pixel generator
	li $v0, 42
	li $a0, 0
	li $a1, 4096
	syscall
	
	move $t5, $a0	# Starting pixel for platform 1
	and $s5, $t5, 3
	if:
		beq $s5, 0, else
		addi $t5, $t5, 1
		and $s5, $t5, 3
		j if
	else:
	li $v0, 42
	li $a0, 0
	li $a1, 4096
	syscall
	
	move $t7, $a0 # Starting pixel for platform 2
	and $s5, $t7, 3
	if2:
		beq $s5, 0, else2
		addi $t7, $t7, 1
		and $s5, $t7, 3
		j if2
	else2:
	li $v0, 42
	li $a0, 0
	li $a1, 4096
	syscall
	
	move $s1, $a0 # Starting pixel for platform 3
	and $s5, $s1, 3
	if3:
		beq $s5, 0, else3
		addi, $s1, $s1, 1
		and $s5, $s1, 3
		j if3
	else3:

	lw $t0, displayAddress	# $t0 stores the base address for display
	li $t1, 0xD1EEFC	# $t1 stores the SKY colour code
	li $t2, 0xDF371D	# $t2 stores the DOODLER colour code
	li $t3, 0x8D580C	# $t3 stores the PLATFORM colour code
	li $t4, 0 		# Keeps track of current pixel
	lw $t6, platform_length# platform1 ending
	lw $s0, platform_length# platform2 ending
	lw $s2, platform_length# platform3 ending
	li $s3, 4032 #doodler start pos
	
	add $t6, $t5, $t6 	# Platform1 ending
	add $s0, $t7, $s0	# Platform2 ending 
	add $s2, $s1, $s2	# Platform3 ending
	
	ScreenPaint:
		beq $t4, $t5, platform # If current pixel is start of platform1 draw platform
		beq $t4, $t7, platform # painting platform 2
		beq $t4, $s1, platform # painting platform 3
		beq $t4, $s3, doodler # doodler initial position
		bge $t4, 4096, KeyboardLoop
		#bgt $s3, 4096, Exit 
		#bge $t4, 4096, keyboardLoop	# If current pixel is final pixel stop drawing
		sw $t1, 0($t0) 		# paint sky colour 
		addi $t0, $t0, 4	# Go to next address
		addi $t4, $t4, 4	# Go to next pixel
		j ScreenPaint
		#sw $t3, 128($t0) # paint the first unit on the second row blue. Why +128?
		
	platform: # Paint platform
		beq $t4, $t6, ScreenPaint
		beq $t4, $s0, ScreenPaint
		beq $t4, $s2, ScreenPaint
		sw $t3, 0($t0)
		addi $t0, $t0, 4
		addi $t4, $t4, 4
		j platform
		
	doodler: #Paint doodler (1 pixel right now)
		sw $t2, 0($t0)
		addi $t0, $t0, 4
		addi $t4, $t4, 4
		j ScreenPaint
		
	KeyboardLoop:
		lw $s4, 0xffff0000
		beq $s4, 1, keyboardInput #s4 will be 1 if a key is pressed
		#doodle pos is 128 greater than any platform then j keyboard loop
		#addi $s7, $t5, 128
		#beq $s3, $s7, KeyboardLoop
		#addi $s7, $t7, 128
		#beq $s3, $s7, KeyboardLoop
		#addi $s7, $s1, 128
		#beq $s3, $s7, KeyboardLoop
		bne $s4, 1, doodleFall
	
	keyboardInput:
		lw $s6, 0xffff0004
		beq $s6, 0x61, respond_to_A #if the key stroke was a
		beq $s6, 0x64, respond_to_D #if the key stroke was d
		beq $s6, 0x77, respond_to_W #if key stroke was w
		
	respond_to_A:
		#update doodler position and redraw screen
		subi $s3, $s3, 4
		li $t4, 0
		lw $t0, displayAddress
		j ScreenPaint
	
	respond_to_D:
		#move doodler left 1 pixel
		addi $s3, $s3, 4
		li $t4, 0
		lw $t0, displayAddress
		j ScreenPaint
		
	respond_to_W:
		subi $s3, $s3, 128
		
		addi $t5, $t5, 128
		addi $t7, $t7, 128
		addi $s1, $s1, 128
		
		addi $t6, $t6, 128
		addi $s0, $s0, 128
		addi $s2, $s2, 128
		
		li $t4, 0
		lw $t0, displayAddress
		j ScreenPaint
		
	doodleFall:
		addi $s3, $s3, 128
		li $t4, 0
		lw $t0, displayAddress
		
		li $v0, 32
		li $a0, 2000
		syscall
		
		j ScreenPaint
Exit:
	#Paint the you lost on screen
	
	li $v0, 10 # terminate the program
	syscall

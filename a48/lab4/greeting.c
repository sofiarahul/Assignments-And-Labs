#include <stdio.h>
#include <stdlib.h>
#include <string.h>


/*
    This program has two arguments: the first is a greeting message, and the
    second is a name.

    The message is an impersonal greeting, such as "Hi" or "Good morning".
    name is set to refer to a string holding a friend's name, such as
    "Emmanuel" or "Xiao".

    First copy the first argument to the array greeting. (Make sure it is
    properly null-terminated.)

    Write code to personalize the greeting string by appending a space and
    then the string pointed to by name.
    So, in the first example, greeting should be set to "Hi Emmanuel", and
    in the second it should be "Good morning Xiao".

    If there is not enough space in greeting, the resulting greeting should be
    truncated, but still needs to hold a proper string with a null terminator.
    For example, "Good morning" and "Emmanuel" should result in greeting
    having the value "Good morning Emmanu" and "Top of the morning to you" and
    "Patrick" should result in greeting having the value "Top of the morning ".

    Do not make changes to the code we have provided other than to add your 
    code where indicated.
*/

int length(char *s)
{
	int counter = 0;
	char *p = s;
	
	while(*(p+counter) != '\0')
	{
		counter++;
	}
	
	return counter;
}

int main(int argc, char **argv) {
    if (argc != 3) {
        fprintf(stderr, "Usage: greeting message name\n");
        exit(1);
    }
    char greeting[20];
    char *name = argv[2];

    // Your code goes here
	char *first_part = argv[1];
	int len = length(first_part);
	//int name_len = length(name);
	char space[2] = " ";
	
	strncat(greeting, first_part, 20);
	strncat(greeting, space, 20-len);
	strncat(greeting, name, 20-len-1);


    printf("%s\n", greeting);
    return 0;
}



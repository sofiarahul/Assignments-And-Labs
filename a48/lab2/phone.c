#include <stdio.h>
#include <stdlib.h>

int main(int argc, char **argv) {

	char input_string[11];
	int input_int; 
	
	scanf("%s %d", input_string, &input_int);
	//scanf("%d", input_int);
	
	if(input_int == -1)
	{
		printf("%s\n",input_string);
	}
	else if(input_int<-1 || input_int > 9)
	{
		printf("ERROR\n");
		return 1;
	}
	else{
		printf("%c",input_string[input_int]);
	}
    return 0;
}

#include <stdio.h>
#include <stdlib.h>

int main(int argc, char **argv) {

	char input_string[11];
	int input_int; 
	int status = 0;
	
	scanf("%s", input_string);
	
	while(scanf( "%d", &input_int)){
		if(input_int == -1)
		{
			printf("%s\n",input_string);
		}
		else if(input_int<-1 || input_int > 9)
		{
			printf("ERROR\n");
			status = 1;
		}
		else
		{
			printf("%c\n",input_string[input_int]);
		}
	}
	
    return status;
}

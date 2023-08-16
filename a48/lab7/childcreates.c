#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <sys/wait.h>

int child_creates(int n, int iterations)
{
	if(n == 0)
	{
		return 0;
	}
	
	int pid = fork();
	
	if(pid<0)
	{
		perror("fork");
		exit(1);
	}
	
	if(pid == 0)
	{
		printf("ppid = %d, pid = %d, i = %d\n", getppid(), getpid(), iterations-n);
		n = n-1;
		child_creates(n, iterations);
		exit(0);
	}
	
	else{
		wait(NULL);
	}
	return 0;
}

int main(int argc, char **argv) {
    //int i;
    int iterations;

    if (argc != 2) {
        fprintf(stderr, "Usage: forkloop <iterations>\n");
        exit(1);
    }

    iterations = strtol(argv[1], NULL, 10);
	
	printf("ppid = %d, pid = %d, i = %d\n", getppid(), getpid(), 0);
	child_creates(iterations, iterations);


    return 0;
}

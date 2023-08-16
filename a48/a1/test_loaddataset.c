#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include "knn.h"

/* This small test file will help you determine if you have successfully
 * completed the load_image function in knn.
 * 
 * compile this program as "gcc -Wall -g -std=gnu99 -lm -o test_loadimage test_loadimage.c knn.c"
 * This program prints the image to standard output, so you should redirect it
 * to a file and compare it with the original image.
 */
unsigned char training_dataset[MAX_SIZE][NUM_PIXELS];
unsigned char training_labels[MAX_SIZE];

int main(int argc, char **argv) {
    if (argc != 2) {
        fprintf(stderr, "Usage: %s imagefile\n", argv[0]);
        exit(1);
    }

    load_dataset(argv[1], training_dataset, training_labels);

	//printf("%u",training_dataset[1][10]);
	//printf("%u",training_dataset[0][0]);
	//printf("%u",training_dataset[0][392]);
	//printf("%u",training_dataset[2][300]);
	
    //print_image(image);
    return 0;
}

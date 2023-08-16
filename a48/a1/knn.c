#include <stdio.h>
#include <math.h>    // Need this for sqrt()
#include <stdlib.h>
#include <string.h>

#include "knn.h"

/* Print the image to standard output in the pgmformat.  
 * (Use diff -w to compare the printed output to the original image)
 */
void print_image(unsigned char *image) {
    printf("P2\n %d %d\n 255\n", WIDTH, HEIGHT);
    for (int i = 0; i < NUM_PIXELS; i++) {
        printf("%d ", image[i]);
        if ((i + 1) % WIDTH == 0) {
            printf("\n");
        }
    }
}

/* Return the label from an image filename.
 * The image filenames all have the same format:
 *    <image number>-<label>.pgm
 * The label in the file name is the digit that the image represents
 */
unsigned char get_label(char *filename) {
    // Find the dash in the filename
    char *dash_char = strstr(filename, "-");
    // Convert the number after the dash into a integer
    return (char) atoi(dash_char + 1);
}

/* ******************************************************************
 * Complete the remaining functions below
 * ******************************************************************/


/* Read a pgm image from filename, storing its pixels
 * in the array img.
 * It is recommended to use fscanf to read the values from the file. First, 
 * consume the header information.  You should declare two temporary variables
 * to hold the width and height fields. This allows you to use the format string
 * "P2 %d %d 255 "
 * 
 * To read in each pixel value, use the format string "%hhu " which will store
 * the number it reads in an an unsigned character.
 * (Note that the img array is a 1D array of length WIDTH*HEIGHT.)
 */
void load_image(char *filename, unsigned char *img) {
    // Open corresponding image file, read in header (which we will discard)
    FILE *f2 = fopen(filename, "r");
    if (f2 == NULL) {
        perror("fopen");
        exit(1);
    }
	
	int i = 0;
	int height;
	int width;
	unsigned char temp;
	
	fscanf(f2, "P2 %d %d 255", &height, &width);
	//printf("height: %d, width: %d\n", height, width);
	
	while(fscanf(f2, "%hhu", &temp) == 1)
	{
		//printf("%u", (unsigned)temp);
		*(img+i) = temp;
		i++;
	}
	//TODO

    fclose(f2);
}


/**
 * Load a full dataset into a 2D array called dataset.
 *
 * The image files to load are given in filename where
 * each image file name is on a separate line.
 * 
 * For each image i:
 *  - read the pixels into row i (using load_image)
 *  - set the image label in labels[i] (using get_label)
 * 
 * Return number of images read.
 */
int load_dataset(char *filename, 
                 unsigned char dataset[MAX_SIZE][NUM_PIXELS],
                 unsigned char *labels) {
    // We expect the file to hold up to MAX_SIZE number of file names
    FILE *f1 = fopen(filename, "r");
    if (f1 == NULL) {
        perror("fopen");
        exit(1);
    }
	
	char single_file[2048];
	int i = 0;
	
	while(fscanf(f1, "%s", single_file) == 1)
	{
		load_image(single_file, dataset[i]);
		*(labels+i) = get_label(single_file);
		i++;
	}

    //TODO

    fclose(f1);
    return i;
}

/** 
 * Return the euclidean distance between the image pixels in the image
 * a and b.  (See handout for the euclidean distance function)
 */
double distance(unsigned char *a, unsigned char *b) {

	double sum = 0.0;
	double temp;
	for(int i = 0; i<NUM_PIXELS ; i++)
	{
		temp = (*(b+i) - *(a+i))*(*(b+i) - *(a+i)); //(b-a)(b-a)
		sum = sum + temp;
	}
    return sqrt(sum);
}

/**
 * Return the most frequent label of the K most similar images to "input"
 * in the dataset
 * Parameters:
 *  - input - an array of NUM_PIXELS unsigned chars containing the image to test
 *  - K - an int that determines how many training images are in the 
 *        K-most-similar set
 *  - dataset - a 2D array containing the set of training images.
 *  - labels - the array of labels that correspond to the training dataset
 *  - training_size - the number of images that are actually stored in dataset
 * 
 * Steps
 *   (1) Find the K images in dataset that have the smallest distance to input
 *         When evaluating an image to decide whether it belongs in the set of 
 *         K closest images, it will only replace an image in the set if its
 *         distance to the test image is strictly less than all of the images in 
 *         the current K closest images.
 *   (2) Count the frequencies of the labels in the K images
 *   (3) Return the most frequent label of these K images
 *         In the case of a tie, return the smallest value digit.
 */ 
 
int max(int *array, int size)
{
	int maximum;
	
	for(int i = 0; i<size; i++)
	{
		if(*(array+i) > maximum)
		{
			maximum = *(array+i);
		}
	}
	
	return maximum;

}

int less_than(double item, int *k_closest, double *distances, int size)
{
	int flag = 0;
	int index;
	
	for(int i = 0; i<size; i++)
	{
		index = *(k_closest+i);
		if(item<*(distances+index))
			flag = 1;
	}
	
	return flag;
}

int find_index(int item, double *distances, int size)
{
	for(int i = 0; i<size; i++)
	{
		if(item == *(distances+i))
			return i;
	}
	return -1;
}

int knn_predict(unsigned char *input, int K,
                unsigned char dataset[MAX_SIZE][NUM_PIXELS],
                unsigned char *labels,
                int training_size) {

	double distances[training_size];
	int k_closest[K];
	int label_frequencies[10];
	
	for(int i = 0; i<training_size; i++)
	{
		distances[i] = distance(input, dataset[i]); //should input go first or last here
	}
	
	for(int f = 0; f<K; f++) //set first K items as closest
	{
		k_closest[f] = f;
	}
	
	for(int j = K+1; j<training_size; j++)
	{
		if(less_than(distances[j], k_closest, distances, K) == 1) //less than all k closest neighbors
		{
			k_closest[find_index(max(k_closest, K), distances, K)] = j;
			//replace largest item in k_closest with j
		}
	}
	
	for(int k = 0; k<K; k++)
	{
		label_frequencies[*(labels+k)]++;
	}
	
    return max(label_frequencies, 10);
}

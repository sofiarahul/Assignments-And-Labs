/*
 * This code is provided solely for the personal and private use of students
 * taking the CSC209H course at the University of Toronto. Copying for purposes
 * other than this use is expressly prohibited. All forms of distribution of
 * this code, including but not limited to public repositories on GitHub,
 * GitLab, Bitbucket, or any other online platform, whether as given or with
 * any changes, are expressly prohibited.
 *
 * Authors: Mustafa Quraish, Bianca Schroeder, Karen Reid
 *
 * All of the files in this directory and all subdirectories are:
 * Copyright (c) 2021 Karen Reid
 */

#include "dectree.h"

/**
 * Load the binary file, filename into a Dataset and return a pointer to 
 * the Dataset. The binary file format is as follows:
 *
 *     -   4 bytes : `N`: Number of images / labels in the file
 *     -   1 byte  : Image 1 label
 *     - NUM_PIXELS bytes : Image 1 data (WIDTHxWIDTH)
 *          ...
 *     -   1 byte  : Image N label
 *     - NUM_PIXELS bytes : Image N data (WIDTHxWIDTH)
 *
 * You can set the `sx` and `sy` values for all the images to WIDTH. 
 * Use the NUM_PIXELS and WIDTH constants defined in dectree.h
 */
Dataset *load_dataset(const char *filename) {
    // TODO: Allocate data, read image data / labels, return
	Dataset *new_dataset = malloc(sizeof(Dataset));
	
	//Image *new_image = malloc(sizeof(Image));
	
	FILE *data_file;
	int num_images;
	int i = 0;
	int error;
	int pixel_counter = 1;
	int read_images = 0;
	
	data_file = fopen(filename, "r");
	if(data_file == NULL)
	{
		fprintf(stderr, "Error opening file\n");
		return NULL;
	}
	
	fread(&num_images,4,1,data_file); //read num images
	new_dataset->num_items = num_images; //store it
	
	new_dataset->images = malloc(sizeof(Image)*num_images); //allocate space for all images
	new_dataset->labels = malloc(sizeof(unsigned char)*num_images); //allocate space for all labels
	
	for(int i = 0; i<num_images; i++)
	{
		((new_dataset->images)+i)->data = malloc(sizeof(unsigned char)*NUM_PIXELS); //allocate space for data in each image
	}
	
	
	while(read_images<=num_images) //read next image
	{
		fread(((new_dataset->labels)+read_images), 1, 1, data_file); //read in label
		//printf("read label: %u", *(new_dataset->labels+read_images));
		
		while(pixel_counter<=NUM_PIXELS) //read single image
		{
			fread((((new_dataset->images)+read_images)->data+i),1,1,data_file);
			pixel_counter++;
			i++;
		}
		
		((new_dataset->images)+read_images)->sx = WIDTH;
		((new_dataset->images)+read_images)->sy = WIDTH;
		
		pixel_counter = 1;
		i = 0;
		read_images++;
	}

	
	error = fclose(data_file);
	if(error != 0)
	{
		fprintf(stderr, "Error: fclose failed.\n");
		return NULL;
	}
	
    return new_dataset;
}

/**
 * Compute and return the Gini impurity of M images at a given pixel
 * The M images to analyze are identified by the indices array. The M
 * elements of the indices array are indices into data.
 * This is the objective function that you will use to identify the best 
 * pixel on which to split the dataset when building the decision tree.
 *
 * Note that the gini_impurity implemented here can evaluate to NAN 
 * (Not A Number) and will return that value. Your implementation of the 
 * decision trees should ensure that a pixel whose gini_impurity evaluates 
 * to NAN is not used to split the data.  (see find_best_split)
 * 
 * DO NOT CHANGE THIS FUNCTION; It is already implemented for you.
 */
double gini_impurity(Dataset *data, int M, int *indices, int pixel) {
    int a_freq[10] = {0}, a_count = 0;
    int b_freq[10] = {0}, b_count = 0;

    for (int i = 0; i < M; i++) {
        int img_idx = indices[i];

        // The pixels are always either 0 or 255, but using < 128 for generality.
        if (data->images[img_idx].data[pixel] < 128) {
            a_freq[data->labels[img_idx]]++;
            a_count++;
        } else {
            b_freq[data->labels[img_idx]]++;
            b_count++;
        }
    }

    double a_gini = 0, b_gini = 0;
    for (int i = 0; i < 10; i++) {
        double a_i = ((double)a_freq[i]) / ((double)a_count);
        double b_i = ((double)b_freq[i]) / ((double)b_count);
        a_gini += a_i * (1 - a_i);
        b_gini += b_i * (1 - b_i);
    }

    // Weighted average of gini impurity of children
    return (a_gini * a_count + b_gini * b_count) / M;
}

/**
 * Given a subset of M images and the array of their corresponding indices, 
 * find and use the last two parameters (label and freq) to store the most
 * frequent label in the set and its frequency.
 *
 * - The most frequent label (between 0 and 9) will be stored in `*label`
 * - The frequency of this label within the subset will be stored in `*freq`
 * 
 * If multiple labels have the same maximal frequency, return the smallest one.
 */
void get_most_frequent(Dataset *data, int M, int *indices, int *label, int *freq) {
    // TODO: Set the correct values and return
    *label = 0;
    *freq = 0;
	
	int label_frequences[10];
	int index;
	
	for(int i = 0; i<M; i++)
	{
		index = *(indices+i);
		label_frequences[*(data->labels+index)]++;
	}
	
	int max_index = 0;
	
	for(int j = 1; j<=10; j++)
	{
		if(label_frequences[j]>max_index)
		{
			max_index = j;
		}
	}
	
	*(label) = max_index;
	*(freq) = label_frequences[max_index];
	
    return;
}

/**
 * Given a subset of M images as defined by their indices, find and return
 * the best pixel to split the data. The best pixel is the one which
 * has the minimum Gini impurity as computed by `gini_impurity()` and 
 * is not NAN. (See handout for more information)
 * 
 * The return value will be a number between 0-783 (inclusive), representing
 *  the pixel the M images should be split based on.
 * 
 * If multiple pixels have the same minimal Gini impurity, return the smallest.
 */
int find_best_split(Dataset *data, int M, int *indices) {
    // TODO: Return the correct pixel
	
	int least_gini;
	int temp;
	int return_pixel;
	
	for(int i = 0; i<NUM_PIXELS; i++)
	{
		temp = gini_impurity(data, M, indices, i);
		
		if(temp<least_gini)
		{
			least_gini = temp;
			return_pixel = i;
		}
	}
	
    return return_pixel;
}

/**
 * Create the Decision tree. In each recursive call, we consider the subset of the
 * dataset that correspond to the new node. To represent the subset, we pass 
 * an array of indices of these images in the subset of the dataset, along with 
 * its length M. Be careful to allocate this indices array for any recursive 
 * calls made, and free it when you no longer need the array. In this function,
 * you need to:
 *
 *    - Compute ratio of most frequent image in indices, do not split if the
 *      ration is greater than THRESHOLD_RATIO
 *    - Find the best pixel to split on using `find_best_split`
 *    - Split the data based on whether pixel is less than 128, allocate 
 *      arrays of indices of training images and populate them with the 
 *      subset of indices from M that correspond to which side of the split
 *      they are on
 *    - Allocate a new node, set the correct values and return
 *       - If it is a leaf node set `classification`, and both children = NULL.
 *       - Otherwise, set `pixel` and `left`/`right` nodes 
 *         (using build_subtree recursively). 
 */
DTNode *build_subtree(Dataset *data, int M, int *indices) {
    // TODO: Construct and return the tree

	//DTNode *root = malloc(sizeof(DTNode));
    return NULL;
}

/**
 * This is the function exposed to the user. All you should do here is set
 * up the `indices` array correctly for the entire dataset and call 
 * `build_subtree()` with the correct parameters.
 */
DTNode *build_dec_tree(Dataset *data) {
    // TODO: Set up `indices` array, call `build_subtree` and return the tree.
    // HINT: Make sure you free any data that is not needed anymore
	
	//int M;
	//int *indices;
	
	//build_subtree(data, M, indices);

    return NULL;
}

int classify(DTNode *root, Image *img)
{
	while(root->classification == -1)
	{
		if(*(img->data+(root->pixel)) < 128)
		{
			classify(root->left, img);
		}
		else
		{
			classify(root->right, img);
		}
	}
	
	return root->classification;
}

/**
 * Given a decision tree and an image to classify, return the predicted label.
 */
int dec_tree_classify(DTNode *root, Image *img) {
    // TODO: Return the correct label
	int predicted_label = -1;
	
	predicted_label = classify(root, img);
    
	return predicted_label;
}

/**
 * This function frees the Decision tree.
 */
void free_dec_tree(DTNode *node) {
    // TODO: Free the decision tree
	
	if(node != NULL)
	{
		free_dec_tree(node->right);
		free_dec_tree(node->left);
		free(node);
	}

    return;
}

/**
 * Free all the allocated memory for the dataset
 */
void free_dataset(Dataset *data) {
    // TODO: Free dataset (Same as A1)

	for(int i = 0; i<data->num_items;i++)
	{
		free(data->images+i);
		free(data->labels+i);
	}
	
	free(data->labels);
	free(data->images);
	free(data);
	
    return;
}

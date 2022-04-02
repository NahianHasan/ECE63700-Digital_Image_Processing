
#include <math.h>
#include "tiff.h"
#include "allocate.h"
#include "typeutil.h"

void error(char *name);
void swap(double *a, double *b);
void bubbleSort(double array1[], double array2[], int n);


// Function to swap elements
void swap(double *a, double *b){
	int temp = *a;
	*a = *b;
	*b = temp;
}
// bubble sort function
void bubbleSort(double array1[], double array2[], int n) {
	int i, j;
	for (i = 0; i < n-1; i++){
		for (j = 0; j < n-i-1; j++){
			if (array1[j] < array1[j+1]) {
				swap(&array1[j], &array1[j+1]);
				swap(&array2[j], &array2[j+1]);
			}
		}
	}
}

int main (int argc, char **argv)
{
	FILE *fp;
	struct TIFF_img input_img, filtered_img;
	double **img,**img_2;
	int32_t i,j,k,l,pixel,ind;
	double temp_index_1,temp_index_2;
	double X[25];
	double a[25] = {1,1,1,1,1,1,2,2,2,1,1,2,2,2,1,1,2,2,2,1,1,1,1,1,1};

	if ( argc != 2 ) error( argv[0] );

	/* open image file */
	if ( ( fp = fopen ( argv[1], "rb" ) ) == NULL ) {
		fprintf ( stderr, "cannot open file %s\n", argv[1] );
		exit ( 1 );
	}

	/* read image */
	if ( read_TIFF ( fp, &input_img ) ) {
		fprintf ( stderr, "error reading file %s\n", argv[1] );
		exit ( 1 );
	}

	/* close image file */
	fclose ( fp );

	/* check the type of image data */
	if ( input_img.TIFF_type != 'g' ) {
		fprintf ( stderr, "error:  image must be 24-bit color\n" );
		exit ( 1 );
	}

	/* Allocate image of double precision floats */
	img = (double **)get_img(input_img.width+4,input_img.height+4,sizeof(double));
	img_2 = (double **)get_img(input_img.width,input_img.height,sizeof(double));
	fprintf ( stderr,"copy image to double padded array\n" );
	for ( i = 2; i < input_img.height+2; i++ ){
		for ( j = 2; j < input_img.width+2; j++ ) {
			//printf("%d\n",input_img.mono[i-2][j-2]);
			img[i][j] = input_img.mono[i-2][j-2];
		}
	}

	for ( i = 0; i < input_img.height+4; i++ ) {
		for ( j=0;j<2;j++ ) {
			img[i][j] = 0;
		}
		for ( j=input_img.width+2;j<input_img.width+4;j++ ) {
			img[i][j] = 0;
		}
	}
	for ( j = 2; j < input_img.width+2; j++ ) {
		for ( i=0;i<2;i++ ) {
			img[i][j] = 0;
		}
		for ( i=input_img.height+2;i<input_img.height+4;i++ ) {
			img[i][j] = 0;
		}
	}

	fprintf ( stderr,"Filter image\n" );
	for ( i = 2; i < input_img.height+2; i++ ) {
		for ( j = 2; j < input_img.width+2; j++ ) {
			ind = 0;
			for ( k=i-2; k<=i+2; k++ ) {
				for ( l=j-2; l<=j+2; l++ ) {
					X[ind] = img[k][l];
					ind += 1;
				}
			}
			//Sort X array
			bubbleSort(X, a, sizeof(X)/sizeof(X[0]));

			//find the median
			k=1;
			temp_index_1 = 0;
			temp_index_2 = 0;
			while(1) {
				for (l=0; l<=k; l++){
					temp_index_1 = temp_index_1 + a[l];
				}
				for (l=k+1; l<sizeof(a)/sizeof(a[0]); l++){
					temp_index_2 = temp_index_2 + a[l];
				}
				if (temp_index_1 >= temp_index_2) {
					break;
				}
				temp_index_1 = 0;
				temp_index_2 = 0;
				k += 1;
			}
			//k is the median index
			img_2[i-2][j-2] = X[k];
		}
	}
	free_img( (void**)img );

	/* set up structure for output color image */
	/* Note that the type is 'c' rather than 'g' */
	get_TIFF ( &filtered_img, input_img.height, input_img.width, 'g' );
	fprintf ( stderr,"copy filtered component to new images\n" );
	for ( i = 0; i < input_img.height; i++ ) {
		for ( j = 0; j < input_img.width; j++ ) {
			pixel = (int32_t)img_2[i][j];
			if(pixel>255) {
				pixel = 255;
			}
			if(pixel<0) {
				pixel = 0;
			}
			filtered_img.mono[i][j] = (int32_t)pixel;
		}
	}
	free_img( (void**)img_2 );

	/* open color image file */
	if ( ( fp = fopen ( "section_2_filtered.tif", "wb" ) ) == NULL ) {
		fprintf ( stderr, "cannot open file section_2_filtered.tif\n");
		exit ( 1 );
	}

	/* write color image */
	if ( write_TIFF ( fp, &filtered_img ) ) {
		fprintf ( stderr, "error writing TIFF file %s\n", argv[2] );
		exit ( 1 );
	}

	/* close color image file */
	fclose ( fp );

	/* de-allocate space which was used for the images */
	free_TIFF ( &(input_img) );
	free_TIFF ( &(filtered_img) );

	return(0);
}

void error(char *name)
{
	printf("usage:  %s  image.tiff \n\n",name);
	printf("this program reads in a 24-bit color TIFF image.\n");
	printf("It then horizontally filters the green component, adds noise,\n");
	printf("and writes out the result as an 8-bit image\n");
	printf("with the name 'green.tiff'.\n");
	printf("It also generates an 8-bit color image,\n");
	printf("that swaps red and green components from the input image");
	exit(1);
}

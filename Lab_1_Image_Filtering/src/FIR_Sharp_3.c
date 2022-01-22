
#include <math.h>
#include "tiff.h"
#include "allocate.h"
#include "typeutil.h"
#include <string.h>

void error(char *name);

int main (int argc, char **argv)
{
	FILE *fp;
	struct TIFF_img input_img, red_img, green_img, blue_img, color_img;
	double **img_r,**img_g,**img_b,**img_2_r,**img_2_g,**img_2_b,temp,lambda;
	char file_name[50];
	int32_t i,j,k,l,pixel;

	if ( argc != 3 ) error( argv[0] );

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
	if ( input_img.TIFF_type != 'c' ) {
		fprintf ( stderr, "error:  image must be 24-bit color\n" );
		exit ( 1 );
	}
	fprintf ( stderr, "Lambda =  %s\n", argv[2] );
	sscanf(argv[2],"%lf",&lambda);
	/* Allocate image of double precision floats */
	img_r = (double **)get_img(input_img.width,input_img.height,sizeof(double));
	img_2_r = (double **)get_img(input_img.width,input_img.height,sizeof(double));
	fprintf ( stderr,"copy red component to double array\n" );
	for ( i = 0; i < input_img.height; i++ ){
		for ( j = 0; j < input_img.width; j++ ) {
			img_r[i][j] = input_img.color[0][i][j];
		}
	}
	fprintf ( stderr,"Filter image, red channel\n" );
	for ( i = 2; i < input_img.height-2; i++ ) {
		for ( j = 2; j < input_img.width-2; j++ ) {
			temp = 0;
			for ( k=i-2; k<=i+2; k++ ) {
				for ( l=j-2; l<=j+2; l++ ) {
					temp = temp + img_r[k][l];
				}
			}
			temp = img_r[i][j] + lambda*(img_r[i][j] - temp/25);
			img_2_r[i][j] = temp;
		}
	}
	free_img( (void**)img_r );
	fprintf ( stderr,"Fill in boundary pixels -- red channel\n" );
	for ( i = 0; i < input_img.height; i++ ) {
		for ( j=0;j<2;j++ ) {
			img_2_r[i][j] = 0;
		}
		for ( j=input_img.width-2;j<=input_img.width-1;j++ ) {
			img_2_r[i][j] = 0;
		}
	}
	for ( j = 2; j < input_img.width-2; j++ ) {
		for ( i=0;i<2;i++ ) {
			img_2_r[i][j] = 0;
		}
		for ( i=input_img.height-2;i<=input_img.height-1;i++ ) {
			img_2_r[i][j] = 0;
		}
	}
	/* set up structure for output color image */
	/* Note that the type is 'c' rather than 'g' */
	get_TIFF ( &red_img, input_img.height, input_img.width, 'g' );
	fprintf ( stderr,"copy red component to new images\n" );
	for ( i = 0; i < input_img.height; i++ ) {
		for ( j = 0; j < input_img.width; j++ ) {
			pixel = (int32_t)img_2_r[i][j];
			if(pixel>255) {
				pixel = 255;
			}
			if(pixel<0) {
				pixel = 0;
			}
			red_img.mono[i][j] = (int32_t)pixel;
		}
	}
	free_img( (void**)img_2_r );



	img_g = (double **)get_img(input_img.width,input_img.height,sizeof(double));
	img_2_g = (double **)get_img(input_img.width,input_img.height,sizeof(double));
	fprintf ( stderr,"copy green component to double array\n" );
	for ( i = 0; i < input_img.height; i++ ){
		for ( j = 0; j < input_img.width; j++ ) {
			img_g[i][j] = input_img.color[1][i][j];
		}
	}
	fprintf ( stderr,"Filter image, green channel\n" );
	for ( i = 2; i < input_img.height-2; i++ ) {
		for ( j = 2; j < input_img.width-2; j++ ) {
			temp = 0;
			for ( k=i-2; k<=i+2; k++ ) {
				for ( l=j-2; l<=j+2; l++ ) {
					temp = temp + img_g[k][l];
				}
			}
			temp = img_g[i][j] + lambda*(img_g[i][j] - temp/25);
			img_2_g[i][j] = temp;
		}
	}
	free_img( (void**)img_g );
	fprintf ( stderr,"Fill in boundary pixels -- green channel\n" );
	for ( i = 0; i < input_img.height; i++ ) {
		for ( j=0;j<2;j++ ) {
			img_2_g[i][j] = 0;
		}
		for ( j=input_img.width-2;j<=input_img.width-1;j++ ) {
			img_2_g[i][j] = 0;
		}
	}
	for ( j = 2; j < input_img.width-2; j++ ) {
		for ( i=0;i<2;i++ ) {
			img_2_g[i][j] = 0;
		}
		for ( i=input_img.height-2;i<=input_img.height-1;i++ ) {
			img_2_g[i][j] = 0;
		}
	}
	get_TIFF ( &green_img, input_img.height, input_img.width, 'g' );
	fprintf ( stderr,"copy green component to new images\n" );
	for ( i = 0; i < input_img.height; i++ ){
		for ( j = 0; j < input_img.width; j++ ) {
			pixel = (int32_t)img_2_g[i][j];
			if(pixel>255) {
				pixel = 255;
			}
			if(pixel<0) {
				pixel = 0;
			}
			green_img.mono[i][j] = (int32_t)pixel;
		}
	}
	free_img( (void**)img_2_g );






	img_b = (double **)get_img(input_img.width,input_img.height,sizeof(double));
	img_2_b = (double **)get_img(input_img.width,input_img.height,sizeof(double));
	fprintf ( stderr,"copy blue component to double array\n" );
	for ( i = 0; i < input_img.height; i++ ){
		for ( j = 0; j < input_img.width; j++ ) {
			img_b[i][j] = input_img.color[2][i][j];
		}
	}
	fprintf ( stderr,"Filter image, blue channel\n" );
	for ( i = 2; i < input_img.height-2; i++ ) {
		for ( j = 2; j < input_img.width-2; j++ ) {
			temp = 0;
			for ( k=i-2; k<=i+2; k++ ) {
				for ( l=j-2; l<=j+2; l++ ) {
					temp = temp + img_b[k][l];
				}
			}
			temp = img_b[i][j] + lambda*(img_b[i][j] - temp/25);
			img_2_b[i][j] = temp;
		}
	}
	free_img( (void**)img_b );
	fprintf ( stderr,"Fill in boundary pixels -- blue channel\n" );
	for ( i = 0; i < input_img.height; i++ ) {
		for ( j=0;j<2;j++ ) {
			img_2_b[i][j] = 0;
		}
		for ( j=input_img.width-2;j<=input_img.width-1;j++ ) {
			img_2_b[i][j] = 0;
		}
	}
	for ( j = 2; j < input_img.width-2; j++ ) {
		for ( i=0;i<2;i++ ) {
			img_2_b[i][j] = 0;
		}
		for ( i=input_img.height-2;i<=input_img.height-1;i++ ) {
			img_2_b[i][j] = 0;
		}
	}
	get_TIFF ( &blue_img, input_img.height, input_img.width, 'g' );
	fprintf ( stderr,"copy blue component to new images\n" );
	for ( i = 0; i < input_img.height; i++ ){
		for ( j = 0; j < input_img.width; j++ ) {
			pixel = (int32_t)img_2_b[i][j];
			if(pixel>255) {
				pixel = 255;
			}
			if(pixel<0) {
				pixel = 0;
			}
			blue_img.mono[i][j] = (int32_t)pixel;
		}
	}
	free_img( (void**)img_2_b );


	get_TIFF ( &color_img, input_img.height, input_img.width, 'c' );
	fprintf ( stderr,"constructing filtered color image" );
	for ( i = 0; i < input_img.height; i++ ) {
		for ( j = 0; j < input_img.width; j++ ) {
			color_img.color[0][i][j] = red_img.mono[i][j];
			color_img.color[1][i][j] = green_img.mono[i][j];
			color_img.color[2][i][j] = blue_img.mono[i][j];
		}
	}

	/* open color image file */
	strcpy(file_name,"sharpened_image_");
	strcat(file_name,argv[2]);
	strcat(file_name,".tif");
	if ( ( fp = fopen ( file_name, "wb" ) ) == NULL ) {
		fprintf ( stderr, "cannot open file sharpened_image.tif\n");
		exit ( 1 );
	}

	/* write color image */
	if ( write_TIFF ( fp, &color_img ) ) {
		fprintf ( stderr, "error writing TIFF file %s\n", argv[3] );
		exit ( 1 );
	}

	/* close color image file */
	fclose ( fp );

	/* de-allocate space which was used for the images */
	free_TIFF ( &(input_img) );
	free_TIFF ( &(red_img) );
	free_TIFF ( &(green_img) );
	free_TIFF ( &(blue_img) );
	free_TIFF ( &(color_img) );



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

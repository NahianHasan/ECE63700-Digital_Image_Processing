#include <math.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include "allocate.h"
#include "typeutil.h"
#include "tiff.h"


struct pixel {
	int m,n;/*m=row, n=column*/
};
void error(char *name);
void ConnectedNeighbors(struct pixel s,
												double T,
												unsigned char **img,
												int width,
												int height,
												int *M,
												struct pixel * c);
int CheckExisting(struct pixel * c,struct pixel * check,struct pixel * TMP,int PC, int M);
void UpdateArray(struct pixel *B, int current_length);
void ConnectedSet(struct pixel s,
									double T,
									unsigned char **img,
									int width,
									int height,
									int ClassLabel,
									unsigned int **seg,
									int *NumConPixels);
int update_unlabelled_img(struct pixel *unlabelled_img,unsigned int **seg,int width,int height,int ClassLabel,int *NumConPixels,struct pixel s);

int main(int argc, char **argv)
{
	FILE *fp;
	struct TIFF_img raw_img, segmented_img;
	unsigned char **input_img;
	struct pixel s;
	unsigned int** seg;
	int T,i,j;
	int ClassLabel,NumConPixels;

	if ( argc != 4 ) error( argv[0] );

	/* open image file */
	if ( ( fp = fopen ( argv[1], "rb" ) ) == NULL ) {
		fprintf ( stderr, "cannot open file %s\n", argv[1] );
		exit ( 1 );
	}

	/* read image */
	if ( read_TIFF ( fp, &raw_img ) ) {
		fprintf ( stderr, "error reading file %s\n", argv[1] );
		exit ( 1 );
	}

	/* close image file */
	fclose ( fp );
	/* check the type of image data */
	if ( raw_img.TIFF_type != 'g' ) {
		fprintf ( stderr, "error:  image must be 24-bit color\n" );
		exit ( 1 );
	}

	sscanf(argv[2],"%d",&T);
	sscanf(argv[3],"%d",&ClassLabel);

	printf("\n\nFinding Connected Components for Threshold = %d",T);
	input_img = (unsigned char **)get_img(raw_img.width,raw_img.height,sizeof(int));
	printf("\nImage Width=%d\n",raw_img.width);
	printf("Image Height=%d\n",raw_img.height);
	for (i=0;i<raw_img.height;i++){
		for (j=0;j<raw_img.width;j++){
			input_img[i][j] = (unsigned char)raw_img.mono[i][j];
		}
	}

	seg = (unsigned int **)get_img(raw_img.width,raw_img.height,sizeof(int));
	for (i=0;i<raw_img.height;i++){
		for (j=0;j<raw_img.width;j++){
			seg[i][j] = 0;
		}
	}
	printf("Data Read\n");

	s.m=67;
	s.n=45;
	ConnectedSet(s,T,input_img,raw_img.width,raw_img.height,ClassLabel,seg,&NumConPixels);

	//Save the segmented image
	get_TIFF ( &segmented_img, raw_img.height, raw_img.width, 'g' );
	for (i=0;i<raw_img.height;i++){
		for (j=0;j<raw_img.width;j++){
			segmented_img.mono[i][j] = (int32_t)seg[i][j];
		}
	}

	if ( ( fp = fopen ( "connected_components.tif", "wb" ) ) == NULL ) {
		fprintf ( stderr, "cannot open file connected_components.tif\n");
		exit ( 1 );
	}
	if ( write_TIFF ( fp, &segmented_img ) ) {
		fprintf ( stderr, "error writing TIFF file %s\n", argv[2] );
		exit ( 1 );
	}
	fclose ( fp );

	return(0);
}

int update_unlabelled_img(struct pixel *unlabelled_img,unsigned int **seg,int width,int height,int ClassLabel,int *NumConPixels,struct pixel s){
	int i,j,count=0;
	if (*NumConPixels==3 || *NumConPixels==2 || *NumConPixels==1 || *NumConPixels==0 || *NumConPixels==4){
		seg[s.m][s.n] = ClassLabel;
	}
	for (i=0;i<height;i++){
		for (j=0;j<width;j++){
			if (seg[i][j] == 0){
				unlabelled_img[count].m = i;
				unlabelled_img[count].n = j;
				count++;
			}
		}
	}
	return count;
}



void ConnectedNeighbors(struct pixel s,
												double T,
												unsigned char **img,
												int width,
												int height,
												int *M,
												struct pixel * c){
	int ind=0;
	*M = 0;
	if (s.m-1 >= 0){
		if (abs(img[s.m][s.n]-img[s.m-1][s.n]) <= T){
			c[ind].m=s.m-1;
			c[ind].n=s.n;
			++*M;
			ind++;
		}
	}

	if (s.m+1 < height){
		if (abs(img[s.m][s.n]-img[s.m+1][s.n]) <= T){
			c[ind].m=s.m+1;
			c[ind].n=s.n;
			++*M;
			ind++;
		}
	}

	if (s.n-1 >= 0){
		if (abs(img[s.m][s.n]-img[s.m][s.n-1]) <= T){
			c[ind].m=s.m;
			c[ind].n=s.n-1;
			++*M;
			ind++;
		}
	}

	if (s.n+1 < width){
		if (abs(img[s.m][s.n]-img[s.m][s.n+1]) <= T){
			c[ind].m=s.m;
			c[ind].n=s.n+1;
			++*M;
		}
	}
}

int CheckExisting(struct pixel * c,struct pixel * check,struct pixel * TMP,int PC, int M){
	int count=0;
	int i,j,flag;
	for (i=0;i<M;i++){
		flag=0;
		for (j=0;j<PC;j++){
			if (c[i].m==TMP[j].m && c[i].n==TMP[j].n){
				flag=1;
				break;
			}
		}
		if (flag==0){
			check[count].m=c[i].m;
			check[count].n=c[i].n;
			count++;
		}
	}
	return count;
}

void UpdateArray(struct pixel *B,int current_length){
	int i;
	for (i=1;i<current_length;i++){
		B[i-1].m = B[i].m;
		B[i-1].n = B[i].n;
	}
}

void ConnectedSet(struct pixel s,
									double T,
									unsigned char **img,
									int width,
									int height,
									int ClassLabel,
									unsigned int **seg,
									int *NumConPixels){
	struct pixel c[4];
	struct pixel check[4];
	struct pixel *B;
	struct pixel *TMP;
	int M=0,i,temp,total_pixels=0;
	int current_length=0,num_count,pix_count=0;


	ConnectedNeighbors(s,T,img,width,height,&M,c);
	B=malloc(M*2*sizeof(int));
	TMP=malloc(M*2*sizeof(int));
	for (i=0;i<M;i++){
		B[i].m=c[i].m;
		B[i].n=c[i].n;
		TMP[i].m=c[i].m;
		TMP[i].n=c[i].n;
	}

	current_length = current_length+M;
	pix_count = pix_count+M;

	M=0;
	while (current_length >0){
		s.m = B[0].m;
		s.n = B[0].n;
		UpdateArray(B,current_length);
		current_length = current_length-1;

		seg[s.m][s.n] = ClassLabel;
		//printf("s.m=%d,",s.m);
		//printf("s.n=%d\n",s.n);
		ConnectedNeighbors(s,T,img,width,height,&M,c);

		//check whether the connected components of the current c are already inside B. If any of them are, then don't include it.
		num_count = CheckExisting(c,check,TMP,pix_count,M);
		total_pixels = total_pixels + num_count;
		//printf("%d\n",current_length);
		if (current_length==0){
			break;
		}
		if (num_count>0){
			B = realloc(B, (current_length+num_count)*2*sizeof(int));
			TMP = realloc(TMP, (pix_count+num_count)*2*sizeof(int));
		}

		temp=0;
		for (i=current_length;i<(current_length+num_count);i++){
			B[i].m = check[temp].m;
			B[i].n = check[temp].n;
			temp++;
		}
		temp=0;
		for (i=pix_count;i<(pix_count+num_count);i++){
			TMP[i].m = check[temp].m;
			TMP[i].n = check[temp].n;
			temp++;
		}

		current_length = current_length+num_count;
		pix_count = pix_count+num_count;
	}
	*NumConPixels = total_pixels;
}

void error(char *name)
{
	printf("Data Could Not Read\n");
	exit(1);
}

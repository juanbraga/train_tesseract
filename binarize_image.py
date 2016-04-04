import cv2
from matplotlib import pyplot as plt
import argparse, glob, os, logging

def binarize(inputfile, outputfile, threshold, inv):

    if outputfile is None:
        outputfile = inputfile[:-4] + "_bin.tiff"    
    
    img = cv2.imread(inputfile,0)
    img = cv2.medianBlur(img,5)
     
    if (inv):
        ret,binary = cv2.threshold(img,float(threshold),255,cv2.THRESH_BINARY)
    else:
        ret,binary = cv2.threshold(img,float(threshold),255,cv2.THRESH_BINARY_INV)
    
    print outputfile
    cv2.imwrite(outputfile, binary)
#    plt.imshow(binary, 'binary')
#    plt.title('threshold')
#    plt.xticks([]),plt.yticks([])
#    plt.show()

def binarize_batch(inputfolder, outputfolder, threshold, inv):
    
    # Load all files in input folder that end with .jpg or .png
    inputfiles = glob.glob(os.path.join(inputfolder, "*.jpg"))
    inputfiles.extend(glob.glob(os.path.join(inputfolder, "*.tif")))

    print inv
    
    for inputfile in inputfiles:

        print inputfile        
        
        if outputfolder is not None:
            outfolder = outputfolder
            if not os.path.isdir(outfolder):
                os.mkdir(outfolder)
        else:
            outfolder = inputfolder

        outputfilename = os.path.basename(inputfile)[:-4] + "_bin.tiff"
        outputfile = os.path.join(outfolder, outputfilename)
        logging.info("Processing: " + inputfile)
        logging.info("Target    : " + outputfile)

        binarize(inputfile, outputfile, threshold, inv)
    

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description="Apply threshold to image.")
    parser.add_argument("inputfile", help="Path to input file containing the "
                        "pitch sequence")
    parser.add_argument("--output", help="Path to output image file. If "
                        "not specified a file will be created with the same "
                        "path/name as inputfile but ending with "
                        
                        "\"_bin.tiff\".")
    parser.add_argument("--threshold", default=100, help="Threshold for binarizing "
                        "the input image. If not specified the default "
                        "value of 100 is used.")
    parser.add_argument("--inv", default=False, help="Invert binary image. " 
                        "If not specified 255 for values over threshold")
    parser.add_argument("--batch", default=False, dest='batch',
                        action='store_const', const=True, help="Treat "
                        "inputfile as a folder and batch process every file "
                        "within this folder that ends with .csv or .txt. If "
                        "--output is specified it is expected to be a folder "
                        "too. If --output is not specified, all binarized "
                        "images will be saved into the input folder.")

    args = parser.parse_args()

    if args.inputfile is not None:

        if args.batch:
            binarize_batch(args.inputfile, args.output, args.threshold, args.inv)
        else:
            binarize(args.inputfile, args.output, args.threshold, args.inv)
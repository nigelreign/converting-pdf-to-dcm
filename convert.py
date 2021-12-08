from pdf2image import convert_from_path
from PIL import Image
import numpy as np
import pydicom

# Get the pdf from path
images = convert_from_path('test.pdf', poppler_path=r'C:\Users\NigelReign\Downloads\poppler-0.68.0_x86\poppler-0.68.0\bin')
 
#  First connvert the pdf to png/jpg
for i in range(len(images)):
    images[i].save('page'+ str(i) +'.jpg', 'JPEG')

#get the converted image
im_frame = Image.open('page0.jpg') # the converted pdf from image

# converting the image to dcm
# Create a dcm file with similar attributes as your generated image
# reference the pre-existing dcm file

ds = pydicom.dcmread('original/test_image.dcm') # pre-existing dicom file
    
if im_frame.mode == 'L':    
    np_image = np.array(im_frame.getdata(),dtype=np.uint8)
    ds.Rows = im_frame.height
    ds.Columns = im_frame.width
    ds.PhotometricInterpretation = "MONOCHROME2"
    ds.SamplesPerPixel = 1
    ds.BitsStored = 8
    ds.BitsAllocated = 8
    ds.HighBit = 7
    ds.PixelRepresentation = 0
    ds.PixelData = np_image.tobytes()
    ds.PatientName = "XX"
    ds.save_as('result_gray.dcm')
if im_frame.mode == 'Li':
    # (8-bit pixels, black and white)
    np_frame = np.array(im_frame.getdata(),dtype=np.uint8)
    ds.Rows = im_frame.height
    ds.Columns = im_frame.width
    ds.PhotometricInterpretation = "MONOCHROME1"
    ds.SamplesPerPixel = 1
    ds.BitsStored = 8
    ds.BitsAllocated = 8
    ds.HighBit = 7
    ds.PixelRepresentation = 0
    ds.PixelData = np_frame.tobytes()
    ds.save_as('converted_image_l.dcm')
elif im_frame.mode == 'RGB':
    # RGBA (4x8-bit pixels, true colour with transparency mask)
    np_frame = np.array(im_frame.getdata(), dtype=np.uint8)[:,:3]
    ds.Rows = im_frame.height
    ds.Columns = im_frame.width
    ds.PhotometricInterpretation = "RGB"
    ds.SamplesPerPixel = 3
    ds.BitsStored = 8
    ds.BitsAllocated = 8
    ds.HighBit = 7
    ds.PixelRepresentation = 0
    ds.PixelData = np_frame.tobytes()
    ds.save_as('converted_image_rgb.dcm')
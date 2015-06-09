import os, sys
from PIL import Image

def process(name,image,size=32,format="png"):
	box = image.copy()
	saved_name = "done/%s" % name
	im_w ,im_h= box.size

	width 	= im_w / size
	height 	= im_h / size
	newSize = size + 2

	new_img_w = newSize * width
	new_img_h = newSize * height

	new_img = Image.new("RGBA",(new_img_w,new_img_h))

	for h in range(0,height):
		for w in range(0, width):
			left  	= w * size
			top	 	= h * size
			right 	= left + size
			bottom	= top + size 
			
			croped  	= box.crop((left,top,right,bottom))
			new_croped 	= Image.new("RGBA",(newSize,newSize))

			## enlarge the image with new data
			pixels = croped.load()
			pixels_new = new_croped.load()

		 	pixel_top 		= 	[pixels[i,0] for i in range(0,size)]
		 	pixel_left 		=	[pixels[0,i] for i in range(0,size)]
		 	pixel_right 	= 	[pixels[size -1, i] for i in range(0,size)]	
		 	pixel_bottom 	=	[pixels[ i,size -1 ] for i in range(0,size)]

			# copy 
			for h0 in range(size):
				for w0 in range(size):
					pixels_new[w0 + 1,h0 + 1] = pixels[w0,h0]

			# copy extra
			for i in range(1,newSize - 1):
				pixels_new[i,0] = pixel_top[i - 1]  # top
				pixels_new[i,newSize -1] = pixel_bottom[i-1] # bottom
				pixels_new[0,i] = pixel_left[i-1] # left
				pixels_new[newSize-1,i] = pixel_right[i-1]
			
			# merge
			new_img.paste(new_croped,(w * newSize,h * newSize))

	new_img.save(saved_name,format)


if __name__ == '__main__':

	if not os.path.exists('tilesets'):
		printf("can't find directory tilesets")
		exit

	if not os.path.exists('done'):
		os.mkdir('done')

	size = 32
	format = "png"
	try:
		size = int(sys.argv[1])
		format = sys.argv[2]
	except Exception, e:
		pass

	for file in os.listdir('tilesets'):
		f_name = file.upper()
		if f_name.endswith("PNG"):
			image = Image.open("tilesets/%s" % file)
			process(file,image,size,format)
			print "%s finished" % file

	print "ok!"



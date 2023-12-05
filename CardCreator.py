from PIL import Image, ImageTk, ImageDraw, ImageFont

class CardCreator(object):

  def __init__(self, brand_text, model_text, grimg_file: Image, height=265, width=132):
    self.brand = brand_text
    try:
      self.model = model_text
    except Exception as e:
      print(e)
    self.grimg = grimg_file
    self.img_height = height
    self.img_width = width
    print("initalization complete")

  def getImgHeight(self):
    return self.img_height

  def getImgWidth(self):
    return self.img_width

  def getBrand(self):
    return self.brand

  def getModel(self):
    return self.model

  def getQR(self):
    return self.grimg

  def getFont(self, size):
    if size < 14:
      size = 14
    return ImageFont.truetype("arialbd.ttf", size)

  def getNewQRsize(self):
    height = int(self.getImgHeight()*0.47)
    width = int(self.getImgWidth()*0.88)
    print("width = " + str(width))
    return (width,height)

  def getCenterX(self):
    return self.getImgWidth()*0.5

  def getBrandPos(self):
    height_from_top = self.getImgHeight()*0.1
    width_from_left = self.getCenterX()
    print(f"height = {height_from_top}\n width= {width_from_left}")
    return width_from_left, height_from_top

  def getModelPos(self, modelpart, modelsize, brandsize):
    w, brand_height = self.getBrandPos()
    brand_height += self.getPixelFromMM(self.getPointHeightInMM(brandsize))
    offset = 0
    if modelpart==2:
      if modelsize==-1:
        modelsize=12
      model_height = self.getPixelFromMM(self.getPointHeightInMM(modelsize))+5
      offset = model_height
    height_from_top = offset + brand_height + self.getImgHeight() * 0.05
    width_from_left = self.getCenterX()
    return (width_from_left, height_from_top)

  def getQRpos(self):
    height_from_top = int(self.getImgHeight()*0.46)
    width_from_left = int(self.getImgWidth()*0.06)
    return (width_from_left, height_from_top)

  def writeText(self, draw, pos, str, size):
    print(f"called writeText with {str}")
    print(f"write text size: {size}")
    fnt = self.getFont(size)
    try:
      draw.text(pos, str, fill=(0,0,0), font=fnt, align="center", anchor="mm")
    except Exception as e:
      print(e)

  def pasteQR(self, img: Image, qrimg):
    try:
      qrimg = qrimg.resize(self.getNewQRsize())
    except Exception as e:
      print("resize fail")
      print(e)
    try:
      img.paste(qrimg, self.getQRpos())
    except Exception as e:
      print("paste fail")
      print(e)

  def createImg(self, width, height):
    try:
      img = Image.new("RGB", (width, height), color=(250,250,250))
    except Exception as e:
      print(e)
    return img

  def getModelParts(self):
    model = self.getModel()
    size = self.getSizeForStr(model)
    parts = 1
    split = 0
    if size!=-1:
      return (size, parts, split)
    i = self.getSplitIndex(model)
    model_left = model[:i]
    model_right = model[i+1:]
    if len(model_left)>len(model_right):
      model = model_left
    else:
      model = model_right
    size = self.getSizeForStr(model)
    parts = 2
    split = i
    return (size, parts, split)

  def getSizeForStr(self, str):
    min_size = 14
    size = 42 #inital
    round_zero = 6
    maxwidth = round(self.getPixelInMM(self.getImgWidth()), round_zero)
    size_in_mm = round(self.getPointInMM(size), round_zero)
    string_len = len(str)
    total = round(string_len * size_in_mm, round_zero)
    while  total > maxwidth:
      size -= 1
      size_in_mm = round(self.getPointInMM(size), round_zero)
      total = round(string_len * size_in_mm, round_zero)
      print(f"maxwidth = {maxwidth}\n size={size}, size_mm = {size_in_mm}\n totalstring = {total}")
    if size>=min_size:
      return size
    print("string is too long")
    return -1 #string is too long

  def getPixelInMM(self, pixel):
    return pixel/38*10

  def getPixelFromMM(self, mm):
    return mm/10*38

  def getPointInMM(self, point):
    return point*0.22

  def getPointHeightInMM(self, point):
    return round(point/50*10,2)

  def getSplitIndex(self, str):
    i = self.getBestSpaceIndex(str)
    if i != -1:
      return i
    i = int(len(str)/2)
    return i

  def getBestSpaceIndex(self, str):
    spaces_indexes = []
    i = 0
    #find all spaces or - indexes
    for c in str:
      if ord(c) == ord(' ') or ord(c) == ord('-'):
        spaces_indexes.append(i)
      i += 1
    no_spaces = len(spaces_indexes)
    if no_spaces==0:
      return -1
    for space in spaces_indexes:
      left = str[:space]
      right = str[space+1:]
      if len(left) >= len(right) - 2 and len(left) <= len(right) + 2:
        return space
    return spaces_indexes[no_spaces-1] #there's no almost equal-splitting space index, so return last index

  def writeModelByParts(self, draw, brandsize):
    size, parts, split = self.getModelParts()
    model = self.getModel()
    if parts==2:
      model_left = model[:split]
      model_right = model[split:]
      self.writeText(draw, self.getModelPos(1, size, brandsize), model_left, size=size)
      self.writeText(draw, self.getModelPos(2, size, brandsize), model_right, size=size)
    else:
      self.writeText(draw, self.getModelPos(1, size, brandsize), model, size=size)

  def writeBrand(self, draw):
    brand = self.getBrand()
    print("brand = " + brand)
    size = self.getSizeForStr(brand)
    print(f"size = {size}")
    if size==-1:
      size = 12
    self.writeText(draw, self.getBrandPos(), brand, size)  # write the brand in the image
    return size

# Define the function to generate the card image
  def getCard(self):
    print("called getCard")
    img = self.createImg(self.getImgWidth(), self.getImgHeight()) #create the image
    print("image created")
    self.drawOnImage(img) #imageInfo
    print("image drawen")
    #img = img.rotate(270)
    print("image rotated")
    return img

  def drawOnImage(self, img):
    try:
      draw = ImageDraw.Draw(img)
      print("draw object created")
      brandsize = self.writeBrand(draw) #writing to image and retrning the brand size
      print("brand on")
      self.writeModelByParts(draw, brandsize)  # write the Model in the image
      print("model on")
    except Exception as e:
      print(e)
    self.pasteQR(img, self.getQR())
    print("qr on")

"""
  def reformat(self, input):
    if len(input):
      return input
    i = self.getSpaceIndex(input)
    if i == -1: #there's no space in the name
      index = int(len(input)/2) #cut the name in the middle
      return self.insertBreakLine(input, index, space=False)
    return self.insertBreakLine(input, i)

  def getSpaceIndex(self, str):
    length = len(str)
    if length > 8:
      try:
        i = input.rindex(" ")
      except Exception as e: #method rindex returns error if index not found
        print(e)
        i = -1
    else:
      i = input.index(" ")
    return i

  def insertBreakLine(self, str, index, space=True):
    str_break = ""
    count = 0
    for c in str:
      if count == index:
        if not space:
          c = c + "\n"
        else:
          c = "\n"
      str_break = str_break + c
      count += 1
    return str_break
    """
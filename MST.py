import numpy as np
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageFilter, ImageEnhance


# DISJOINT SET FIND FUNCTION
def Find(par, node):
    if par[node] == node:
        return node
    else:
        par[node] = Find(par, par[par[node]])
        return par[node]


# DISJOINT SET UNION FUNCTION
def Union(par, node1, node2):
    par[Find(par, node2)] = Find(par, node1)


# FUNCTION TO CALCULATE DIFFERENCE IN RGB VALUES OF TWO PIXELS
# USING SQUARED EUCLIDEAN DISTANCE FORMULA
def RGBDifference(pixels, p1, p2):
    dr = (int(pixels[p1[0]][p1[1]][0]) - int(pixels[p2[0]][p2[1]][0]))
    dg = (int(pixels[p1[0]][p1[1]][1]) - int(pixels[p2[0]][p2[1]][1]))
    db = (int(pixels[p1[0]][p1[1]][2]) - int(pixels[p2[0]][p2[1]][2]))
    return dr * dr + dg * dg + db * db


# FUNCTION TO SET IMAGE BACKGROUND TO WHITE
def mstThreshold(image, threshold=200, innerRadius=0, outerRadius=2):
    # CONVERTING IMAGE TO ARRAY OF PIXELS
    pixels = np.array(image)

    # STORING OLD PIXEL VALUES
    oldPixels = pixels

    # INITIALIZING DIMENSIONS AND CALCULATING TOTAL NO OF PIXELS
    imageHeight = pixels.shape[0]
    imageWidth = pixels.shape[1]
    pixelCount = imageHeight * imageWidth

    # INITIALLIZING ARRAY TO STORE EDGES
    edges = np.zeros(pixelCount * outerRadius * 2, 'int32, int32, int32')
    i = 0

    # USING DOUBLE LOOP LOOPING OVER ALL PIXELS ONE BY ONE
    for r in range(0, imageHeight):
        for c in range(0, imageWidth):
            # FIRST PIXEL TO FORM ANY EDGE
            j = r * imageWidth + c

            # NOW WE FORM EDGE BETWEEN FIRST PIXEL AND PIXELS WHICH ARE IN RANGE OF INEER AND      #OUTER RADIUS AND WHICH ARE ON LEFT OR UPPER SIDE OF FIRST PIXEL
            for d in range(innerRadius, outerRadius):
                if r > d:
                    jup = (r - d - 1) * imageWidth + c
                    edges[i] = (j, jup, RGBDifference(pixels, (r, c), (r - d - 1, c)))
                    i += 1

                if c > d:
                    jleft = r * imageWidth + c - d - 1
                    edges[i] = (j, jleft, RGBDifference(pixels, (r, c), (r, c - d - 1)))
                    i += 1

    np.resize(edges, i)

    # KRUSKAL'S MST ALGORITHM WITH THRESHOLD TO FIND MINIMUM SPANNING FORESTS
    edges = np.array(sorted(edges, key=lambda x: x[2]))

    # WE INITIALLIZE PARENT ARRAY
    parent = np.arange(0, pixelCount)

    mergedCount = 0

    for i in range(0, edges.size):
        # IF EDGE WEIGHT GREATER THAN THRESHOLD WE BREAK THE LOOP
        if edges[i][2] > threshold:
            break
        # ELSE WE INCLUDE EDGE IN MINIMUM SPANNING TREE UPDATE PARENT ARRAY
        if Find(parent, edges[i][0]) != Find(parent, edges[i][1]):
            Union(parent, edges[i][0], edges[i][1])
            mergedCount += 1

    # CALCULATE SUM AND FREQUENCY OF PIXELS FOR EACH SEGMENT
    colorCount = {};
    maxFreq = -1

    for i in range(0, pixelCount):

        # LOCATE PIXEL
        r = i // imageWidth
        c = i % imageWidth

        # FIND ROOT ELEMENT ASSOCIATED WITH SEGMENT OF WHICH THAT PIXEL IS PART OF
        root = Find(parent, i)

        # INCREASE THE PIXEL COUNT OF PIXELS SEGMENT
        colorCount[root] = colorCount.get(root, 0) + 1

        # IF PIXELS SEGMENT IS GREATER THAN MAXIMUM FREQUENCY SEGMENT THEN MAKE IT #MAXIMUM FREQUENCY SEGMENT
        if maxFreq == -1 or colorCount[root] > colorCount[maxFreq]:
            maxFreq = root

    # ASSIGN WHITE COLOUR TO PIXELS OF MAXIMUM FREQUENCY SEGMENT AND OLD COLOUR TO OTHER #PIXELS
    for i in range(0, pixelCount):
        r = i // imageWidth
        c = i % imageWidth
        root = Find(parent, i)

        if root == maxFreq:
            pixels[r][c][0] = 255
            pixels[r][c][1] = 255
            pixels[r][c][2] = 255
        else:
            pixels[r][c][0] = oldPixels[r][c][0]
            pixels[r][c][1] = oldPixels[r][c][1]
            pixels[r][c][2] = oldPixels[r][c][2]

    print('TOTAL PIXELS IN IMAGE : ', pixelCount)
    print('TOTAL EDGES FORMED : ', edges.size)
    print('TOTAL EDGES MERGED : ', mergedCount)
    print('TOTAL SEGMENTS FORMED : ', pixelCount - mergedCount)

    # ARRAY OF PIXELS TO IMAGE AGAIN
    return Image.fromarray(pixels)


# MAIN PROGRAM

root = Tk()
root.title("DAA MINI PROJECT")
root.iconbitmap("C:/Users/DELL/Desktop/favicon.ico")
imPath = filedialog.askopenfilename(initialdir="C:/Users/DELL/Desktop", title="Select A File",
                                    filetypes=(("jpg files", "*.jpg"), ("all files", "*.*")))

# PARAMETERS
# IMAGE FILE MUST BE IN RGB COLOR FORMAT, RECOMMENDED SIZE IS BETWEEN 200X200 TO 800X800 PIXELS

im = Image.open(imPath)

# SENSITIVITY TO COLOR DIFFERENCES, A HIGHER THRESHOLD WILL TOLERATE MORE DIFFERENCES
threshold = 150

# RADIUS IN WHICH NEIGHBORING PIXELS WILL BE CONSIDERED
innerRadius = 0
outerRadius = 5

print('Source image: ', imPath)
print(im.format, im.size, im.mode)
print('Segmentation threshold: ', threshold)
print('Inner/outer radius: ', innerRadius, outerRadius)

# FUNCTION TO TURN BACKGROUND WHITE
im = mstThreshold(im, threshold, innerRadius, outerRadius)

# SHOW RESULT IMAGE
im.show()


import logging
import os
import time

class ConsoleScreen:

    def __init__(self, dimensions=(50, 50), fontSize=2):
        #changeFontSize(fontSize)

        self.width, self.height = dimensions
        os.system(f'mode con: cols={self.width+4} lines={self.height+4}')
        self.background = u"\u2591"
        self.shade = {
            "light": u"\u2591",
            "medium": u"\u2592",
            "dark": u"\u2593",
            "full": u"\u2588",
            "X": "X",
            "x": "x"
        }
        self.pixel = self.shade["full"]

        self.field = [[self.background for x in range(self.width)] for y in range(self.height)]
        logging.basicConfig(filename='ConsoleScreen.log', level=logging.INFO, filemode='w')

    def clearField(self):
        self.field = [[self.background for x in range(self.width)] for y in range(self.height)]

    def clearScreen(self):
        os.system('clear')

    def clear(self):
        self.clearScreen()
        self.clearField()

    def roundPoint(self, p, r=0):
        return tuple([int(round(x, r)) for x in p])
    
    flatten = lambda self, t: [item for sublist in t for item in sublist]
    
    def mapFunc(self, value, start1, stop1, start2,
                stop2):  # Maps a value from a range ont another value from a different range
        return start2 + (stop2 - start2) * ((value - start1) / (stop1 - start1))

    def getShade(self, value):
        return [" ", u"\u2591", u"\u2592", u"\u2593", u"\u2588"][
            round(self.mapFunc(value, 255, 0, 0, 4))]

    def onScreen(self, pixel):
        if 0 < pixel[0] < self.width and 0 < pixel[1] < self.height:
            return True
        return False

    def drawPixel(self, xy, shade=u"\u2588"):
        if self.onScreen(xy):
            self._drawPixel(xy, shade)

    def _drawPixel(self, xy, shade=u"\u2588"):
        x, y = xy
        self.field[round(y)][round(x)] = shade

    def drawLine(self, p1, p2, shade=u"\u2588", draw=True):
        p1 = self.roundPoint(p1)
        p2 = self.roundPoint(p2)

        x0, y0 = p1
        x1, y1 = p2

        line = []

        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        x, y = x0, y0
        sx = -1 if x0 > x1 else 1
        sy = -1 if y0 > y1 else 1
        if dx > dy:
            err = dx / 2.0
            while x != x1:
                line.append((x, y))
                err -= dy
                if err < 0:
                    y += sy
                    err += dx
                x += sx
        else:
            err = dy / 2.0
            while y != y1:
                line.append((x, y))
                err -= dx
                if err < 0:
                    x += sx
                    err += dy
                y += sy
        line.append((x, y))

        line = list(set(line))
        if draw:
            for c in line:
                self.drawPixel(c, shade)
        return line

    def drawTriangle(self, triangle, fill=False, shade=u"\u2588"):
        l1 = self.drawLine(triangle[0], triangle[1], shade)
        l2 = self.drawLine(triangle[1], triangle[2], shade)
        l3 = self.drawLine(triangle[2], triangle[0], shade)

    def drawCircle(self, xy, r, shade=False, draw=True):  # Draws circle with radius "r" from midpoint "xy".
        xc, yc = xy
        coords = []

        def drawC(xc, yc, x, y):
            coords.append((xc + x, yc + y))
            coords.append((xc - x, yc + y))
            coords.append((xc + x, yc - y))
            coords.append((xc - x, yc - y))
            coords.append((xc + y, yc + x))
            coords.append((xc - y, yc + x))
            coords.append((xc + y, yc - x))
            coords.append((xc - y, yc - x))

        x = 0
        y = r
        d = 3 - 2 * r
        drawC(xc, yc, x, y)
        while y >= x:
            x += 1
            if (d > 0):
                y -= 1
                d = d + 4 * (x - y) + 10
            else:
                d = d + 4 * x + 6
            drawC(xc, yc, x, y)
            # drawC(xc, yc, zc, x+1, y)
            # drawC(xc, yc, zc, x-1, y)

        if draw:
            for c in coords:
                self.drawPixel(c, shade=shade)
        return coords

    def display(self, border=False):
        try:
            if border:
                filledLines = "".join([border for n in range(self.width + 2)])
                everythingElse = "\n".join([border + "".join(self.field[n]) + border for n in range(len(self.field))])
                print(filledLines + "\n" + everythingElse + "\n" + filledLines)
            else:
                print("\n".join(["".join(r) for r in self.field]))
        except Exception as e:
            logging.error("Failed Printing Field")
            logging.error(str(e))
    
    def getValue(self, px):
        if px in [" ", u"\u2591", u"\u2592", u"\u2593", u"\u2588"]:
            index = [" ", u"\u2591", u"\u2592", u"\u2593", u"\u2588"].index(px)
            value = int(self.mapFunc(index, 0, 5, 0, 255))
            return (value, value, value)
        else:
            return (255,255,255)
        
    def displayToPicture(self, name="display.png"):
        print("Saving Image!")
        values = [" ", u"\u2591", u"\u2592", u"\u2593", u"\u2588"]
        newPic = []
        
        for px in self.flatten(self.field):
            value = self.getValue(px)
            newPic.append(value)
        
        t1 = time.time()
        from PIL import Image
        
        im = Image.new("RGB", (self.width,self.height))
        im.putdata(newPic)
        im.save(name)
        

        
        
if __name__ == "__main__":
    f = ConsoleScreen()
    #t = time.time()
    f.drawTriangle(((40, 6), (300, 50), (3, 120)), fill=False)
    #print(time.time()-t)
    # f.drawLine((0, 0), (948, 506))
    #f.drawBigPixel((10, 10), 30)
    #f.display(f.shade["full"])
    f.display()
    input("[DONE!]")
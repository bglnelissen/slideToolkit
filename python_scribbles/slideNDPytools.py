#!/usr/bin/env python
#
# Ref: https://github.com/fepegar/ndPytools/blob/master/ndpitools.py
#

import os
import re
import shutil
import subprocess
from subprocess import Popen, PIPE, STDOUT

import numpy as np

NUMBER_OF_MAGNIFICATIONS = 5
MAX_TILE_SIZE = 20000  # 20000*20000*3 = 1.2 GB RAM
COMPRESSION_NONE = 'n'
COMPRESSION_JPEG = 'j'

class NDPI:

    def __init__(self, filepath, debug=False):
        if not filepath.endswith('.ndpi'):
            raise IOError(os.path.basname(filepath) + ' is not an NDPI file.')
        elif not os.path.exists(filepath):
            raise IOError(filepath + ' does not exist.')
        else:
            self.filepath = filepath
            self.readInfoFromHeader()
        self.commandLine = []
        self.debug = debug


    def __repr__(self):
        s = ['Nanozoomer Digital Pathology Image']
        s.append(' Source lens: x%d' % self.sourceLens)
        s.append(' Size: %d x %d pixels' % (self.size[0], self.size[1]))
        s.append(' Resolution: %d x %d pixels/cm2' % (self.resolution[0], self.resolution[1]))
        s.append(' Pixel spacing: %.3f x %.3f nm' % (self.spacing[0]*1e6, self.spacing[1]*1e6))
        return '\n'.join(s)


    def readInfoFromHeader(self):
        cmd = ['tifftopnm', '-headerdump', self.filepath]
        process = Popen(cmd, stdout=PIPE, stderr=STDOUT)
        text = process.communicate()[0]

        pattern = r'Image Width: (\d+) Image Length: (\d+)'
        numbersStrings = re.findall(pattern, text)
        self.size = np.array([int(n) for tup in numbersStrings for n in tup])

        pattern = r'Tag 65421: (\d+)'
        numbersStrings = re.findall(pattern, text)
        self.sourceLens = int(numbersStrings[0])
        self.magnifications = [self.sourceLens/4.**i for i in range(NUMBER_OF_MAGNIFICATIONS)]
        self.magnifications = [int(x) if x%1 == 0 else x for x in self.magnifications]  # E. g. 20.0 -> 20

        pattern = r'Resolution: (\d+), (\d+) pixels/cm'
        numbersStrings = re.findall(pattern, text)
        resolution = np.array([int(n) for tup in numbersStrings for n in tup])
        self.resolution = resolution
        self.spacing = 10./resolution  # 10 mm


    def getMagnificationsString(self):
        s = ['x%s'%n for n in self.magnifications]
        return ', '.join(s)


    def split(self, magnifications=[], outputPath=None, compression=COMPRESSION_JPEG, run=True):
        commandLine = ['ndpisplit']
        if magnifications:
            if not isinstance(magnifications, list):
                magnificationsString = '-x' + str(magnifications)
            else:
                magnificationsString = '-x'
                for magnification in magnifications:
                    magnificationsString += str(magnification) + ','

            commandLine.append(magnificationsString.strip(','))
        commandLine.append('-c' + compression)
        commandLine.append(self.filepath)
        self.commandLine = commandLine
        if run:
            self.run()
            tiffPath = self.getMagnificationFilepath(magnifications)
            if outputPath is None:  # we suppose there is only one magnification
                outputPath = tiffPath
            else:
                src, dst = tiffPath, outputPath
                if os.path.exists(src):
                    shutil.move(src, dst)
            return outputPath


    def extractROI(self, magnification, topLeftX, topLeftY, width, height, outputPath=None, compression=COMPRESSION_JPEG, run=True):
        if magnification not in self.magnifications:
            raise ValueError('Magnification x%s is not available. Choose between the following: %s' % (magnification, self.getMagnificationsString()))
        magnificationSize = self.getSize(magnification)
        inX = topLeftX < magnificationSize[0] and width <= magnificationSize[0] and (topLeftX + width) <= magnificationSize[0] + 1
        inY = topLeftY < magnificationSize[1] and height <= magnificationSize[1] and (topLeftY + height) <= magnificationSize[1] + 1

        commandLine = ['ndpisplit']
        options = '-Ex%s,%d,%d,%d,%d' % (str(magnification), topLeftX, topLeftY, width, height)
        commandLine.append(options)
        commandLine.append('-c' + compression)
        commandLine.append(self.filepath)
        # print magnificationSize
        # print topLeftX, topLeftY, width, height
        # print commandLine
        # print inX
        # print inY
        if not (inX and inY):
            raise ValueError('Wrong ROI size. The image size for this magnification is %s.' % self.getSizeString(magnificationSize))
        self.commandLine = commandLine
        if run:
            self.run()
            roiPath = self.getROIFilepath(magnification)
            if outputPath is None:
                return roiPath
            else:
                src, dst = roiPath, outputPath
                if os.path.exists(src):
                    shutil.move(src, dst)
                    return dst


    def getSizeString(self, size):
        return '%d x %d' % (size[0], size[1])


    def getAffine(self, magnification=None, sz=0.05, oz=0):
        if magnification is None:
            magnification = self.sourceLens
        sx, sy = self.getSpacing(magnification)
        affine = np.diag([sx, sy, sz, 1])
        affine[2, 3] = oz
        sizeX, sizeY = self.getSize(magnification)
        affine[0, 3] = sizeX * sx
        affine[0, 0] *= -1
        return affine


    def extractROIFromFile(self, acsvPath, magnification=None, outputDir=None, prefix=None, oz=0, flipX=False, flipY=False, removeTIFF=True, makeNifti=True):
        roiCenterWorld, roiSizeWorld = acsv.ROI(acsvPath).getCenterAndSize()
        self.extractROIFromCenterAndSize(roiCenterWorld, roiSizeWorld, magnification=magnification, outputDir=outputDir, prefix=prefix, oz=oz, flipX=flipX, flipY=flipY, removeTIFF=removeTIFF, makeNifti=makeNifti)


    def extractROIFromCenterAndSize(self, roiCenterWorld, roiSizeWorld, magnification=None, outputDir=None, prefix=None, oz=0, flipX=False, flipY=False, removeTIFF=True, makeNifti=True):
        import nibabel as nib
        import acsv
        import utils

        if magnification is None:
            magnification = self.sourceLens
        ijk2ras = self.getAffine(magnification)

        ras2ijk = np.linalg.inv(ijk2ras)
        roiCenterPixel = nib.affines.apply_affine(ras2ijk, roiCenterWorld)
        sx, sy, sz, _ = np.diag(ijk2ras)
        roiSizePixel = np.abs(roiSizeWorld / np.array((sx, sy, sz)))

        topLeft = np.round(roiCenterPixel - roiSizePixel/2).astype(int)
        topRight = np.round(roiCenterPixel + roiSizePixel/2).astype(int)
        topRightX = topRight[0]
        topLeftX, topLeftY, _ = topLeft
        width, height, _ = np.round(roiSizePixel).astype(int)

        if flipX:
            topLeftX = self.flip(topRightX, 0, magnification)
            topRightX = self.flip(topLeftX, 0, magnification)
        if flipY:
            topLeftY = self.flip(topLeftY, 1, magnification) - height


        numTilesX = width / MAX_TILE_SIZE + 1
        numTilesY = height / MAX_TILE_SIZE + 1
        numTiles = numTilesX * numTilesY

        tileWidth = width / numTilesX
        tileHeight = height / numTilesY

        if outputDir is None:
            outputDir = os.path.dirname(self.filepath)
        if prefix is None:
            prefix = os.path.splitext(os.path.basename(self.filepath))[0]

        for tileY in range(numTilesY):
            for tileX in range(numTilesX):
                tileTopLeftX = topLeftX + tileX*tileWidth
                tileTopLeftY = topLeftY + tileY*tileHeight
                tileTopRightX = tileTopLeftX + tileWidth - 1

                if flipX:
                    tileColumn = numTilesX - tileX - 1
                else:
                    tileColumn = tileX

                if flipY:
                    tileRow = numTilesY - tileY - 1
                else:
                    tileRow = tileY

                if numTiles == 1:
                    outputPath = os.path.join(outputDir, prefix + '.tif')
                else:
                    outputPath = os.path.join(outputDir, prefix + '_tile_%d_%d.tif' % (tileRow, tileColumn))

                utils.ensureDir(outputPath)
                roiPath = self.extractROI(magnification, tileTopLeftX, tileTopLeftY, tileWidth, tileHeight, outputPath=outputPath)

                if makeNifti:
                    import ImageUtils as iu
                    roiAffine = ijk2ras[:]
                    roiAffine[:3, :3] = np.abs(roiAffine[:3, :3])
                    roiAffine[0, 3] = self.flip(tileTopRightX, 0, magnification) * roiAffine[0, 0]
                    roiAffine[1, 3] = tileTopLeftY * roiAffine[1, 1]

                    if flipX:
                        roiAffine[0, 0] *= -1
                        roiAffine[0, 3] = abs(roiAffine[0, 0]) * (tileTopLeftX + tileWidth)
                    if flipY:
                        roiAffine[1, 1] *= -1
                        roiAffine[1, 3] = abs(roiAffine[1, 1]) * self.flip(tileTopLeftY, 1, magnification)

                    roiAffine[2, 3] = oz
                    iu.histologyImageToNiftiRGB(roiPath, affine=roiAffine)

                if removeTIFF:
                    os.remove(roiPath)


    def flip(self, n, dim, magnification=None):
        if magnification is None:
            magnification = self.getSourceLens()
        sizeDim = self.getSize(magnification)[dim]
        return sizeDim - n - 1


    def getMagnificationFilepath(self, magnification):
        base = os.path.splitext(self.filepath)[0]
        magPath = '{}_x{}_z0.tif'.format(base, magnification)
        return magPath


    def getROIFilepath(self, magnification):
        base = os.path.splitext(self.filepath)[0]
        magPath = '{}_x{}_z0_1.tif'.format(base, magnification)
        return magPath


    def getSize(self, magnification=None):
        if magnification is None:
            magnification = self.sourceLens
        return map(int, self.size / (self.sourceLens / magnification))


    def getSpacing(self, magnification=None):
        if magnification is None:
            magnification = self.sourceLens
        return self.spacing * (self.sourceLens / magnification)


    def getSourceLens(self):
        return self.sourceLens


    def getROISize(self, acsvPath):
        import acsv
        _, _, width, height = acsv.ROI(acsvPath).getCropValuesWorld()
        spacingX, spacingY = self.getSpacing()
        widthPixels = np.round(width / spacingX).astype(int)
        heightPixels = np.round(height / spacingY).astype(int)
        return widthPixels, heightPixels


    def getROIMemory(self, acsvPath):
        widthPixels, heightPixels = self.getROISize(acsvPath)
        numPixels = widthPixels * heightPixels
        numBytes = numPixels * 3
        if numBytes > 1e9:
            print('%.3f' % (numBytes/1e9), 'GB')
        else:
            print('%d' % (numBytes/1e6), 'MB')


    def getSplitRatio(self, remove=True):
        import ImageUtils as iu
        lowestMagnification = self.magnifications[-2]  # Sometimes the lowest magnification image is truncated
        imgPath = self.split(lowestMagnification, compression=COMPRESSION_NONE)
        splitRatio = iu.getSplitLeftRightColumnRatio(imgPath)
        if remove:
            os.remove(imgPath)
        return splitRatio


    def printCommandLine(self):
        print(' '.join(self.commandLine))


    def run(self):
        if self.debug:
            print('Running:')
            self.printCommandLine()
        subprocess.call(self.commandLine)


def getSplitRatio(filepath, remove=True):
    ndpiFile = NDPI(filepath)
    return ndpiFile.getSplitRatio(remove=remove)

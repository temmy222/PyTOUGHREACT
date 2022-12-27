import os
import shutil
import itertools


class SynergyUtilitiesToughReact(object):
    # takes in file names as a list
    """
    This class prepares the output files from TOUGHREACT for plot visualizations and analysis
    """

    def __init__(self, location, word, file2='MESH'):

        """
        An instance of this class takes in five parameters the last of which is optional;

        location --> the current direction where the simulations have been carried out
        destination ---> the directory containing PYTOUGH and its class which would be needed for
        manipulations
        filenames -> the result files to be transferred to the destination folder
        word --> the word where the truncation in the MESH file is to begin. Typically this should be 'CONNE'
        """

        self.location = location
        self.word = word
        self.file2 = file2

    def copyfile(self, filename, destination):

        """
        This method copies single file from the location to the destination folder. it takes in a a single argument

        filename -> the name of the file to be transferred
        """
        # copy specific file
        src_files = os.listdir(self.location)
        for file_name in src_files:
            if file_name == filename:
                full_file_name = os.path.join(self.location, file_name)
                if (os.path.isfile(full_file_name)):
                    shutil.copy(full_file_name, destination)

    def copyallfiles(self, filenames):

        """
        This method copies all files given in the instance of the class to the destination folder. It makes use
        of the copyfile() method in achieving this


        """
        # copy all files
        for i in range(0, len(filenames)):
            a = filenames[i]
            self.copyfile(a)
        print('...copying files...')

    def findword(self):

        """
        This method finds the word where the truncation of the MESH file is to occur
        """
        # find the position of a word
        with open(self.file2) as myFile:
            for num, line in enumerate(myFile, 1):
                if self.word in line:
                    point1 = num
                    return point1
        myFile.close()

    def sliceofffile(self):

        """
        This method slices off all parameters below the word stated in the instance of the class
        """
        #        os.remove("test2.txt")
        f = open("test2.txt", "w+")
        f.close()
        f = open("test.txt", "w+")
        f.close()
        f = open('test2.txt', 'r+')
        f.truncate(0)
        f.close()
        os.remove("test.txt")
        point1 = self.findword()
        with open("test2.txt", "w") as f1:
            with open(self.file2, "r") as text_file:
                for line in itertools.islice(text_file, 1, point1 - 2):
                    f1.write(line)
        f1.close()

    def sliceoffline(self):
        """
        This method slices off all grid parameter such as the volume, distance betweeen grids as stated in
        the TOUGHREACT flow.inp file

        The aim of the findword(), sliceofffile() and this method is to provide us with a list of all gridblocks
        in the simulation
        """
        self.sliceofffile()
        with open('test2.txt') as thefile:
            lines = thefile.readlines()
            mes = []
            for i in range(0, len(lines)):
                a = lines[i]
                b = a[0:5]
                mes.append(b)

        return mes
        thefile.close()

    def writetofile(self):
        """
        This method writes all gridblocks to a separate file called 'test.txt' for easy location and onward
        manipulations
        """
        mesh = self.sliceoffline()
        with open("test.txt", "w") as f1:
            for item in mesh:
                f1.write("%s\n" % item)
        f1.close()

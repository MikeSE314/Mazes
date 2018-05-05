from __future__ import print_function

import os
import random
import time

class Cell:
    def __init__(self, set_, right=False, left=False, top=False, bottom=False):
        self.right_open = right
        self.left_open = left
        self.top_open = top
        self.bottom_open = bottom
        self.set = set_

    def printSelf(self):
        print("  ", end="")
        if not self.right_open:
            print("|", end="")
        else:
            print(" ", end="")

    def printBelow(self):
        if not self.bottom_open:
            print("__", end="")
        else:
            print("  ", end="")
        if not self.right_open:
            print("|", end="")
        elif not self.bottom_open:
            print("_", end="")
        else:
            print(" ", end="")

    def setSet(self, set_):
        self.set = set_

    def getSet(self):
        return self.set

    # ===RIGHT===

    def openRight(self):
        self.right_open = True

    def toggleRight(self):
        self.right_open = not self.right_open

    def getRight(self):
        return self.right_open

    # ===LEFT===

    def openLeft(self):
        self.left_open = True

    def toggleLeft(self):
        self.left_open = not self.left_open

    def getLeft(self):
        return self.left_open

    # ===TOP===

    def openTop(self):
        self.top_open = True

    def toggleTop(self):
        self.top_open = not self.top_open

    def getTop(self):
        return self.top_open

    # ===BOTTOM===

    def openBottom(self):
        self.bottom_open = True

    def toggleBottom(self):
        self.bottom_open = not self.bottom_open

    def getBottom(self):
        return self.bottom_open

class Row:
    def __init__(self):
        self.lastRow = []
        self.currentRow = []
        self.nextRow = []
        self.PROBABILITY = 0.5
        self.sets = []

    def addCell(self, c=None):
        if c:
            self.currentRow.append(c)
        else:
            possible = range(len(self.currentRow) + 1)
            for cell in self.currentRow:
                if cell.getSet() in possible:
                    possible.remove(cell.getSet())
            self.currentRow.append(Cell(possible[0]))

    def addCellNextRow(self, c=None):
        if c:
            self.nextRow.append(c)
        else:
            possible = range(len(self.currentRow) + 1)
            for cell in self.currentRow:
                if cell.getSet() in possible:
                    possible.remove(cell.getSet())
            for cell in self.nextRow:
                if cell.getSet() in possible:
                    possible.remove(cell.getSet())
            self.nextRow.append(Cell(possible[0]))

    def printTop(self):
        print("_", end="")
        for cell in self.currentRow:
            print("___", end="")
        print("")

    def printRow(self):
        print("|", end="")
        for cell in self.currentRow:
            cell.printSelf()

    def printBelow(self):
        print("|", end="")
        for cell in self.currentRow:
            cell.printBelow()

    def join(self):
        for i in range(len(self.currentRow) - 1):
            if random.random() < self.PROBABILITY and \
                    self.currentRow[i].getSet() != \
                    self.currentRow[i + 1].getSet():
                self.currentRow[i].openRight()
                self.currentRow[i + 1].openLeft()
                getVal = self.currentRow[i].getSet()
                setVal = self.currentRow[i + 1].getSet()
                for cell in self.currentRow:
                    if cell.getSet() == setVal:
                        cell.setSet(getVal)

    def openBottoms(self):
        self.sets = []
        for cell in self.currentRow:
            self.sets.append(cell.getSet())
        for cell in self.currentRow:
            if self.sets.count(cell.getSet()) == 1 or \
                    random.random() < self.PROBABILITY:
                cell.openBottom()
            elif cell.getSet() in self.sets: # if it doesn't get removed,
                self.sets.remove(cell.getSet()) # make sure the next one does.

    def repopulate(self):
        for cell in self.currentRow:
            if cell.getBottom():
                self.nextRow.append(Cell(cell.getSet(), top=True))
            else:
                self.addCellNextRow()

    def openBottom(self, index):
        self.currentRow[index].openBottom()

    def openRight(self, index):
        self.currentRow[index].openRight()

    def openLeft(self, index):
        self.currentRow[index].openLeft()

    def openTop(self, index):
        self.currentRow[index].openTop()

    def step(self):
        self.lastRow = self.currentRow
        self.currentRow = self.nextRow
        self.nextRow = []

def main(m):
    mainRow = Row()
    for i in range(m):
        mainRow.addCell()
    mainRow.printTop()
    while True:
        mainRow.join()
        mainRow.openBottoms()
        mainRow.repopulate()
        mainRow.printRow()
        print("")
        mainRow.printBelow()
        mainRow.step()
        if raw_input() == "q":
            quit()

if __name__ == "__main__":
    m = 15
    if len(os.sys.argv) > 1:
        m = int(os.sys.argv[1])
    main(m)


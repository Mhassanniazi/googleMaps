

class readFile:
    def __init__(self):
        self.number = []
        self.category = []
        self.links = []

    def fileText(self):
        with open("reviews.txt") as file:
            for item in file:
                values = item.split(';')
                self.number.append(values[0])
                self.category.append(values[1])
                self.links.append(values[2])
            return self.category, self.links

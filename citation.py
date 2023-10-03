class Citation:
    key = ""
    title = ""
    year = 0

    # why when I capitalise here, am I getting less matches - surely I should get more!?

    def __hash__(self):
        return hash(str(self.key))

    def __eq__(self, other):
        #comparisons are case-sensitive in python
        return self.key.casefold() == other.key.casefold()
class UnexpectedLineError(Exception):
    def __init__(self, line):
        super(UnexpectedLineError, self).__init__('ERROR: Unexpected Line: ' + line)


class Author(object):
    """Simple class to store Git author's name and email."""

    def __init__(self, name='', email=''):
        self.name = name
        self.email = email

    def to_json(self):
        return {
            'name' : self.name,
            'email' : self.email,
        }
    
    def __str__(self):
        return "%s (%s)" % (self.name, self.email)

    def __eq__(self, other):
        return self.name == other.name and self.email == other.email


class CommitData(object):
    """Simple class to store Git commit data."""

    def __init__(self, commit_hash=None, author=Author(), message=None,
                 date=None, change_id=None, files_changed=0, insertions=0, deletions = 0):
        self.commit_hash = commit_hash
        self.author = author
        self.message = message
        self.commit_date = date
        # change id
        self.change_id = change_id
        self.files_changed = files_changed
        self.insertions = insertions
        self.deletions = deletions

    # creates a dictionary that represents the class, since the author is a multivalue field, is has to be converted separately
    def to_json(self):
        return{
            'commit_hash' : self.commit_hash,
            'author' : self.author.to_json(),
            'message' : self.message,
            'commit_date' : str(self.commit_date),
            'change_id' : self.change_id,
            'files_changed' : self.files_changed,
            'insertions' : self.insertions,
            'deletions' : self.deletions,
        }

    def __str__(self):
        return "%s;%s;%s;%s;%s;%s;%s;%s" % (self.commit_hash, self.author, self.message,
                                   str(self.commit_date), self.change_id,
                                   self.files_changed, self.insertions, self.deletions)
    

    def __eq__(self, other):
        if isinstance(other, CommitData):
            return (self.commit_hash == other.commit_hash 
                and self.author == other.author 
                and self.message == other.message 
                and str(self.commit_date) == str(other.commit_date) 
                and self.change_id == other.change_id
                and self.files_changed == other.files_changed
                and self.insertions == other.insertions
                and self.deletions == other.deletions)
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
                 date=None, change_id=None):
        self.commit_hash = commit_hash
        self.author = author
        self.message = message
        self.commit_date = date
        # change id
        self.change_id = change_id

    # creates a dictionary that represents the class, since the author is a multivalue field, is has to be converted separately
    def to_json(self):
        return{
            'commit_hash' : self.commit_hash,
            'author' : self.author.to_json(),
            'message' : self.message,
            'commit_date' : str(self.commit_date),
            'change_id' : self.change_id,
        }

    def __str__(self):
        return "%s;%s;%s;%s;%s" % (self.commit_hash, self.author, self.message,
                                   str(self.commit_date), self.change_id)
    

    def __eq__(self, other):

        return (self.commit_hash == other.commit_hash 
            and self.author == other.author 
            and self.message == other.message 
            and self.commit_date == other.commit_date 
            and self.change_id == other.change_id)
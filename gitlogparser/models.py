class Author(object):
    """Simple class to store Git author's name and email."""

    def __init__(self, name='', email=''):
        self.name = name
        self.email = email

    def __str__(self):
        return "%s (%s)" % (self.name, self.email)


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

    def __str__(self):
        return "%s;%s;%s;%s;%s" % (self.commit_hash, self.author, self.message,
                                   str(self.commit_date), self.change_id)
__author__ = 'awhite'


class GenericPage:
    """
    A generic page handler whose purpose is to serve as a base class for all underlings such as
    those that might be specified in the configuration file.
    """
    content_type = "text/plain"
    #plaintext

    def __init__(self, serv):
        """
        INitialize a GenericPage object
        @param serv: The server for accessing the database or configuration file.
        @return: A GenericPage object
        """
        self.master = serv

    def retrieve(self, title):
        """
        Retrieve the page generated by the class
        @param title: the title presumably for HTML purposes only
        @return: Any kind of object with __str__ defined.
        """
        return title
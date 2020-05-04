

class ElementsError(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0];
        else:
            self.message = None;

    def __str__(self):
        if self.message:
            return "{0}".format(self.message);
        else:
            # This should NEVER run, but just in case
            return "An error has occurred but unfortunately no further information is available";
    pass;


class ElementsConnectionError(ElementsError):
    """This is only here to add a more descriptive error name, will just pass up to ElementsError"""
    pass;

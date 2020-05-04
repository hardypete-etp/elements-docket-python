"""
.. module:: connect
   :platform: Unix, Windows
   :synopsis: Controls access to data through the Elements API.

.. moduleauthor:: Pete Harding <pete@elementstechnology.co.uk> and Paolo Sanchez Puccini <paolo@elementstechnology.co.uk>


"""

from __future__ import absolute_import


class Connection(object):
    """
    Connection manages the interface between the client and server in a simple
    (hopefully) and robust manner.
    """
    from . import error as _elerror # Will this work once it is installed as a package?
    # import as _* so keep the autocompletes clean, will hide these imports from the user
    import requests as _req
    import json as _json
    import datetime as _datetime

    # Likewise, getters and setters will mean that we don't need to expose these
    _apikey = None;
    # This would only be used by us anyway, I think
    _URL='https://api.elements.technology/externalapi.php'


    def __init__(self, apikey = None):
        """
        Construct new Connection object,


        :param apikey: [optional] Client API key generated from the elements dashboard
        :type apikey: str
        :return: None -- Returns nothing, run implicitly

        :raises:
            ElementsConnectionError
            ElementsError

        """
        self._apikey = apikey;


    def setapikey(self, apikey):
        """
        Sets the API key to be used for connections

        :param apikey: [required] Client API key generated from the elements dashboard
        :return: None -- Returns nothing

        :raises:

        """
        self._apikey = apikey;


    def checkapikey(self):
        """
        Checks the API key supplied is valid, and that this should allow data to be retrieved

        :param None:
        :return: Boolean

        :raises:
            ElementsConnectionError:  No API key has been set
        """
        # Should maybe check that the string is valid b64 before going any further, as there is no point checking a malformed key
        if(self._apikey is None):
            raise self._elerror.ElementsConnectionError("No API key is set.  Set API key before calling this function")
        else:
            return self.checkauth();


    def _getURL(self):
        return self._URL


    def _getelementsheaders(self):
        if(self._apikey is None):
            raise self._elerror.ElementsConnectionError("No API key is set.  Set API key before calling this function");
        else:
            return { 'Authorize' : self._apikey, 'Content-Type':'application/json'};


    def _getauthresultresponse(self,r):
        content = self._json.loads(r.content)
        if not 'auth' in content:
            raise self._elerror.ElementsConnectionError(content["message"])
        else:
            if 'result' in content['auth']:
                if content['auth']['result'] != "success":
                    raise self._elerror.ElementsConnectionError(content["message"])
                else:
                    return True
            else:
                raise self._elerror.ElementsConnectionError()

    def _getresultresponse(self, r):
        content = self._json.loads(r.content)

        if 'result' in content:
            result = content['result']
            if result == "fail":
                raise self._elerror.ElementsError(content["message"])
            else:
                return True
        else:
            return self.checkauth();

    def checkauth(self):
        """
        """
        if self._apikey is None:
            raise self._elerror.ElementsConnectionError("No API key is set.  Set API key before calling this function")
        else:
            r = self._req.post(
                self._getURL(),
                headers = self._getelementsheaders(),
                data = self._json.dumps({}),
                verify = True);
            if r.ok:
                if self._getauthresultresponse(r): # authorisation check
                    return True;

            else:
                raise self._elerror.ElementsConnectionError("Server not reachable.  Could not establish connection to elements server, check internet connection and try again.");


    ## function calls

    def _validate_dateformat(self, date_text):
        try:
            return self._datetime.datetime.strptime(date_text, '%Y-%m-%d')
        except ValueError as ve:
            raise ve;
        except Exception as e:
            raise e;

    def _getdataresponse (self,r):
        content = self._json.loads(r.content)
        if 'query' in content:
            query = content['query']
            if 'data' in query:
                return content['query']['data']
            else:
                return query
        else:
            print(content)


    def listtemplates(self):
        """
        Get a list with the dictionaries correspondent to each template. Each dictionary has the ID, name and description of the template

        :param None:
        :return: Returns a list.

        :raises:
            ElementsConnectionError: If API key is no valid, server cannot be found, etc.
            ElementsError:  Any other error
        """

        if not self.checkauth( ):
            return 'Authorization Check failed';

        json_request = self._json.dumps({"func":"listtemplates",
                                  "params":{}});

        r = self._req.post(
                  self._getURL(),
                  headers = self._getelementsheaders(),
                  data = json_request,
                  verify=True);

        if r.ok:
            return self._getdataresponse(r)
        else:
            return False


    def gettemplatefromid(self, id=None):
        """
        """
        if not self.checkauth():
            return 'Authorization Check failed'

        if isinstance(id,int) or isinstance(id,str):
            input_params={"templateid":id}
        else:
            print('Incorrect ID type')
            return

        json_request = self._json.dumps({"func":"gettemplatefromid",
                                        "params":input_params})
        r= self._req.post(
                  self._getURL(),
                  headers = self._getelementsheaders(),
                  data = json_request,
                  verify=True)
        if r.ok:
            query = self._getdataresponse(r)
            template_id_check=query['template_id']
            if template_id_check is None:
                print('Template ID not found')
                return False
            else:
                return query
        else:
            return False


    def getorderfromid(self, id = None):
        """
        Get an order information give its ID.

        :param id: template ID[required] unique ID indentifier assigned to a template once saved
        :return: Returns a list of all the subprocesses of an order given its ID or False otherwhise

        :raises:
            ElementsConnectionError: If API key is no valid, server cannot be found, etc.
            ElementsError:  Any other error
        """

        self.checkauth()

        if isinstance(id,int) or isinstance(id,str):
            input_params = { "orderid" : id }
        else:
            print ('Incorrect ID format')
            return False

        json_request = self._json.dumps({"func":"getorder",
                                        "params":input_params})
        r= self._req.post(
                  self._getURL(),
                  headers = self._getelementsheaders(),
                  data = json_request,
                  verify=True)
        if r.ok:
            query = self._getdataresponse(r)
            if not query:
                print('Order ID not found')
                return False
            else:
                return query;
        else:
            return False


    def getsnapshot(self,today=""):
        if( today == "" ):
            today = self._datetime.date.today().strftime('%Y-%m-%d');

        # Test Connection
        try:
            self.checkauth()
        except self._elerror.ElementsConnectionError as e:
            print("An ElementsConnectionException occurred with message:  {0}".format(e));
            return False;
        except Exception as e:
            print("An Exception occurred with message:  {0}".format(e));
            return False;

        if today:
            try:
                self._validate_dateformat(today)
                    # should raise an exeception
                # If the functions called raise exceptions, then we have to
                # deal with the exceptions here as well as when they are fired
                # within the function . . . I think
            except ValueError as e:
                print("Error in date format caused a ValueError: {}".format(e) );
                return False;
            except Exception as e:
                print("Error in date format caused an Exception: {}".format(e) );
                return False;

        input_params = { "date" : today }

        json_request = self._json.dumps({"func":"snapshot",
                                        "params":input_params})
        r = self._req.post(
                  self._getURL(),
                  headers = self._getelementsheaders(),
                  data = json_request,
                  verify=True)

        if r.ok:
            data = self._getdataresponse(r)
            if not data:
                print("Orders not found to the given date")
                return False
            else:
                return data
        else:
            return False

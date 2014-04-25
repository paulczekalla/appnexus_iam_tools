class Placement:
    def __init__(self, id, name, code, publisher_name, site_name, default_referrer_url, custom_categories):
        pass
        
    def setId(self, id):
        self._id = id
    
    def getId(self):
        return self._id

    _id = property(getId, setId)
    
    
    def setName(self, name):
        self._name = name
    
    def getName(self):
        return self._name

    _name = property(getName, setName)
    
    
    def setCode(self, code):
        self._code = code
    
    def getCode(self):
        return self._code

    _code = property(getCode, setCode)
    
    
    def setPublisherName(self, _publisher_name):
        self._publisher_name = publisher_name
    
    def getPublisherName(self):
        return self._publisher_name

    _publisher_name = property(getPublisherName, setPublisherName)
    
    
    def setSite_name(self, site_name):
        self._site_name = site_name
    
    def getSite_name(self):
        return self._site_name

    _site_name = property(getSite_name, setSite_name)
    
    
    def setDefault_referrer_url(self, default_referrer_url):
        self._default_referrer_url = default_referrer_url
    
    def getDefault_referrer_url(self):
        return self._default_referrer_url

    _default_referrer_url = property(getDefault_referrer_url, setDefault_referrer_url)
    
    
    def setCustom_categories(self, custom_categories):
        self._custom_categories = custom_categories
    
    def getCustom_categories(self):
        return self._custom_categories

    _custom_categories = property(getCustom_categories, setCustom_categories)
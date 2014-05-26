class Profile:
    def __init__(self, profile_id, country_targets, region_targets, city_targets, segment_group_targets):
        self._profile_id = profile_id
        self._country_targets = country_targets
        self._region_targets = region_targets
        self._city_targets = city_targets
        self._segment_group_targets = segment_group_targets

    def setId(self, profile_id):
        self._profile_id = profile_id

    def getId(self):
        return self._profile_id

    profile_id = property(getId, setId)
    
    
    def setCountry_Targets(self, country_targets):
        self._country_targets = country_targets
    
    def getCountry_Targets(self):
        return self._country_targets

    country_targets = property(getCountry_Targets, setCountry_Targets)


    def setRegion_targets(self, region_targets):
        self._region_targets = region_targets
    
    def getRegion_targets(self):
        return self._region_targets

    region_targets = property(getRegion_targets, setRegion_targets)


    def setCity_targets(self, city_targets):
        self._city_targets = city_targets
    
    def getCity_targets(self):
        return self._city_targets

    city_targets = property(getCity_targets, setCity_targets)

    
    def setSegment_group_targets(self, segment_group_targets):
        self._segment_group_targets = segment_group_targets
    
    def getSegment_group_targets(self):
        return self._segment_group_targets

    segment_group_targets = property(getSegment_group_targets, setSegment_group_targets)
import copy
from entity.placement import Placement

class PlacementCategoriesChecker:
    def __init__(self):
        pass

    def read_in_categories(self, placement, site_categories, all_categories):
        placement_cat_list = copy.deepcopy(site_categories)
                        
        if placement['content_categories'] is not None:
            for placement_cat in placement['content_categories']:
                placement_cat_list.append(placement_cat['name'])
                all_categories.add(placement_cat['name'])
                        
        return Placement(placement['id'], placement['name'], placement['code'], placement['publisher_name'], placement['site_name'], placement['default_referrer_url'], placement_cat_list)
from api.saved_search import SavedSearch
from api.filters import Filters
from data.defaults import Strings
import pytest


@pytest.mark.parametrize("name, name_expected", [(Strings.random(l=24), True), ("$"*128, False)])
@pytest.mark.parametrize("item_types", [['PSScene3Band']])
@pytest.mark.parametrize("__daily_email_enabled", [True, False])
@pytest.mark.parametrize("_filter", Filters.testable)
def test_create(name, name_expected, item_types, __daily_email_enabled, _filter):
    """Each of the specified parametrized lists could be expanded:
        Name: 
            Length: 0,1,63,64,65
            Validity: Allowed symbols vs many invalid options (special symbols, non strings, sql injections etc.)
            I used name as an example of a negative test, but all negative tests should be separated ito its own test.
        Item_Types:
            Was specified only one type PSScene3Band, could be expanded within that item type as it has many properties.
            (Although, item types and filter types should have dedicated tests to be able to cover the complexity.)
        Filter:
            I Implemented some filters, but stopped because its hard to know if the approach correct without valid api key.
        _daily_email_enabled:
            Assuming its related to an emails being sent out, actual verification of emails being sent,
             should have a separate test, related to that functionality.
    """
    search = SavedSearch(name=name, item_types=item_types, filter=_filter, __daily_email_enabled=__daily_email_enabled)
    search.create()
    assert search.is_created == name_expected, f'Saved search should be {"" if name_expected else "not "}created with name {name}'

@pytest.mark.parametrize("original_name, changed_name, name_expected", [(Strings.random(l=12),Strings.random(l=14), True), (Strings.random(l=12), "$"*128, False)])
# @pytest.mark.parametrize("orig_item_types,changed_item_types", [(['REOrthoTile'], ['PSScene3Band])])
# @pytest.mark.parametrize("__daily_email_enabled", [True, False])
# @pytest.mark.parametrize("orig_filter", "changed_filter", zip(Filters.testable, Filters.testable[1:] + Filters.testable[:1]))
# def test_update(original_name, changed_name, name_expected, orig_item_types, changed_item_types, orig_filter, changed_filter, __daily_email_enabled ):
def test_update(original_name, changed_name, name_expected):    
    """All expannsions from creation test can be appliead for an update test as well.
    """
    search = SavedSearch(name=original_name)
    original = search.create()
    search.update(search_id=original.get('id'), name=changed_name)
    updated = search.get(search_id=original.get('id'))
    assert updated.get('name')  == changed_name if name_expected else original_name, f'Saved search should be {"" if name_expected else "not "}updated with name {changed_name}'
    

@pytest.mark.parametrize("existing", [True, False])
def test_delete(existing):
    search = SavedSearch() #We have default values in case type of saved search doesnt matter. We should make sure that it really doesnt matter though.
    if existing:
        original = search.create()
        _id = original.get('id')
    else:
        _id = Strings.random(l=12) # we need to make sure this value cant exist, but formatted correctly.
    search.delete(search_id=_id)
    assert search.is_deleted == existing, f'Saved search should be {"" if existing else "not "}deleted.'
    
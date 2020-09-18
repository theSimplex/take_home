from data.defaults import FilterDefaults

class Filter(object):
    def __init__(self, conditions):
        self.conditions = conditions


class ConditionFilter(object):
    def __init__(self, field_name, config):
        self.field_name = field_name
        self.config = config

    def to_dict(self):
        return {
            "type": self.__class__.__name__,
            "field_name": self.field_name,
            "config": self.config
        }

    def __and__(self, other):
        if isinstance(other, AndFilter):
            other.conditions.append(self)
            return other
        return AndFilter([self, other])

    def __or__(self, other):
        if isinstance(other, OrFilter):
            other.conditions.append(self)
            return other
        return OrFilter([self, other])

    def __invert__(self):
        return NotFilter(self)


class DateRangeFilter(ConditionFilter):
    """Matches dates that fall within a range."""

    def __init__(self, field_name='acquired', gt=None, gte=None, lt=None, lte=None, timezone="Z"):
        assert field_name in ['acquired', 'published', 'updated']
        assert not (lt and lte), "lt and lte are mutually exclusive"
        assert not (gt and gte), "gt and gte are mutually exclusive"
        config = {"gt": gt, "gte": gte, "lt": lt, "lte": lte}
        for key in list(config.keys()):
            val = config[key]
            if not val:
                del config[key]
                continue
            config[key] = config[key].isoformat() + timezone
        super().__init__(field_name, config)


class GeometryFilter(ConditionFilter):
    """Matches using GeoJSON geometry."""
    def __init__(self, geometry=None):
        if not geometry:
            geometry = FilterDefaults.default_geometry_filter
        assert geometry['type'] in ["Polygon", "MultiPolygon", "Feature", "FeatureCollection"]
        if geometry['type'] in ['Polygon', 'MultiPolygon']:
            assert isinstance(geometry['coordinates'], list) or isinstance(geometry['coordinates'], tuple)
        else:
            assert isinstance(geometry['features'], list) or isinstance(geometry['features'], tuple)
        super().__init__("geometry", geometry)

    @staticmethod
    def _multi_polygonize(d):
        if d['type'] == "MultiPolygon":
            return d['coordinates']
        else:
            return [d['coordinates']]


class NumberInFilter(ConditionFilter):
    """Matches any number within the array of provided numbers."""

    def __init__(self, field_name="gsd", value_list=[3]):
        assert field_name in ["sun_azimuth", "sun_elevation", "gsd", "view_angle", "cloud_cover", "black_fill",
                              "usable_data", "origin_y"]
        assert isinstance(value_list, list)
        super().__init__(field_name, value_list)


class RangeFilter(ConditionFilter):
    """Matches numbers that fall within a range."""

    def __init__(self, field_name="cloud_cover", gt=None, gte=None, lt=None, lte=0.1):
        assert field_name in ["sun_azimuth", "sun_elevation", "gsd", "view_angle", "cloud_cover", "black_fill",
                              "usable_data", "origin_y"]
        assert not (lt and lte), "lt and lte are mutually exclusive"
        assert not (gt and gte), "gt and gte are mutually exclusive"
        config = {"gt": gt, "gte": gte, "lt": lt, "lte": lte}
        for key in list(config.keys()):
            val = config[key]
            if val is None:
                del config[key]

        upper_bound = config.get('lt', config.get('lte', float('inf')))
        lower_bound = config.get('gt', config.get('gte', float('-inf')))
        assert upper_bound >= lower_bound, "lower_bound > upper_bound"
        assert len(config) > 0, "Need at least one value in the RangeFilter"
        super().__init__(field_name, config)


class StringInFilter(ConditionFilter):
    """Matches any string within the array of provided strings."""

    def __init__(self, field_name="ground_control", string_list=["true"]):
        assert field_name in ["catalog_id", "strip_id", "item_type", "grid_cell",
                              "satellite_id", "provider", "ground_control","quality_category"]
        assert isinstance(string_list, list)
        super().__init__(field_name, string_list)
        
class UpdateFilter(ConditionFilter):
    """Matches any changes to a specified metadata field value made after a specified date, due to a republishing event."""

    def __init__(self, field_name="ground_control", config={"gt": "2020-04-15T00:00:00Z"}):
        assert field_name in ["catalog_id", "strip_id", "item_type", "grid_cell",
                              "satellite_id", "provider", "ground_control"]
        assert isinstance(config, dict)
        super().__init__(field_name, config)


class LogicalFilter(Filter):
    def to_dict(self):
        return {
            "type": self.__class__.__name__,
            "config": [condition.to_dict() for condition in self.conditions] if isinstance(self.conditions, list) else self.conditions.to_dict()
        }

    def __and__(self, other):
        self.conditions.append(other)
        return self

    def __or__(self, other):
        if isinstance(other, ConditionFilter):
            self.conditions.append(other)
            return other
        return OrFilter([self, other])

    def __invert__(self):
        return NotFilter(self)


class AndFilter(LogicalFilter):
    def __init__(self, conditions=None):
        if not conditions:
            self.conditions = [StringInFilter(), UpdateFilter()]

class OrFilter(LogicalFilter):
    def __init__(self, conditions=None):
        if not conditions:
            self.conditions = [StringInFilter(), StringInFilter(field_name="quality_category",string_list=["test"])]

class NotFilter(LogicalFilter):
    def __init__(self, conditions=None):
        if not conditions:
            self.conditions = StringInFilter()

class Filters:
    testable = [DateRangeFilter, GeometryFilter, NumberInFilter, RangeFilter, StringInFilter, UpdateFilter,
                AndFilter, OrFilter, NotFilter]
    
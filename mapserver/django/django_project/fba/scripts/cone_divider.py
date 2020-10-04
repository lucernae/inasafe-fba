import math
from shapely.geometry import LineString, Point
from shapely.ops import split
from shapely.geometry import mapping, base, shape


class ConeDivider:
    """
    Split a Polygon cone based on Point list,
    Returns divided cones as a geojson dict data
    """

    points = []
    cone_json = None
    tick_length = 10

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    # Get the angle between two points
    def _getAngle(self, pt1, pt2):
        x_diff = pt2.x - pt1.x
        y_diff = pt2.y - pt1.y
        return math.degrees(math.atan2(y_diff, x_diff))

    # Start and end points of chainage tick
    # Get the first end point of a tick
    def _getPoint1(self, pt, bearing, dist):
        angle = bearing + 90
        bearing = math.radians(angle)
        x = pt.x + dist * math.cos(bearing)
        y = pt.y + dist * math.sin(bearing)
        return Point(x, y)

    # Get the second end point of a tick
    def _getPoint2(self, pt, bearing, dist):
        bearing = math.radians(bearing)
        x = pt.x + dist * math.cos(bearing)
        y = pt.y + dist * math.sin(bearing)
        return Point(x, y)

    # Create a geojson feature from shapely object and properties
    def _create_geojson_feature(
            self,
            shapely_object: base.BaseGeometry,
            properties: dict = None) -> dict:
        if properties is None:
            properties = {}
        if not isinstance(shapely_object, base.BaseGeometry):
            raise Exception('Not a shapely object')
        return {
            'type': 'Feature',
            'properties': properties,
            'geometry': mapping(shapely_object)
        }

    # Split the cone to multiple cones
    # put the point properties into their respective cones
    # then return the divided cones as geojson
    def split_cones(self) -> dict:

        try:
            # Convert to shapely object
            cone_geom = shape(self.cone_json['features'][0]['geometry'])
            center_points = []
            for point in self.points['features']:
                center_points.append({
                    'geometry': Point(point['geometry']['coordinates']),
                    'properties': point['properties']
                })
        except (KeyError, ValueError) as e:
            return {}

        # Create ticks from points
        ticks = []
        for num, pt in enumerate(center_points, 1):
            pt = pt['geometry']
            if num == 1:
                angle = self._getAngle(pt, center_points[num]['geometry'])
                line_end_1 = self._getPoint1(pt, angle, self.tick_length / 2)
                angle = self._getAngle(line_end_1, pt)
                line_end_2 = self._getPoint2(line_end_1, angle,
                                            self.tick_length)
                ticks.append(LineString([(line_end_1.x, line_end_1.y),
                                         (line_end_2.x, line_end_2.y)]))
            # Everything in between
            if num < len(center_points) - 1:
                angle = self._getAngle(pt, center_points[num]['geometry'])
                line_end_1 = self._getPoint1(center_points[num]['geometry'],
                                            angle,
                                            self.tick_length / 2)
                angle = self._getAngle(line_end_1,
                                      center_points[num]['geometry'])
                line_end_2 = self._getPoint2(line_end_1, angle,
                                            self.tick_length)
                ticks.append(LineString([(line_end_1.x, line_end_1.y),
                                         (line_end_2.x, line_end_2.y)]))

            # End chainage
            if num == len(center_points):
                angle = self._getAngle(center_points[num - 2]['geometry'], pt)
                line_end_1 = self._getPoint1(pt, angle, self.tick_length / 2)
                angle = self._getAngle(line_end_1, pt)
                line_end_2 = self._getPoint2(line_end_1, angle,
                                            self.tick_length)
                ticks.append(LineString([(line_end_1.x, line_end_1.y),
                                         (line_end_2.x, line_end_2.y)]))

        # Split the cone by ticks
        cone_list = [ cone_geom ]
        for tick in ticks[1:]:
            for cone in cone_list:
                if tick.crosses(cone):
                    divided_cones = split(cone, tick)
                    cone_list.remove(cone)
                    for divided_cone in divided_cones:
                        cone_list.append(divided_cone)
                    break

        cones_with_props = []
        features = []

        # Add point properties to cones
        for center_point in center_points:
            center_point_geom = center_point['geometry']
            center_point_prop = center_point['properties']
            for cone in cone_list:
                if center_point_geom.within(cone) and not cones_with_props:
                    cones_with_props.append(cone)
                    features.append(
                        self._create_geojson_feature(cone, center_point_prop)
                    )
                    break
                if cones_with_props and cone not in cones_with_props:
                    prev_cone = cones_with_props[len(cones_with_props) - 1]
                    if (cone.intersects(center_point_geom) and cone.intersects(
                            prev_cone)) or (prev_cone.intersects(
                            center_point_geom) and cone.intersects(prev_cone)):
                        cones_with_props.append(cone)
                        features.append(
                            self._create_geojson_feature(cone,
                                                        center_point_prop)
                        )
                        break

        geojson_data = {
            'type': 'FeatureCollection',
            'features': features
        }
        return geojson_data

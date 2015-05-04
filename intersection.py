import math
from math import sin, cos, atan2, asin, acos, tan, radians, sqrt, degrees, pi

#used from https://gist.github.com/jeromer/2005586 with a little modification
def calculate_initial_compass_bearing(pointA, pointB):
    """
    Calculates the bearing between two points.

    The formulae used is the following:
         theta = atan2(sin(delta_long).cos(lat2), cos(lat1).sin(lat2) - sin(lat1).cos(lat2).cos(delta_long))

    :Parameters:
      - `pointA: The tuple representing the latitude/longitude for the
        first point. Latitude and longitude must be in decimal degrees
      - `pointB: The tuple representing the latitude/longitude for the
        second point. Latitude and longitude must be in decimal degrees

    :Returns:
      The bearing in degrees

    :Returns Type:
      float
    """
    if (type(pointA) != tuple) or (type(pointB) != tuple):
        raise TypeError("Only tuples are supported as arguments")
 
    lat1 = radians(pointA[0])
    lat2 = radians(pointB[0])
 
    diffLong = radians(pointB[1] - pointA[1])
 
    x = sin(diffLong) * cos(lat2)
    y = cos(lat1) * sin(lat2) - (sin(lat1)
            * cos(lat2) * cos(diffLong))
 
    initial_bearing = atan2(x, y)
 
    # Now we have the initial bearing but atan2 return values
    # from -180 to + 180 which is not what we want for a compass bearing
    # The solution is to normalize the initial bearing as shown below
    initial_bearing = degrees(initial_bearing)
    compass_bearing = (initial_bearing + 360) % 360
    final_bearing = (compass_bearing + 180) % 360 
    #print compass_bearing, final_bearing
    #return compass_bearing, final_bearing
    #compass_bearing = start bearing
    return compass_bearing


def arc_intersection(lat1, lon1, bearing1, lat2, lon2, bearing2):

    '''
    Translated to Python from http://www.movable-type.co.uk/scripts/latlong.html
    '''
    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)
    delta_lat = lat2 - lat1
    delta_lon = lon2 - lon1
    theta13 = radians(bearing1)
    theta23 = radians(bearing2)
    
    d12 = 2 * asin( sqrt(     sin(delta_lat/2) * sin(delta_lat/2)      +       cos(lat1) * cos(lat2) * sin(delta_lon/2) * sin(delta_lon/2)       ) )
    if d12 == 0:
        return None
    
    theta1 = acos(     ( sin(lat2) - sin(lat1) * cos(d12) )        /            (sin(d12) * cos(lat1))             )
    if math.isnan(theta1):
        theta1 = 0
    theta2 = acos(     ( sin(lat1) - sin(lat2) * cos(d12) )        /            (sin(d12) * cos(lat2))             )
    
    if sin(delta_lon) > 0:
        theta12 = theta1
        theta21 = 2 * pi - theta2
    else:
        theta12 = 2 * pi -theta1
        theta21 = theta2
    

    alpha1 = (theta13 - theta12 + pi) % (2 * pi) - pi
    alpha2 = (theta21 - theta23 + pi) % (2 * pi) - pi
    
    if sin(alpha1) == 0 and sin(alpha2) == 0: #infinite intersection
        return None
    if sin(alpha1) * sin(alpha2) < 0:  #ambigous intersection
        return None
    
    alpha3 = acos( - cos(alpha1) * cos(alpha2) + sin(alpha1) * sin(alpha2) * cos(d12))
    d13 = atan2(sin(d12) * sin(alpha1) * sin(alpha2), cos(alpha2) + cos(alpha1) * cos(alpha3))
    lat3 = asin( sin(lat1) * cos(d13) + cos(lat1) * sin(d13) * cos(theta13))
    real_delta_lon13 = atan2(sin(theta13) * sin(d13) * cos(lat1) , cos(d13) - sin(lat1) * sin(lat3))
    lon3 = lon1 + real_delta_lon13
    
    lon3 = (lon3 + 3 * pi) % (2 * pi) - pi
    return degrees(lat3), degrees(lon3)

# find the intersection of the A1A2 line/arc and B1B2 line/arc.
pointA1 = (50, 50)
pointA2 = (51, 51)
pointB1 = (40, 40)
pointB2 = (41, 41)
#first find the bearings
bearing1 = calculate_initial_compass_bearing(pointA1, pointA2)
print bearing1
bearing2 = calculate_initial_compass_bearing(pointB1, pointB2)
print bearing2

#use A1 and B1 as start points and bearing1, bearing2 to find the intersection
intersection_point = arc_intersection(lat1=pointA1[0], lon1=pointA1[1], bearing1=bearing1, lat2=pointB1[0], lon2=pointB1[1], bearing2=bearing2)
print intersection_point
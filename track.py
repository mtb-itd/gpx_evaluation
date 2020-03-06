import gpxpy
from scipy.signal import medfilt
import numpy as np
class Track():
    def __init__(self, gpx):
        #self.gpx_file = open(gpx, 'r')
        self.gpx_file = gpx
        self.gpx = gpxpy.parse(self.gpx_file)
        self.data = [[],[]]
        self.data_map = []
        self.feature_collection = []
        self.origin = []


    def process(self):
        distance_sum = 0
        steps = 0
        prev_point = None
        for track in self.gpx.tracks:
            for segment in track.segments:
                for point in segment.points:
                    self.data_map.append([point.latitude, point.longitude])
                    if prev_point != None:
                        distance = gpxpy.geo.distance(prev_point.latitude, prev_point.longitude,prev_point.elevation, point.latitude, point.longitude, point.elevation)
                    else:
                        distance = 0
                        self.origin.append(point.latitude)
                        self.origin.append(point.longitude)
                    self.data[0].append(round(distance_sum / 1000, 3))
                    self.data[1].append(int(point.elevation))
                    distance_sum += distance
                    prev_point = point
        self.total_distance = round(distance_sum / 1000, 3)

        #cleans track with median filter
        self.data_raw = self.data.copy()
        self.data[1] = medfilt(self.data[1], 39)


    def processElevation(self):
        total_up = 0
        total_down = 0
        prev_point = None
        for point in self.data[1]:
            if prev_point != None:
                elevation = prev_point - point
            else:
                elevation = 0

            if elevation > 0:
                total_up += elevation
            else:
                total_down += abs(elevation)
            prev_point = point
        self.total_up = total_up
        self.total_down = total_down

    def saveFiltered(self, path):
        lep_gpx = gpxpy.gpx.GPX()
        # Create first track in our GPX:
        gpx_track = gpxpy.gpx.GPXTrack()
        lep_gpx.tracks.append(gpx_track)

        # Create first segment in our GPX track:
        gpx_segment = gpxpy.gpx.GPXTrackSegment()
        gpx_track.segments.append(gpx_segment)

        i = 0
        for track in self.gpx.tracks:
            for segment in track.segments:
                for point in segment.points:
                    point.elevation = self.data[1][0]
                    i += 1

        with open(path, 'w') as f:
            f.write(self.gpx.to_xml())

        return True




    def naGor(self):
        return self.total_up
    def naDol(self):
        return self.total_down
    def posrek(self):
        return self.total_distance
    def grafData(self):
        return self.data
    def grafDataRaw(self):
        return self.data_raw


def distLatLonPoint2Line(p0, p1, p2): # distance from p0 to line defined by p1 and p2 [lat,lon] (in deg)
    # Mercator projection
    P0 = np.array([np.radians(p0[1]), np.arcsinh(np.tan(np.radians(p0[0])))])*6371e3
    P1 = np.array([np.radians(p1[1]), np.arcsinh(np.tan(np.radians(p1[0])))])*6371e3
    P2 = np.array([np.radians(p2[1]), np.arcsinh(np.tan(np.radians(p2[0])))])*6371e3

    # distance from point to line
    dist = abs((P2[1]-P1[1])*P0[0]-(P2[0]-P1[0])*P0[1]+P2[0]*P1[1]-P2[1]*P1[0])/np.sqrt(np.power(P2[1]-P1[1], 2)+np.power(P2[0]-P1[0], 2)) # (from https://en.wikipedia.org/wiki/Distance_from_a_point_to_a_line#Line_defined_by_two_points)

    return(dist)


def RDP(data, epsilon): # Ramer–Douglas–Peucker algorithm
    if epsilon <= 0:
        return(data)

    dist_max = 0
    index = 0

    for i in np.arange(1, data.shape[0]):
        dist = distLatLonPoint2Line(data[i, :2], data[0, :2], data[-1, :2])

        if dist > dist_max:
            index = i
            dist_max = dist

    if dist_max > epsilon:
        tmp1 = RDP(data[:index+1, :], epsilon)
        tmp2 = RDP(data[index:, :], epsilon)

        data_new = np.vstack((tmp1[:-1], tmp2))
    else:
        data_new = np.vstack((data[0, :], data[-1, :]))

    return(data_new)
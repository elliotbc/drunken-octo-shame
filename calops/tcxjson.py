import sys
import json
from xml.dom import minidom

def tcxToJson(tcxFile):
  return json.dumps(parseGpx(tcxFile))

def parseGpx(tcxFile):
  dom = minidom.parse(tcxFile)
  outputTracks = []

  tracks = dom.getElementsByTagName("Track")
  for track in tracks:
    outputTracks.append(readTrack(track))

  return outputTracks

def readTrack(track): 
  trackData = {}
  trackData["points"] = []

  trackPoints = track.getElementsByTagName("Trackpoint")
  for trackPoint in trackPoints:
    trackData["points"].append(readTrackpoint(trackPoint));

  return trackData
    

def readTrackpoint(point):
 
  result = {}

  if not point.hasChildNodes():
    return result

  m = {
    "AltitudeMeters" : "alt",
    "DistnaceMeters" : "dist",
    "Cadence" : "cad",
    "Speed" : "speed",
    "Time" : "time"
  }

  position_map = {
    "LatitudeDegrees" : "lat",
    "LongitudeDegrees" : "lon"
  }

  for child in point.childNodes:
    if hasattr(child,"tagName"):
      if child.tagName in m:
        try:
          result[m[child.tagName]] = float(child.firstChild.nodeValue)
        except ValueError:
          result[m[child.tagName]] = child.firstChild.nodeValue
      if child.tagName == "Position":
        for c in child.childNodes:
          if hasattr(c,"tagName"):
            if c.tagName in position_map:
              result[position_map[c.tagName]] = float(c.firstChild.nodeValue)

  return result

def readTrackPoint(point):
  return {
    "lat": point.getAttribute("lat"),
    "lon": point.getAttribute("lon"),
    "elevation": getTextValue(point, "ele"),
    "time": getTextValue(point, "time")
  }



## Utility

def getTextValue(node, tagName):
  if node.getElementsByTagName(tagName):
    return node.getElementsByTagName(tagName)[0].firstChild.nodeValue
  else:
    return 0

print tcxToJson(sys.argv[1])

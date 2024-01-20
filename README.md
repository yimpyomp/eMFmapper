# <div align="center"> eMFmapper: Generate maps depicting current weather conditions at airports across the United States


## Concept of Operation:
The mapper retrieves weather information via the Aviation Weather Center API. Metar data is retrieved and loaded into a DataFrame, currently only flight category is the only aspect of weather that is retrieved. Along with the current conditions,
the coordinates and ICAO identifier of the station reporting the weather is also retrieved, to be used in displaying the points on the map. The program is currently static, it will not update unless the program is run again. 

## Contributing:
I highly doubt anyone will ever stumble across this project, and if you have then I apologize, as you can tell I am still very new to all of this. Any feedback on the structure of the code is appreciated. 

## Planned/In development features:
Currently, I plan to work on adding functionality to allow the map to refresh itself once started, rather than needing to re-run the program. In addition, I am beginning to experiment/learn how to implement a CLI, as I always have to run it from an
IDE.

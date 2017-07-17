//Data Loading:
datasources["UFSCar Dragonboar"].dragonboard.timestamp

tstamp = datasources["UFSCar Dragonboar"].dragonboard.timestamp
var date = new Date(tstamp);
var hours = date.getHours();
var minutes = "0" + date.getMinutes();
var seconds = "0" + date.getSeconds();
return hours + ':' + minutes.substr(-2) + ':' + seconds.substr(-2);


//Temperature:
datasources["UFSCar Dragonboar"].dragonboard.temperature[0].value

tstamp = datasources["UFSCar Dragonboar"].dragonboard.temperature[0].timestamp
var date = new Date(tstamp);
var hours = date.getHours();
var minutes = "0" + date.getMinutes();
var seconds = "0" + date.getSeconds();
return hours + ':' + minutes.substr(-2) + ':' + seconds.substr(-2);

//GPS
coordinates = datasources["UFSCar Dragonboar"].dragonboard.gps[0].value
return coordinates.split(",")[0];

coordinates = datasources["UFSCar Dragonboar"].dragonboard.gps[0].value
return coordinates.split(",")[1]


//Lux
datasources["UFSCar Dragonboar"].dragonboard.lux[0].value

tstamp = datasources["UFSCar Dragonboar"].dragonboard.lux[0].timestamp
var date = new Date(tstamp);
var hours = date.getHours();
var minutes = "0" + date.getMinutes();
var seconds = "0" + date.getSeconds();
return hours + ':' + minutes.substr(-2) + ':' + seconds.substr(-2);

//Tilt
datasources["UFSCar Dragonboar"].dragonboard.tilt[0].value

tstamp = datasources["UFSCar Dragonboar"].dragonboard.tilt[0].timestamp
var date = new Date(tstamp);
var hours = date.getHours();
var minutes = "0" + date.getMinutes();
var seconds = "0" + date.getSeconds();
return hours + ':' + minutes.substr(-2) + ':' + seconds.substr(-2);

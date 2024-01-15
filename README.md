# Traffic Streaming App
App for streaming Madrid traffic data visualization and analysis

## Docker Deploy
```commandline
docker compose up 
```

Then you can access the app by entering in 127.0.0.1:8050 in your browser.

### Metadata
Real time traffic data from Madrid with periodicity of 5 min.
- **fecha_hora:** Timestamp of the data.
- **idelem:** Sensor identification.
- **descripcion:** Location description of the sensor.
- **accesoAsociado:** Code related to semaphore control for timing changes.
- **intensidad:** Traffic intensity in vehicles/hour. A negative value indicates lack of data.
- **ocupacion:** Percentage of time a sensor is occupied by a vehicle.
- **carga:** Charge parameter estimated from occupation and vial saturation intensity. Represents a degree of saturation of the vial, from 0 (no traffic) to 100 (saturation).
- **nivelServicio:** 0-fluid; 1-slow; 2-retentions; 3-congestion
- **intensidadSat:** Max intensity supported by the vial in veh/h.
- **error:** Control code of data validity on the measure point.
- **subarea:** Code identification of the subarea to which the sensor is placed.
- **st_x:** X UTM coordinate of the sensor.
- **st_y:** Y UTM coordinate of the sensor.
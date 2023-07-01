## Metadata
Datos de tráfico en tiempo real con periodicidad de 5 minutos.
- **fecha_hora:** Fecha y hora en que se obtuvieron los datos.
- **idelem:** Identificación del punto de medida.
- **descripcion:** Denominación del punto de medida.
- **accesoAsociado:** Código de control relacionado con el control semafórico para la modificación de los tiempos.
- **intensidad:** Intensidad  en vehiculos/hora. Un valor  negativo implica la ausencia de tráfico.
- **ocupacion:** Porcentaje de tiempo que está un detector de tráfico ocupado por un vehiculo. 
- **carga:** Parametro de carga del vial. Representa una estimación del grado de congestión, calculado a partir de un algoritmo que usa como variables la intensidad y ocupación, con ciertos factores de correción. Establece el grado de uso de la vía en un rango de 0 (vacía) a 100 (colapso). Un valor negativo implica la ausencia de datos.
- **nivelServicio:** 0-fluido; 1-lento; 2-retenciones; 3-congestión
- **intensidadSat:** Intensidad de saturación de la vía en veh/hora y que se corresponde con el máximo número de vehículos que pueden pasar en el acceso a la intersección manteniendose la fase verde del semáforo.
- **error:** Código de control de la validez de los datos en el punto de médida.
- **subarea:** Identificador de la subárea de explotación de tráfico a la que pertenece el punto de medida.
- **st_x:** Coordenada X UTM del centroide que representa al punto de medida.
- **st_y:** Coordenada Y UTM del centroide que representa al putno de medida.

## Sensor array optimization

![Array optimization](https://github.com/myliangding/DAE/blob/master/documentation/AE_sensor_ani.gif)
### Take a bite
- To download a CSV file containing 20 sensor locations on a cylindrical sample with a radius of 50 mm and a height of 100 mm, simply paste the following address into your web browser.
```html
https://db.seis.cloud/aecylinders?nsensor=20&radius=50&height=100
```

- To download a CSV file containing 20 sensor locations on a block sample with one vertex at [-32.5, -32.5, -65] and another vertex at [32.5, 32.5, 65], simply paste the following address into your web browser.
```html
https://db.seis.cloud/aeblocks?nsensor=20&p1x=-32.5&p1y=-32.5&p1z=-65&p2x=32.5&p2y=32.5&p2z=65
```


### Example in Python

See also <a href="https://github.com/Liang-Ding/DAE/blob/master/examples/get_sensor_locations.py">the example</a>

```python
from DArrays.AEDesigner import Designer
```

```python
# Initialize an instance that can request sensor array from SeisCloud (https://seis.cloud). 
designer = Designer()
```

```python
# Get sensor locations on a block sample and save as csv file.
saving_filepath = "sensor_block_n20.csv"
designer.get_sensors_on_blocks(nsensor=20, p1x=-32.5, p1y=-32.5, p1z=-65,
                               p2x=32.5, p2y=32.5, p2z=65, saving_filepath=saving_filepath)
```
* nsensor: the number of sensor in the array
* [p1x, p1y, p1z]: the first vertex of the block sample.
* [p2x, p2y, p2z]: the second vertex of the block sample. 
* [0, 0, 0]: the sample center


```python
# Get sensor locations on a cylinder sample and save as csv file.
saving_filepath = "sensor_cylinder_n20.csv"
designer.get_sensors_on_cylinders(nsensor=20, radius=50, height=100,
                                     saving_filepath=saving_filepath)
```
* nsensor: the number of sensor in the array
* radius: the radius of the cylinder sample. 
* height: the height of the cylinder sample. 
* [0, 0, 0]: the sample center


### Note
- At present, our website offers a sensor array that includes between **8** to **40** sensors. If you're interested in optimizing a sensor array that exceeds 40 sensors, please don't hesitate to let [**me**](mailto:myliang.ding@mail.utoronto.ca) know.

- If you reside in certain countries or regions and are experiencing difficulty accessing SeisCloud (https://seis.cloud) due to connectivity problems, kindly reach out to me via email if you have an interest in utilizing our code.



* Sensor array optimization

![Array optimization](https://github.com/myliangding/DAE/blob/master/documentation/AE_sensor_ani.gif)

# Example

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
# Get sensor locations on a block sample and save as csv file.
saving_filepath = "sensor_cylinder_n20.csv"
designer.get_sensors_on_cylinders(nsensor=20, radius=50, height=100,
                                     saving_filepath=saving_filepath)
```
* nsensor: the number of sensor in the array
* radius: the radius of the cylinder sample. 
* height: the height of the cylinder sample. 
* [0, 0, 0]: the sample center

Data processing tools for acoustic emission tests. 

## Examples of usage
* Estimate the uncertainty of moment tensor inversion:

This code is tested on Linux. You may need to change the file path for '<b>sensor_location</b>' and '<b>save_dir</b>' in '[./example/app_mt_uncertainty.py](https://github.com/Liang-Ding/DAE/blob/master/examples/app_mt_uncertainty.py)' if you are using Windows OS.   

You can assess your own sensor array by setting a *.csv file with its format the same as [sensor_array_1.csv](https://github.com/Liang-Ding/DAE/blob/master/examples/sensor_array_1.csv). 

The sensors' position and source location can be set based on your own samples (or models). Those values don't need to be within [0, 1]. 

```shell
python ./examples/app_mt_uncertainty.py 
```

You are welcome to cite our paper if using any part of the code for your work
```text
Ding, L., Kravchinsky, E., Popoola, A., Qiu, Y., Goodfellow, S., Liu, Q., & Grasselli, G. (2022). 
Systematic uncertainty quantification of first-polarity-based moment tensor inversion 
due to sparse coverage of sensor arrays in laboratory acoustic emission monitoring., 
in preparation.
```

* source location (to be added)

![Sample and coordination](https://github.com/myliangding/DAE/blob/master/documentation/DCylinder.jpg)

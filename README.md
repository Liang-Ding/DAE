Data processing tools for acoustic emission tests. 

## Documentation
<ol>
<li> Estimating the uncertainty of moment tensor inversion</li>

<ul>
<li> This code is tested on Linux. You may need to change the file path for '<b>sensor_location</b>' and '<b>save_dir</b>' in '[./example/app_mt_uncertainty.py](https://github.com/Liang-Ding/DAE/blob/master/examples/app_mt_uncertainty.py)' if you are using Windows OS.</li>
<li>You can assess your own sensor array by setting a *.csv file with its format the same as [sensor_array_1.csv](https://github.com/Liang-Ding/DAE/blob/master/examples/sensor_array_1.csv).</li>
<li>The sensors' position and source location can be set based on your own samples (or models). Those values don't need to be within [0, 1].</li>
<li>The 'fm_delta' in '[./example/app_mt_uncertainty.py](https://github.com/Liang-Ding/DAE/blob/master/examples/app_mt_uncertainty.py' is the interval in degree of grid search. Selecting a smaller interval (eg. 1, 2) drastically increases the computation, therefore a suitable interval, such as (5, 10), is recommended. </li>
</ul>

<li>Runing the code</li>
<ul>
<li>Estimating the uncertainty, storing the misfit of all moment tensors </li>
setting parameters in './examples/app_mt_uncertainty.py '

```text
b_save = True
save_dir = 'A directory where the result (a inversion_results.csv file) is stored.'
```
```shell
python ./examples/app_mt_uncertainty.py 
```

<li>
Estimating the uncertainty only 
</li>
setting parameters in './examples/app_mt_uncertainty.py '

```text
b_save = False
save_dir = None
```
```shell
python ./examples/app_mt_uncertainty.py 
```
</ul>
</ol>




You are welcome to cite our paper if using any part of the code for your work
```text
Ding, L., Kravchinsky, E., Popoola, A., Qiu, Y., Goodfellow, S., Liu, Q., & Grasselli, G. (2022). 
Systematic uncertainty quantification of first-polarity-based moment tensor inversion 
due to sparse coverage of sensor arrays in laboratory acoustic emission monitoring., 
in preparation.
```

* source location (to be added)

![Sample and coordination](https://github.com/myliangding/DAE/blob/master/documentation/DCylinder.jpg)

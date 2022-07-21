## Moment tensor inversion and Uncertainty Quantification

<ol>
<li> Settings and parameters</li>

<ul>
<li> This code is tested on Linux. You may need to change the file path for '<b>sensor_location</b>' and '<b>save_dir</b>' in <a href="https://github.com/Liang-Ding/DAE/blob/master/examples/app_mt_uncertainty.py">./example/app_mt_uncertainty.py</a> if you are using Windows OS.</li>
<li>You can assess your own sensor array by setting a *.csv file with its format the same as <a href="https://github.com/Liang-Ding/DAE/blob/master/examples/sensor_array_1.csv">./example/sensor_array_1.csv</a>.</li>
<li>The sensors' position and source location can be set based on your own samples (or models). Those values don't need to be within [0, 1].</li>
<li>The 'fm_delta' in <a href="https://github.com/Liang-Ding/DAE/blob/master/examples/app_mt_uncertainty.py">./example/app_mt_uncertainty.py</a> is the interval in degree of grid search. Selecting a smaller interval (eg. 1, 2) drastically increases the computation, therefore a suitable interval, such as (5, 10), is recommended. </li>
</ul>

<!-- moment tensor type --> 
<br>
<li>Moment tensor types</li>
Set the parameter <b>inv_type</b> in <a href="https://github.com/Liang-Ding/DAE/blob/master/examples/app_mt_uncertainty.py">./example/app_mt_uncertainty.py</a> to use different types of moment tensor in the inversion. 
<ul>
<li>Full moment tensor (default)</li>

```text
inv_type='full'
```

<li>Double-couple (DC)</li>

```text
inv_type='dc'
```

<li>Deviatoric (DC+CLVD)</li>

```text
inv_type='dev'
```

</ul>


<!-- Inversion and uncertainty quantification -->
<br>
<li>Inversion and Uncertainty quantification</li>
<ul>
<li>Estimating the uncertainty and storing the misfit of all moment tensors (default) </li>
setting parameters in <a href="https://github.com/Liang-Ding/DAE/blob/master/examples/app_mt_uncertainty.py">./example/app_mt_uncertainty.py</a>

```text
b_save = True
save_dir = 'A directory where the result (a inversion_results*.csv file) is stored.'
```
then running the code
```shell
python ./examples/app_mt_uncertainty.py 
```

<li>
Only estimating the uncertainty 
</li>
setting parameters in <a href="https://github.com/Liang-Ding/DAE/blob/master/examples/app_mt_uncertainty.py">./example/app_mt_uncertainty.py</a>

```text
b_save = False
save_dir = None
```
then running the code
```shell
python ./examples/app_mt_uncertainty.py 
```
</ul>

</ol>

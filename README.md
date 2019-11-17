# pecan-dataport-DB

[![Build Status](https://travis-ci.com/markcx/pecan-dataport-DB.svg?token=pEMCHgBzx77s5ATw7U7T&branch=master)](https://travis-ci.com/markcx/pecan-dataport-DB)

### Pecan street dataport database project 
This repo builds up a python package to pull up and backup postgres Database content. It mainly works on energy related data. 

When running the following line: 
```bash
python main.py
```
The expected result is 

```python
electricity
0                    eg_angle_15min
1                      eg_angle_1hr
2                     eg_angle_1min
3                       eg_angle_1s
4            eg_apparentpower_15min
5              eg_apparentpower_1hr
6             eg_apparentpower_1min
7               eg_apparentpower_1s
8                  eg_current_15min
9                    eg_current_1hr
10                  eg_current_1min
11                    eg_current_1s
12               eg_realpower_15min
13                 eg_realpower_1hr
14                eg_realpower_1min
15                  eg_realpower_1s
16  eg_realpower_1s_40homes_dataset
17                     eg_thd_15min
18                       eg_thd_1hr
19                      eg_thd_1min
20                        eg_thd_1s
``` 

and a list of anonymized building IDs 

```python
[   26    27    43    59    77    86    93    94   101   114   142   145
   153   166   171   183   186   187   252   335   370   379   387   410
   483   499   503   516   518   526   545   547   558   621   661   668
   690   698   744   781   792   796   821   871   890   914   946   950
   974   984   994  1042  1086  1103  1104  1169  1185  1192  1202  1222
  1240  1249  1283  1334  1354  1417  1463  1500  1517  1551  1617  1629
  1641  1642  1696  1706  1714  1718  1731  1766  1792  1796  1879  1925
  1947  1970  2018  2034  2094  2096  2126  2129  2153  2158  2164  2199
  2233  2318  2335  2337  2358  2361  2365  2378  2442  2448  2461  2470
  2472  2557  2561  2602  2611  2638  2750  2786  2787  2811  2814  2818
  2859  2864  2925  2945  2980  3000  3009  3029  3039  3134  3204  3310
  3338  3344  3368  3373  3383  3392  3403  3413  3440  3456  3482  3488
  3500  3506  3517  3527  3538  3635  3649  3652  3700  3715  3719  3723
  3734  3736  3778  3829  3831  3840  3849  3893  3918  3935  3953  3967
  3976  3996  4031  4090  4147  4193  4213  4283  4298  4313  4336  4342
  4352  4356  4357  4373  4375  4395  4414  4473  4495  4499  4509  4514
  4526  4550  4580  4628  4633  4670  4699  4732  4735  4767  4830  4874
  4877  4894  4946  4956  4998  5026  5035  5058  5060  5097  5109  5129
  5192  5218  5246  5264  5275  5317  5357  5367  5371  5403  5439  5448
  5449  5450  5545  5587  5615  5656  5658  5677  5679  5715  5738  5746
  5749  5763  5784  5796  5809  5814  5892  5929  5949  5959  5972  5982
  5984  5997  6063  6069  6101  6121  6126  6139  6148  6161  6172  6178
  6240  6248  6302  6348  6378  6390  6412  6423  6464  6487  6498  6514
  6526  6558  6564  6578  6594  6643  6672  6691  6692  6703  6706  6730
  6799  6836  6868  6907  6983  6990  7016  7017  7019  7021  7024  7030
  7069  7108  7159  7365  7367  7390  7429  7504  7531  7536  7541  7627
  7660  7678  7680  7682  7690  7719  7731  7739  7741  7767  7769  7788
  7793  7800  7850  7875  7901  7935  7937  7940  7951  7965  7973  7989
  7999  8005  8013  8031  8046  8084  8086  8142  8156  8162  8198  8236
  8243  8277  8278  8282  8292  8317  8327  8342  8386  8419  8450  8467
  8503  8565  8626  8627  8645  8707  8767  8825  8829  8847  8849  8862
  8908  8967  8992  8995  9002  9004  9019  9022  9052  9053  9081  9106
  9121  9134  9141  9160  9164  9186  9206  9237  9248  9278  9290  9295
  9333  9356  9477  9484  9609  9613  9647  9701  9729  9737  9776  9818
  9875  9912  9915  9921  9922  9926  9932  9938  9939  9942  9956  9958
  9971  9973  9982  9983 10089 10164 10182 10202 10488 10554 10621 10811
 10983 11421 11435 11478 11785 11878 11888 11896 11954]
```


-----


* Reference
https://github.com/nilmtk/nilmtk  



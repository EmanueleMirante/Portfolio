# Annual Median Home Sales Price Analysis

The analysis is on the median sales price of houses sold for the United States from 1963 to 2020.The dataset
used has been obtained from Federal Reserve Economic Data(FRED).

## Preliminary Analysis

The assumption that our time series is a realization of a stationary process is clearly fundamental in time series analysis, so we must first determine whether the series can be considered a realization of a stationary process.In this stage a very useful tool is the graph of the series, many of the patterns in the data can be seen visually.

<p float="left">
  <figcaption>Fig 1: Time Plot</figcaption>
  <img src="Images/Annual_Median_Home_Sales_Price_IMG/yearP.png" width="500"  title= 'cico'/>
  <figcaption>Fig 2: Median Home Price in the United States (Nominal - Inflaction-adjusted)</figcaption>
  <img src="Images/Annual_Median_Home_Sales_Price_IMG/infnot.png" width="500" /> 

</p>




From the figure 1 we can observe an increasing trend in 1963-2007, a changing direction with a decreasing trend in home prices
starting from 2007, probably due to subprime mortgage crisis, an increasing trend again until 2020.This is a
historical home price series using nominal prices, but data which are affected by the value of money are best adjusted,in fact,
probably,the median cost of a new house will have increased over the years due to inflation.For this reason,the series was adjusted
so that all values are stated in dollar values from a particular year.
The inflation-adjusted values were obtained by dividing the original prices values by their own CPI(Consumer Price Index) and
then multiplying by the reference year CPI. In this case we set 2000 as reference year.Also the CPI was obtained from FRED
In figure 2 we can see that the adjusted values curve were more flat than the original data and appears to be less smooth, the
positive trend seems, however, to remain. The positive trend is confirmed by decreasing autocorrelations in the acf plots(figures
3 and 4 ) but the autocorrelation of the original data decreases more fast than those of the inflaction-adjusted data.

<p float="left">
  <figcaption>Fig 3: Acf original data</figcaption>
  <img src="Images/Annual_Median_Home_Sales_Price_IMG/acforig.png" width="500"  />
</p>

<p float="left">
  <figcaption>Fig 4: Acf adjusted data </figcaption>
  <img src="Images/Annual_Median_Home_Sales_Price_IMG/acfadj.png" width="500" /> 
</p>

The series is annual and therefore has no seasonality so we can compute only the ”trend” component.In particular this component
was estimated using two approaches:

* Moving average smoothing
* LOWESS Smoothing


<p float="left">
  <img src="Images/Annual_Median_Home_Sales_Price_IMG/maor.png" width="250" />
  <img src="Images/Annual_Median_Home_Sales_Price_IMG/lowor.png" width="250" /> 
  <img src="Images/Annual_Median_Home_Sales_Price_IMG/maad.png" width="250" /> 
  <img src="Images/Annual_Median_Home_Sales_Price_IMG/lowad.png" width="250" /> 

</p>

In the figures we can see the components of trend calculated with the moving average of order 15 and with the lowess for both
series.With both methods we can see that both series have an increasing trend but the transformed series has a more undulating
trend line with a series of ups and downs which confirms what was said previously.In general the loess method has been preferred
because with this we do not lose the first and last m/2 values of the trend. For the following steps only the inflaction-adjusted
series will be used.

It is necessary to obtain a stationary series. First we stabilize the variance using the box cox transformation, meanwhile for stabilise the mean it was used the First-difference.
As it appears from the ACF plot(figure 10), the series ∆Yt is stationary , aspect confirmed by the Augmented Dickey-Fuller stationarity test, for which we reject the null hypothesis of non-stationarity with a p-value=0.01.

<p float="left">
  <figcaption>Fig 9: ACF X<sub>t</sub> </figcaption>
  <img src="Images/Annual_Median_Home_Sales_Price_IMG/acfadj.png" width="500"  title= 'cico'/>
  <figcaption>Fig 10: ACF ∆Y<sub>t</sub></figcaption>
  <img src="Images/Annual_Median_Home_Sales_Price_IMG/Rplot07.png" width="500" /> 

</p>

## Model Identification and Forecasting

Model Identification involves determining the order of the model required (p and q) in order to capture the salient dynamic features of the data.
Once the model has been identified we have to estimate the paremeters. For the choice of the model it has been chosen an interval of values for p and q with d=1:

* 0<p<4
* 0<q<4

subsequently were used the information criteria(AIC,SBIC) to discriminate among the competing model.

25 models have been estimated,the model that minimizes AIC is ARIMA(3,1,1),the one chosen by the minimizzation of SBIC is an
ARIMA(2,1,1).In figures below the are the acf, pacf and qqplot of the model chosen with SBIC.It appears that almost all correlations
in the residuals result from randomness of the sampling process, and from the q-q plot they appear normally distributed.What
has been said previously is checked by Ljung-Box test that confirms the null hypothesis of indipendence and from the Jarque-Bera
test that confirms the null hypothesis of Normality.

<p float="left">
  <img src="Images/Annual_Median_Home_Sales_Price_IMG/acffitB.png" width="310"  title= 'cico'/>
  <img src="Images/Annual_Median_Home_Sales_Price_IMG/pacffitB.png" width="310" /> 
  <img src="Images/Annual_Median_Home_Sales_Price_IMG/qqplotFitB.png" width="310" /> 

</p>


In the table there are the coeﬀicients for the model ARIMA(2,1,1),calculated the test statistic t, we can say that all the coeﬀicients
of the model are significant.

  |             | AR1         | AR2       |MA1
  | ----------- | ----------- |-----------|-----------|
  | Coef        | 0.98        | -0.33     |-0.72
  | Sd          | 0.19601     | 0.12650   |0.16881
  | t.value     | 5.004       |-2.645     |-4.283

Table 1: Coeﬀicients of ARIMA(2,1,1) - SBIC




In figure below instead the are the acf, pacf and q-qplot of the model chosen with AIC.Also in this case the residuals result normal and
independent both by seeing the graphs and by performing a formal tests



<p float="left">
  <img src="Images/Annual_Median_Home_Sales_Price_IMG/acffita.png" width="310"  title= 'cico'/>
  <img src="Images/Annual_Median_Home_Sales_Price_IMG/pacffita.png" width="310" /> 
  <img src="Images/Annual_Median_Home_Sales_Price_IMG/qqplotfita.png" width="310" /> 

</p>



  |             | AR1         | AR2       |MA1
  | ----------- | ----------- |-----------|-----------|
  | Coef        | 0.98        | -0.33     |-0.72
  | Sd          | 0.19601     | 0.12650   |0.16881
  | t.value     | 5.004       |-2.645     |-4.283

Table 2: Coeﬀicients of ARIMA(3,1,1) - AIC


In table 2 there are the coeﬀicients for the model ARIMA(3,1,1),calculated the test statistic t, we can say that all the coeﬀicients
of the model are significant at the 5% level except for the AR2 and AR3 coeﬀicients.

### Forecasting

Now let’s compare the models based on forecast performance.The dataset has been divided into train(from 1963 to 2010 ∼ 80%
of observation) and test set(from 2011 to 2020 ∼ 20% of observation).
We look for the model that minimizes all the metrics, in this case it is ARIMA(3, 1, 1),the model chosen by AIC. In the figure
11 we can see the predicted values plot on the Box-Cox scale(with the confident interval) of the adjusted-inflaction data, and
in the figure 12[^1] the predicted values plot on the nominal price scale after applying the Box-Cox back transformation and the
inverse formula to return to nominal values.




  |   MODEL     | RMSE        | MAE       |MPE        |MAPE  
  | ----------- | ----------- |-----------|-----------|-----------
  | Arima(2,1,1)| 7.97        | 7.28     |3.54      |3.78
  | Arima(3,1,1)| 7.28     | 6.52   |3.06    |3.39
 
 Table 3: Metrics for both models






<p float="left">
  <figcaption>Fig 11: Predicted Values on Box-Cox Scale </figcaption>
  <img src="Images/Annual_Median_Home_Sales_Price_IMG/plotplot.png" width="500"  title= 'cico'/>
  <figcaption>Fig 12: Figure 42: Predicted Values on Nominal Price Scale </figcaption>
  <img src="Images/Annual_Median_Home_Sales_Price_IMG/evvai.png" width="500" /> 

</p>

[^1]: The green line represent the train set, the red line the predictions and the blue line the test set


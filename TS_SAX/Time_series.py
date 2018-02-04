import numpy as np
import matplotlib.pyplot as plt
import timesynth as ts

def ir_Time_series_Gaussian(t):
    time_sampler = ts.TimeSampler(stop_time=t)
    irregular_time_samples = time_sampler.sample_irregular_time(num_points=100, keep_percentage=50)

    gp = ts.signals.GaussianProcess(kernel='Matern', nu=3./2)
    gp_series = ts.TimeSeries(signal_generator=gp)
    samples = gp_series.sample(irregular_time_samples)[0]
    return (samples,irregular_time_samples)


def ir_Time_series_CAR(t):
    time_sampler = ts.TimeSampler(stop_time=t)
    irregular_time_samples = time_sampler.sample_irregular_time(num_points=500, keep_percentage=50)

    car = ts.signals.CAR(ar_param=0.9, sigma=0.01)
    car_series = ts.TimeSeries(signal_generator=car)
    samples = car_series.sample(irregular_time_samples)
    return (samples[0], irregular_time_samples)


def Time_series_Gaussian(t):
    time_sampler = ts.TimeSampler(stop_time=t)
    regular_time_samples = time_sampler.sample_regular_time(num_points=t)

    gp = ts.signals.GaussianProcess(kernel='Matern', nu=3./2)
    gp_series = ts.TimeSeries(signal_generator=gp)
    samples = gp_series.sample(regular_time_samples)[0]
    return samples
   
def Time_series_CAR(t):
    time_sampler = ts.TimeSampler(stop_time=t)
    regular_time_samples = time_sampler.sample_regular_time(num_points=t)

    car = ts.signals.CAR(ar_param=0.9, sigma=0.01)
    car_series = ts.TimeSeries(signal_generator=car)
    samples = car_series.sample(regular_time_samples) 
#    plt.plot(regular_time_samples, samples[0], marker='o', markersize=4)
    return samples[0] 

def Time_series1(t):
    limit_low = 0
    limit_high = 0.48
    my_data = np.random.normal(0, 0.5, t) \
              + np.abs(np.random.normal(0, 2, t) \
                       * np.sin(np.linspace(0, 3*np.pi, t)) ) \
              + np.sin(np.linspace(0, 5*np.pi, t))**2 \
              + np.sin(np.linspace(1, 6*np.pi, t))**2
    
    scaling = (limit_high - limit_low) / (max(my_data) - min(my_data))
    my_data = my_data * scaling
    my_data = my_data + (limit_low - min(my_data))
#    plot(my_data)



#a = Time_series_Gaussian(200)
#Time_series_CAR(200)

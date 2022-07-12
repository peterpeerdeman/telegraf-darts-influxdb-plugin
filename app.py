import os
import sys
from darts.timeseries import TimeSeries
from darts.models.forecasting.fft import FFT
from darts.models.forecasting.nbeats import NBEATSModel
from darts.utils.missing_values import fill_missing_values
import math

from influxdata import query_influx_data, write_influx_line_format

# parse environment variables
influx_query = os.environ.get('INFLUX_QUERY')
influx_org = os.environ.get('INFLUX_ORG')
influx_token = os.environ.get('INFLUX_TOKEN')
influx_url = os.environ.get('INFLUX_URL')
prediction_model = os.environ.get('PREDICTION_MODEL', 'fft')
prediction_model_epochs = os.environ.get('PREDICTION_MODEL_EPOCHS', 30)
prediction_split = os.environ.get('PREDICTION_SPLIT')
prediction_metric_name = os.environ.get('PREDICTION_METRIC_NAME', 'prediction')
prediction_count = os.environ.get('PREDICTION_COUNT')

# retrieve and prepare data
df = query_influx_data(influx_query, influx_org, influx_token, influx_url)
df['_time'] = df['_time'].astype('datetime64[ns]')
df = df.set_index('_time')
df.drop(df.tail(1).index,inplace=True) # drop last row, to avoid issues with frequency

# apply 0shot machine learning
series =  TimeSeries.from_dataframe(df, value_cols='_value', fill_missing_dates=True, fillna_value=1)
series = fill_missing_values(series)

##TODO: extract to different file / functions
if prediction_model == 'nbeats':
    model = NBEATSModel(
        input_chunk_length=30,
        output_chunk_length=30,
        generic_architecture=True,
        num_stacks=10,
        num_blocks=1,
        num_layers=4,
        layer_widths=512,
        n_epochs=int(prediction_model_epochs),
        nr_epochs_val_period=1,
        batch_size=800,
        model_name="nbeats_run",
    )
    if prediction_split:
        train, val = series.split_before(float(prediction_split))
    else:
        train, val = series.split_before(0.90)
    try:
        model.fit(train, val_series=val, verbose=False)
    except BaseException: 
        print(BaseException)
        print("error fitting model, try inputting more data", file=sys.stderr)
        quit()
    if prediction_count:
        pred_val = model.predict(n=int(prediction_count))
    else:
        pred_val = model.predict(n=math.floor(len(series)/3))
else:
    if prediction_split:
        train, val = series.split_before(float(prediction_split))
    else:
        train, val = series.split_before(0.50)
    model = FFT(nr_freqs_to_keep=20)
    model.fit(train)
    if prediction_count:
        pred_val = model.predict(n=int(prediction_count))
    else:
        pred_val = model.predict(len(val)*3)


# write data to influx line format
write_influx_line_format(pred_val, prediction_metric_name)

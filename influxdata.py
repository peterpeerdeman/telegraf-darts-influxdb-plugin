from influxdb_client import InfluxDBClient
from influx_line_protocol import Metric

def query_influx_data(query, org, token, url):
    client = InfluxDBClient(
        url=url,
        token=token,
        org=org
    )
    query_api = client.query_api()
    data_frame = query_api.query_data_frame(org=org, query=query)
    client.close()
    return data_frame

def write_influx_line_format(forecast, prediction_metric_name):
    df = forecast.pd_dataframe()
    for index, row in df.iterrows():
        metric = Metric(prediction_metric_name)
        metric.with_timestamp(index.value)
        metric.add_value("value", float(row["_value"]))
        print(metric)

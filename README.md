<h1 align="center">telegraf-darts-influxdb-plugin 👋</h1>
<p>
  <img alt="Version" src="https://img.shields.io/badge/version-0.0.1-blue.svg?cacheSeconds=2592000" />
  <img src="https://img.shields.io/badge/python-%3E%3D3.9.13-blue.svg" />
  <a href="https://github.com/peterpeerdeman/telegraf-darts-influxdb-plugin#readme" target="_blank">
    <img alt="Documentation" src="https://img.shields.io/badge/documentation-yes-brightgreen.svg" />
  </a>
  <a href="https://github.com/peterpeerdeman/telegraf-darts-influxdb-plugin/graphs/commit-activity" target="_blank">
    <img alt="Maintenance" src="https://img.shields.io/badge/Maintained%3F-yes-green.svg" />
  </a>
  <a href="https://github.com/peterpeerdeman/telegraf-darts-influxdb-plugin/blob/master/LICENSE" target="_blank">
    <img alt="License: MIT" src="https://img.shields.io/github/license/peterpeerdeman/telegraf-pvoutput" />
  </a>
  <a href="https://twitter.com/peterpeerdeman" target="_blank">
    <img alt="Twitter: peterpeerdeman" src="https://img.shields.io/twitter/follow/peterpeerdeman.svg?style=social" />
  </a>
</p>

> an external telegraf plugin that retrieves a timeseries from influxdb, uses darts to create a forecast, and writes it back to influx line format

## Prerequisites

- python >=3.9.13

## Standalone usage

```sh
cp .env.dist .env
# or ensure all environment variables listed in `.env.dist` are set before running node command
pip install -r requirements.txt
python3 app.py
```

## Docker development environment

mounts the current folder and runs with docker image
```
docker run --rm -v $PWD:/app -it peterpeerdeman/telegraf-darts-influxdb-plugin:0.0.1 python app.py
```

## telegraf configuration with docker image plugin 

telegraf.conf
```sh
[[inputs.exec]]
  commands = [
    "docker run --user root:995 --rm --env PREDICTION_MODEL=fft --env INFLUX_TOKEN=xxxxx --env INFLUX_URL=192.168.1.5:8086 --env INFLUX_ORG=org --env PREDICTION_METRIC_NAME=x-prediction --env INFLUX_QUERY='from(bucket: \"bucket\") |> range(start: -30d) |> filter(fn: (r) => r[\"_measurement\"] == \"xxx\") |> filter(fn: (r) => r[\"_field\"] == \"year_value\") |> aggregateWindow(every: 1h, fn: mean, createEmpty: false)' --name telegraf-darts-influxdb-plugin peterpeerdeman/telegraf-darts-influxdb-plugin:0.0.1",
  ]
  interval = "12h"
  timeout = "10m"
  data_format = "influx"
  name_override = "prediction-x"

[[outputs.influxdb_v2]]
  urls = ["http://influxdb2:8086"]
  token = "$INFLUX_TOKEN"
  organization = "org"
  bucket = "bucket"
  namepass = ["prediction-x"]
```

## Run tests

```sh
#TODO
```

## Author

👤 **Peter Peerdeman**

* Website: https://peterpeerdeman.nl
* Twitter: [@peterpeerdeman](https://twitter.com/peterpeerdeman)
* Github: [@peterpeerdeman](https://github.com/peterpeerdeman)
* LinkedIn: [@peterpeerdeman](https://linkedin.com/in/peterpeerdeman)

## 🤝 Contributing

Contributions, issues and feature requests are welcome!<br />Feel free to check [issues page](https://github.com/peterpeerdeman/telegraf-pvoutput/issues). 

## Show your support

Give a ⭐️ if this project helped you!

## 📝 License

This project is [MIT](https://github.com/peterpeerdeman/telegraf-pvoutput/blob/master/LICENSE) licensed.

***
_This README was generated with ❤️ by [readme-md-generator](https://github.com/kefranabg/readme-md-generator)_


# Grafana dashboards

The deployed Grafana OSS container is connected to Prometheus and displays API metrics. Two dashboards were created and saved in the live instance:

- `ResumeClassification API Monitoring` — API request rate.
- `ResumeClassification Monitoring - Final` — API availability.

The API availability panel showed `1` after the test resume prediction, and the request-rate graph showed activity. The dashboard definitions have not been exported as JSON into this repository. The live Grafana state is associated with the running instance; its exact container mount path has not been independently recorded in this source tree.

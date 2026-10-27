# Grafana monitoring

The deployed Grafana OSS container is connected to Prometheus and displays API metrics. Two dashboards were created and saved in the live instance:

- `ResumeClassification API Monitoring` — API request rate.
- `ResumeClassification Monitoring - Final` — API availability.

The API availability panel showed `1` after the test resume prediction, and the request-rate graph showed activity. The actual dashboard definitions have not been exported as JSON into this repository, so the saved panels are still present only in the live Grafana state.

For a fresh Compose deployment, `provisioning/datasources/prometheus.yml` registers Prometheus at `http://prometheus:9090` as Grafana's default data source. It does not recreate the manually built dashboards. The Grafana container uses a named volume for its database; the exact mount in the original EC2 container should be checked before any container replacement.

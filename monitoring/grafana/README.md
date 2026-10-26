# Grafana dashboard source

The deployed Grafana dashboard(s) are currently saved in the persistent `grafana-data` Docker volume. An exported dashboard JSON and provisioning file were not included in the uploaded source archives, so this directory does not yet provision a dashboard automatically.

After the EC2 instance is started, export the tested dashboard(s) from Grafana (Dashboard → Share/Export → Export as JSON) and commit the JSON here. Do not commit Grafana's database, secrets, password files, or generated runtime data. Once an exported dashboard is reviewed, it can be provisioned by Grafana so dashboards are version-controlled.

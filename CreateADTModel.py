# Databricks notebook source
import pyspark.sql.functions as F
import base64
import os
import json
from azure.digitaltwins import *
from azure.digitaltwins.core import DigitalTwinsClient
from azure.identity import *

# COMMAND ----------

azSubcriptionId = dbutils.secrets.get(scope = "common-sp", key = "az-sub-id")
azTenantId = dbutils.secrets.get(scope = "common-sp", key = "az-tenant-id")
spId = dbutils.secrets.get(scope = "common-sp", key = "common-sa-sp-client-id")
spSecret = dbutils.secrets.get(scope = "common-sp", key = "common-sa-sp-client-secret")

os.environ["AZURE_TENANT_ID"] = azTenantId
os.environ["AZURE_CLIENT_ID"] = spId
os.environ["AZURE_CLIENT_SECRET"] = spSecret

adt_url = "https://digital-twin-instance.api.eus2.digitaltwins.azure.net"
models_path = './models/'

# COMMAND ----------

credential = DefaultAzureCredential()
service_client = DigitalTwinsClient(adt_url, credential)

# COMMAND ----------

model_jsons = os.listdir(models_path)
models = []
for fn in model_jsons:
  with open(models_path + fn, 'r') as fh:
    models.extend(json.load(fh))

# COMMAND ----------

created_models = service_client.create_models(models)

# COMMAND ----------

service_client.list_models().next()

# COMMAND ----------



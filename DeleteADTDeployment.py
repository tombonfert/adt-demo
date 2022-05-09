# Databricks notebook source
# MAGIC %pip install azure-digitaltwins-core

# COMMAND ----------

# MAGIC %pip install azure-identity

# COMMAND ----------

import os
import json
from azure.digitaltwins import *
from azure.core.exceptions import ResourceExistsError
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
twin_definitions_path = './twins/twin_definitions.json'

# COMMAND ----------

credential = DefaultAzureCredential()
service_client = DigitalTwinsClient(adt_url, credential)

# COMMAND ----------

# MAGIC %md
# MAGIC ### Delete Relationships

# COMMAND ----------

with open(twin_definitions_path, 'r') as fh:
  relationships = json.load(fh)['relationships']
  for rel in relationships:
    print(rel)
    service_client.delete_relationship(rel['$sourceId'], rel['$relationshipId'])

# COMMAND ----------

# MAGIC %md
# MAGIC ### Delete Twins

# COMMAND ----------

with open(twin_definitions_path, 'r') as fh:
  twins = json.load(fh)['twins']
  for twin in twins:
    print(twin['twin_id'])
    service_client.delete_digital_twin(twin['twin_id'])

# COMMAND ----------

# MAGIC %md
# MAGIC ### Delete Models

# COMMAND ----------

listed_models = service_client.list_models()
# TODO Delete models in correct order (from leaf nodes to the root)

#for model in listed_models:
#  print(model)
#  service_client.decommission_model(model.id)
#  service_client.delete_model(model.id)

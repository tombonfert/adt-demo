# Databricks notebook source
# MAGIC %pip install azure-digitaltwins-core

# COMMAND ----------

# MAGIC %pip install azure-identity

# COMMAND ----------

import pyspark.sql.functions as F
import base64
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

# MAGIC %md
# MAGIC ### Set up connection to ADT instance

# COMMAND ----------

credential = DefaultAzureCredential()
service_client = DigitalTwinsClient(adt_url, credential)

# COMMAND ----------

# MAGIC %md
# MAGIC ### Create models

# COMMAND ----------

model_jsons = os.listdir(models_path)
models = []
for fn in model_jsons:
  with open(models_path + fn, 'r') as fh:
    models.extend(json.load(fh))

# COMMAND ----------

try:
  created_models = service_client.create_models(models)
except Exception as e:
  if isinstance(e, ResourceExistsError):
    print("Some of the model ids already exist")
    pass
  else:
    raise(e)

# COMMAND ----------

# MAGIC %md
# MAGIC ### Create Twins

# COMMAND ----------

with open(twin_definitions_path) as fh:
  twins_list = json.load(fh)['twins']
  for twin_dict in twins_list:
    temporary_twin = {
      "$metadata": {
        "$model": twin_dict['model_id']
      },
      "$dtId": twin_dict['twin_id']
    }
    print(temporary_twin)
    created_twin = service_client.upsert_digital_twin(twin_dict['twin_id'], temporary_twin)

# COMMAND ----------

# MAGIC %md
# MAGIC ### Create Relationships

# COMMAND ----------

with open(twin_definitions_path) as fh:
  relationships = json.load(fh)['relationships']
  for relationship in relationships:
    print(relationship)
    service_client.upsert_relationship(
        relationship["$sourceId"],
        relationship["$relationshipId"],
        relationship
    )

# COMMAND ----------



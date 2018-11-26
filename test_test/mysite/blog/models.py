from django.db import models
import pandas as pd
import numpy as np


class Exp_models(models.Model):
	class Meta:
		db_table = 'exp_data'
	id = models.AutoField(primary_key=True)

	Run_id              =  models.CharField(max_length=200 ,blank=True)
	Treatment           =  models.CharField(max_length=200 ,blank=True)
	Tissue              =  models.CharField(max_length=200 ,blank=True)
	Gene_id             =  models.CharField(max_length=200 ,blank=True)
	Tpm                 =  models.CharField(max_length=200 ,blank=True)
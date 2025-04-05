import numpy as np
import pandas as pd
import tensorflow as tf
import yfinance as yf
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns
from tensorflow.keras.layers import Dropout
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import GRU, Dense, BatchNormalization
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import GRU, Dense, Dropout, BatchNormalization
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.regularizers import l2
from tensorflow.keras import layers
from tensorflow.keras.models import load_model


class GruAgent:

    def __init__(self):
        self.scaler = MinMaxScaler()
        self.model = load_model('GRU_Agent.keras')

    def preprocessing(self, x):
        return self.scaler.fit_transform(x.values.reshape(-1, 1))

    def create_last_sequence(self, x, seq_length=90):
        return np.array([x[-seq_length:]])

    def predict(self, x):
        pred = self.model.predict(x)
        pred = self.scaler.inverse_transform(pred)
        return int(pred[0][0])

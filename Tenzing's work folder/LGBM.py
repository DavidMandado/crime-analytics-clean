#import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import r2_score, mean_squared_error, accuracy_score, classification_report
from lightgbm import LGBMRegressor
import time
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.multioutput import MultiOutputRegressor
import time
import optuna
import lightgbm as lgb


#streed data
df_street = pd.read_csv(r'C:\Users\mgshe\PycharmProjects\Addressing-real-world-crime-and-security-problems-with-data-science\combined_data_2019_onwards.csv', low_memory=False)
df_street['Month'] = pd.to_datetime(df_street['Month'])
df_street['year_month'] = df_street['Month'].dt.to_period('M')

# useful for later
lsoa_lookup = df_street[['Latitude', 'Longitude', 'LSOA name']].drop_duplicates()


# Build lookup from original street data
lsoa_code_name_lookup = df_street[['LSOA name', 'LSOA code']].drop_duplicates()

# burglary flag
df_street['is_burglary'] = (df_street['Crime type'].str.lower() == 'burglary').astype(int)

# aggregation of street data
burglary_agg = df_street.groupby(['LSOA name', 'year_month']).agg(
    total_crimes=('Crime ID', 'count'),
    burglaries=('is_burglary', 'sum')
).reset_index()

#stop and seach time
df_stopsearch = pd.read_csv(r"C:\Users\mgshe\PycharmProjects\Addressing-real-world-crime-and-security-problems-with-data-science\Tenzing's work folder\combined_data_S&S_2019_onwaresd.csv", low_memory=False)
df_stopsearch['Date'] = pd.to_datetime(df_stopsearch['Date'])
df_stopsearch['year_month'] = df_stopsearch['Date'].dt.to_period('M')

# spatial join to add LSOA names
df_stopsearch_lsoa = pd.merge(
    df_stopsearch,
    lsoa_lookup,
    on=['Latitude', 'Longitude'],
    how='left'
)

# Aggregate stop and search data per LSOA and month
stopsearch_agg_lsoa = df_stopsearch_lsoa.groupby(['LSOA name', 'year_month']).size().reset_index(name='stop_search_count')


# Merge burglary and stop & search data into one main df
combined_df = pd.merge(
    burglary_agg,
    stopsearch_agg_lsoa,
    on=['LSOA name', 'year_month'],
    how='left'
)

combined_df['stop_search_count'] = combined_df['stop_search_count'].fillna(0)


new_data_df = pd.read_csv(r"C:\Users\mgshe\PycharmProjects\Addressing-real-world-crime-and-security-problems-with-data-science\Data\crime_counts_with_lags_imd_and_population.csv")
print(new_data_df.head())



# Parse month as datetime and convert to Period[M] to match main dataset
new_data_df['month'] = pd.to_datetime(new_data_df['month']).dt.to_period('M')

# Focus on burglary only
new_data_df = new_data_df[new_data_df['crime_type'].str.lower() == 'burglary']


# Merge engineered features into combined_df
combined_df = pd.merge(
    combined_df,
    lsoa_code_name_lookup,
    on='LSOA name',
    how='left'
)

# 4. Now merge with lag/IMD/population features
combined_df = pd.merge(
    combined_df,
    new_data_df,
    left_on=['LSOA code', 'year_month'],
    right_on=['lsoa_code', 'month'],
    how='left'
)


# idk if I should split year_month (potential seasonality features)
combined_df['year'] = combined_df['year_month'].dt.year
combined_df['month'] = combined_df['year_month'].dt.month




#oki new stuff
# implement Rik's 3 month predictor
for lag in [1, 2, 3]:
    combined_df[f'burglaries_t+{lag}'] = combined_df.groupby('LSOA name')['burglaries'].shift(-lag)

# Drop rows with missing targets
multi_y_cols = ['burglaries_t+1', 'burglaries_t+2', 'burglaries_t+3']
combined_df = combined_df.dropna(subset=multi_y_cols)

#  features and targets
features = [
    'total_crimes',
    'stop_search_count',
    'lag_1', 'lag_2', 'lag_3',
    'rolling_mean_3', 'rolling_std_3', 'rolling_mean_6', 'rolling_sum_12',
    'imd_decile_2019', 'income_decile_2019', 'employment_decile_2019',
    'crime_decile_2019', 'health_decile_2019', 'population',
    'year', 'month'
]
target = 'burglaries'

print(combined_df.head())
x = combined_df[features].fillna(0)
y = combined_df[multi_y_cols]

# STEP 3: Train-test split
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

def objective(trial):
    params = {
        'objective': 'regression',
        'metric': 'rmse',
        'boosting_type': 'gbdt',
        'verbosity': -1,
        'learning_rate': trial.suggest_float('learning_rate', 0.01, 0.2),
        'num_leaves': trial.suggest_int('num_leaves', 20, 200),
        'max_depth': trial.suggest_int('max_depth', 4, 16),
        'min_child_samples': trial.suggest_int('min_child_samples', 10, 100),
        'subsample': trial.suggest_float('subsample', 0.6, 1.0),
        'colsample_bytree': trial.suggest_float('colsample_bytree', 0.6, 1.0),
        'reg_alpha': trial.suggest_float('reg_alpha', 0.0, 1.0),
        'reg_lambda': trial.suggest_float('reg_lambda', 0.0, 1.0)
    }

    base_model = lgb.LGBMRegressor(**params, n_estimators=1000)
    model = MultiOutputRegressor(base_model)

    model.fit(x_train, y_train)

    preds = model.predict(x_test)
    rmse = mean_squared_error(y_test, preds, squared=False)  # RMSE over all targets
    return rmse


study = optuna.create_study(direction='minimize')
study.optimize(objective, n_trials=1)  # Can increase if needed

print("Best parameters found:")
print(study.best_params)


best_params = study.best_params
final_base_model = lgb.LGBMRegressor(**best_params, n_estimators=1000)
final_model = MultiOutputRegressor(final_base_model)

final_model.fit(x_train, y_train)

# Evaluate
preds = final_model.predict(x_test)
rmse = mean_squared_error(y_test, preds, squared=False)
print(f'Final MultiOutput RMSE: {rmse:.4f}')


#
# model = MultiOutputRegressor(LGBMRegressor(random_state=83))
# t0 = time.perf_counter()
# model.fit(X_train, y_train)
# fit_time = time.perf_counter() - t0
#
# print(f"Fit time: {fit_time:.2f} seconds")
#
# # STEP 5: Make predictions and evaluate
y_pred_rounded = preds.round().astype(int)
horizons = ['1‑month ahead', '2‑months ahead', '3‑months ahead']
for i, label in enumerate(horizons):
    rmse = mean_squared_error(y_test.values[:, i], preds[:, i], squared=False)
    r2 = r2_score(y_test.values[:, i], preds[:, i])
    #y_pred_temp = [y_pred_rounded[:, i]]
    #classification_report(y_test, y_pred_temp)
    #accuracy = accuracy_score(y_test[:, i], y_pred_rounded[:, i])

    print(f'{label}: RMSE={rmse:.2f}, R²={r2:.3f}')
    #print(classification_report)

importances = np.mean([est.feature_importances_ for est in final_model.estimators_], axis=0)
imp_df = pd.DataFrame({'feature': features, 'importance': importances}).sort_values('importance', ascending=False)
print(imp_df)

#poisson time


# Avoid log(0) or instability in Poisson loss
combined_df[multi_y_cols] = combined_df[multi_y_cols].clip(lower=1e-5)

x = combined_df[features].fillna(0)
y = combined_df[multi_y_cols]

# Split
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

# Each base LightGBM regressor will use Poisson objective
base_poisson = lgb.LGBMRegressor(objective='poisson', n_estimators=1000)

# Wrap in multi-output regressor
poisson_model = MultiOutputRegressor(base_poisson)

# Fit

study.optimize(objective, n_trials=1)  # Can increase if needed

poisson_model.fit(x_train, y_train)

# Predict
y_pred = poisson_model.predict(x_test)

# Evaluate
rmse = mean_squared_error(y_test, y_pred, squared=False)
print(f'Poisson MultiOutput RMSE: {rmse:.4f}')
for i, col in enumerate(multi_y_cols):
    err = mean_squared_error(y_test.iloc[:, i], y_pred[:, i], squared=False)
    print(f'{col} RMSE: {err:.4f}')



#
# #model time
# features = [
#     'total_crimes',
#     'stop_search_count',
#     'lag_1', 'lag_2', 'lag_3',
#     'rolling_mean_3', 'rolling_std_3', 'rolling_mean_6', 'rolling_sum_12',
#     'imd_decile_2019', 'income_decile_2019', 'employment_decile_2019',
#     'crime_decile_2019', 'health_decile_2019', 'population',
#     'year', 'month'
# ]
# target = 'burglaries'
#
#
#
#
# x = combined_df[features]
# y = combined_df[target]
#
#
#
#
# x = combined_df[features]
# x = x.fillna(0)  # or use imputation
#
# y = combined_df[target]
#
# x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)
#
# model = LGBMRegressor(random_state=83)
# model.fit(x_train, y_train)
#
#
# y_pred = model.predict(x_test)
# y_pred_rounded = y_pred.round().astype(int)
# results = x_test.copy()
#
# results['predicted_burglaries'] = y_pred_rounded
# results['actual_burglaries'] = y_test.values
# results['LSOA name'] = combined_df.loc[x_test.index, 'LSOA name']
# results['year_month'] = combined_df.loc[x_test.index, 'year_month']
#
#
# # this is hella long
# #print(results[['LSOA name', 'year_month', 'predicted_burglaries', 'actual_burglaries']].to_string(index=False))
#
#
#
# output_path = r"C:Users\mgshe\PycharmProjects\Addressing-real-world-crime-and-security-problems-with-data-science\Tenzing's work folder\model_results_rounded.csv"
# results[['LSOA name', 'year_month', 'predicted_burglaries', 'actual_burglaries']].to_csv(output_path, index=False)# Evaluattion time
# r2 = r2_score(y_test, y_pred_rounded)
# print(f"R² (Accuracy) on Test Data: {r2:.4f}")
# mse = mean_squared_error(y_test, y_pred_rounded)
# print(f"Mean Squared Error: {mse:.4f}")
#
# print("pburg: ", results['predicted_burglaries'].mean(), "\naburg",results['actual_burglaries'].mean())
# # binary encoding bc the output was weird
# y_pred_binary = (y_pred >= 0.5).astype(int)
# y_test_binary = (y_test >= 1).astype(int)
# print("bi time")
# print(classification_report(y_test_binary, y_pred_binary))
# accuracy = accuracy_score(y_test_binary, y_pred_binary)
# print ("bi acc:", accuracy)
# accuracy = accuracy_score(y_test, y_pred_rounded)
# print(classification_report(y_test, y_pred_rounded))
#
# print(f"Accuracy: {accuracy:.4f}")
#

"""
plt.scatter(y_test, y_pred_rounded, alpha=0.5)
plt.xlabel('Actual Burglaries')
plt.ylabel('Predicted Burglaries')
plt.title('Actual vs Predicted Burglary Counts')
plt.show()
plt.savefig("actual vs predicted burglary counts.png")
"""
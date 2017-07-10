import pandas as pd

def call_and_concat(sample_df, feature_funcs):
    feature_df_list = []
    for feature_func in feature_funcs:
        feature_df = feature_func(sample_df)
        feature_mod_name = '%s.%s' % (feature_func.__module__, feature_func.__name__)
        feature_df.columns = ['%s.%s' % (feature_mod_name, x) for x in feature_df.columns]
        feature_df_list.append(feature_df)
    return pd.concat(feature_df_list, axis=1)

    
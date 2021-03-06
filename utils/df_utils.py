import itertools as it

import numpy as np
import pandas as pd

from utils.statistics import significance_test, fdr_corrected_pvals


def initialize_empty_columns_at_index(dataframe, row_index):
    # I have to do this ugly thing here because initializing with 3 nans is somehow not possible because pandas sets
    # the dtype of the cell as float instead ob object
    dataframe.loc[row_index, 'config_has_run'] = False
    dataframe.loc[row_index, 'mse_train'] = False
    dataframe.loc[row_index, 'mse_valid'] = False
    dataframe.loc[row_index, 'mse_test'] = False
    dataframe.loc[row_index, 'corr_train'] = False
    dataframe.loc[row_index, 'corr_valid'] = False
    dataframe.loc[row_index, 'corr_test'] = False
    dataframe.loc[row_index, 'corr_p_train'] = False
    dataframe.loc[row_index, 'corr_p_valid'] = False
    dataframe.loc[row_index, 'corr_p_test'] = False
    dataframe.loc[row_index, 'r^2_train'] = False
    dataframe.loc[row_index, 'r^2_valid'] = False
    dataframe.loc[row_index, 'r^2_test'] = False
    return dataframe


def prefill_columns_configuration_at_index(dataframe, row_index, has_run):
    dataframe.loc[row_index, 'config_has_run'] = has_run
    dataframe.loc[row_index, 'mse_train'] = [[np.nan], [np.nan], [np.nan]]
    dataframe.loc[row_index, 'mse_valid'] = [[np.nan], [np.nan], [np.nan]]
    dataframe.loc[row_index, 'mse_test'] = [[np.nan], [np.nan], [np.nan]]
    dataframe.loc[row_index, 'corr_train'] = [[np.nan], [np.nan], [np.nan]]
    dataframe.loc[row_index, 'corr_valid'] = [[np.nan], [np.nan], [np.nan]]
    dataframe.loc[row_index, 'corr_test'] = [[np.nan], [np.nan], [np.nan]]
    dataframe.loc[row_index, 'corr_p_train'] = [[np.nan], [np.nan], [np.nan]]
    dataframe.loc[row_index, 'corr_p_valid'] = [[np.nan], [np.nan], [np.nan]]
    dataframe.loc[row_index, 'corr_p_test'] = [[np.nan], [np.nan], [np.nan]]
    dataframe.loc[row_index, 'r^2_train'] = [[np.nan], [np.nan], [np.nan]]
    dataframe.loc[row_index, 'r^2_valid'] = [[np.nan], [np.nan], [np.nan]]
    dataframe.loc[row_index, 'r^2_test'] = [[np.nan], [np.nan], [np.nan]]
    return dataframe


def fill_results_in_configurations_at_index(dataframe, row_index, df, i_subject):
    if len(df) == 12:
        dataframe.loc[row_index, 'mse_train'][i_subject] = df.values[0, 1]
        dataframe.loc[row_index, 'mse_valid'][i_subject] = df.values[4, 1]
        dataframe.loc[row_index, 'mse_test'][i_subject] = df.values[8, 1]
        dataframe.loc[row_index, 'corr_train'][i_subject] = df.values[1, 1]
        dataframe.loc[row_index, 'corr_valid'][i_subject] = df.values[5, 1]
        dataframe.loc[row_index, 'corr_test'][i_subject] = df.values[9, 1]
        dataframe.loc[row_index, 'corr_p_train'][i_subject] = df.values[2, 1]
        dataframe.loc[row_index, 'corr_p_valid'][i_subject] = df.values[6, 1]
        dataframe.loc[row_index, 'corr_p_test'][i_subject] = df.values[10, 1]
        dataframe.loc[row_index, 'r^2_train'][i_subject] = df.values[3, 1]
        dataframe.loc[row_index, 'r^2_valid'][i_subject] = df.values[7, 1]
        dataframe.loc[row_index, 'r^2_test'][i_subject] = df.values[11, 1]
    elif len(df) == 9:
        print('WARNING! Residual result df missing r^2 (len = 9)!')
        dataframe.loc[row_index, 'mse_train'][i_subject] = df.values[0, 1]
        dataframe.loc[row_index, 'mse_valid'][i_subject] = df.values[3, 1]
        dataframe.loc[row_index, 'mse_test'][i_subject] = df.values[6, 1]
        dataframe.loc[row_index, 'corr_train'][i_subject] = df.values[1, 1]
        dataframe.loc[row_index, 'corr_valid'][i_subject] = df.values[4, 1]
        dataframe.loc[row_index, 'corr_test'][i_subject] = df.values[7, 1]
        dataframe.loc[row_index, 'corr_p_train'][i_subject] = df.values[2, 1]
        dataframe.loc[row_index, 'corr_p_valid'][i_subject] = df.values[5, 1]
        dataframe.loc[row_index, 'corr_p_test'][i_subject] = df.values[8, 1]
    else:
        print('Unknown result df format of len: {}'.format(len(df)))
        exit()
    # if configurations.loc[i_config, 'model_name'] in ['deep4', 'eegnet', 'resnet']:
    #     for column_name in df.columns:
    #         if column_name == 'train_loss':
    #             configurations.loc[i_config, 'mse_train'][i_subject] = df.tail(1)[column_name].values[0]#, 1]
    #         if column_name == 'valid_loss':
    #             configurations.loc[i_config, 'mse_valid'][i_subject] = df.tail(1)[column_name].values[0]#, 2]
    #         if column_name == 'test_loss':
    #             configurations.loc[i_config, 'mse_test'][i_subject] = df.tail(1)[column_name].values[0]#, 3]
    #         if column_name == 'train_corr':
    #             configurations.loc[i_config, 'corr_train'][i_subject] = df.tail(1)[column_name].values[0]#, 4]
    #         if column_name == 'valid_corr':
    #             configurations.loc[i_config, 'corr_valid'][i_subject] = df.tail(1)[column_name].values[0]#, 5]
    #         if column_name == 'test_corr':
    #             configurations.loc[i_config, 'corr_test'][i_subject] = df.tail(1)[column_name].values[0]#, 6]
    # elif configurations.loc[i_config, 'model_name'] in ['lin_reg', 'lin_svr', 'rbf_svr', 'rf_reg']:
    #     dataframe.loc[row_index, 'mse_train'][i_subject] = df.values[0, 1]
    #     dataframe.loc[row_index, 'mse_valid'][i_subject] = df.values[4, 1]
    #     dataframe.loc[row_index, 'mse_test'][i_subject] = df.values[8, 1]
    #     dataframe.loc[row_index, 'corr_train'][i_subject] = df.values[1, 1]
    #     dataframe.loc[row_index, 'corr_valid'][i_subject] = df.values[5, 1]
    #     dataframe.loc[row_index, 'corr_test'][i_subject] = df.values[9, 1]
    #     dataframe.loc[row_index, 'corr_p_train'][i_subject] = df.values[2, 1]
    #     dataframe.loc[row_index, 'corr_p_valid'][i_subject] = df.values[6, 1]
    #     dataframe.loc[row_index, 'corr_p_test'][i_subject] = df.values[10, 1]
    # else:
    #     print('Unknown model name: {}'.format(configurations.loc[i_config, 'model_name']))
    #     break
    return dataframe


def max_of_each_entry(df, label_key, value_key):
    max_value = []
    for unique_label in np.unique(df[label_key]):
        max_value.append(np.max(df[df[label_key] == unique_label][value_key]))

    return max_value


def get_dataframe_values_matching_two_criteria_in_two_columns(dataframe, condition_col, condition_name,
                                                              metric_name_col, metric_name, metric_value_col):
    return dataframe[(dataframe[condition_col] == condition_name)
                     & (dataframe[metric_name_col] == metric_name)][metric_value_col].values


def dataframe_significance_test(dataframe, condition_col, condition_name_a, condition_name_b, metric_name_col,
                                metric_name, metric_value_col):
    a = get_dataframe_values_matching_two_criteria_in_two_columns(dataframe, condition_col, condition_name_a,
                                                                  metric_name_col, metric_name, metric_value_col)
    b = get_dataframe_values_matching_two_criteria_in_two_columns(dataframe, condition_col, condition_name_b,
                                                                  metric_name_col, metric_name, metric_value_col)

    return significance_test(a, b, alpha=0.5, alternative='two-sided', use_continuity=True)


def single_value_row_configurations(configurations, subject_values):
    # Reformat configuration dataframe to have one row per metric value
    single_value_configurations = pd.DataFrame()
    for i_config in range(len(configurations)):
        for metric in ['mse', 'corr', 'corr_p', 'r^2']:
            for data_split in ['train', 'valid', 'test']:
                for i_subject in range(len(subject_values)):
                    single_value_configurations = single_value_configurations.append(
                        pd.DataFrame({'subject_train': subject_values[i_subject],
                                      'subject_apply': subject_values[i_subject],
                                      'data_split': data_split,
                                      'metric_value': configurations[metric + '_' + data_split][i_config][i_subject],
                                      'metric_name': metric,
                                      'data': configurations.loc[i_config, 'data'],
                                      'electrodes': configurations.loc[i_config, 'electrodes'],
                                      'band_pass': configurations.loc[i_config, 'band_pass'],
                                      'model_name': configurations.loc[i_config, 'model_name'],
                                      'unique_id': configurations.loc[i_config, 'unique_id'],
                                      'data_folder': configurations.loc[i_config, 'data_folder'],
                                      'batch_size': configurations.loc[i_config, 'batch_size'],
                                      'max_epochs': configurations.loc[i_config, 'max_epochs'],
                                      'cuda': configurations.loc[i_config, 'cuda'],
                                      'result_folder': configurations.loc[i_config, 'result_folder'],
                                      'init_lr': configurations.loc[i_config, 'init_lr'],
                                      'weight_decay': configurations.loc[i_config, 'weight_decay'],
                                      'sampling_rate': configurations.loc[i_config, 'sampling_rate'],
                                      'n_seconds_valid_set': configurations.loc[i_config, 'n_seconds_valid_set'],
                                      'n_seconds_test_set': configurations.loc[i_config, 'n_seconds_test_set'],
                                      'config_has_run': configurations.loc[i_config, 'config_has_run']}, index=[0]),
                        ignore_index=True)
    return single_value_configurations


def remove_columns_with_same_value(df, exclude=('train',)):
    cols_multiple_vals = []
    for col in df.columns:
        try:
            values_set = set(df[col])
            has_multiple_vals = len(values_set) > 1
            if has_multiple_vals:
                all_nans = np.all(np.isnan(values_set))
        except TypeError:
            all_nans = False
            # transform to string in case there are lists
            # since lists not hashable to set
            has_multiple_vals = len(set([str(val) for val in df[col]])) > 1
        cols_multiple_vals.append((has_multiple_vals and (not all_nans)))
    cols_multiple_vals = np.array(cols_multiple_vals)
    excluded_cols = np.array([c in exclude for c in df.columns])
    df = df.iloc[:, (cols_multiple_vals | excluded_cols)]
    return df


def print_performance_matrix(dataframe,
                             x_col,
                             y_col,
                             metric_name_col,
                             metric_name,
                             metric_value_col,
                             averaging_func=np.median,
                             transformation_func=lambda x: x,
                             fmt=':3f'):
    performance_matrix = compute_performance_matrix(dataframe,
                                                    x_col,
                                                    y_col,
                                                    metric_name_col,
                                                    metric_name,
                                                    metric_value_col,
                                                    averaging_func=averaging_func,
                                                    transformation_func=transformation_func)[0]
    # format(performance_matrix, fmt)
    # latex_tabular = " \\\\\n".join([" & ".join(map(str, line)) for line in performance_matrix])
    print(" \\\\\n".join([" & ".join(map('{0:.3f}'.format, line)) for line in performance_matrix]))
    # print(latex_tabular.)


def compute_performance_matrix(dataframe,
                               x_col,
                               y_col,
                               metric_name_col,
                               metric_name,
                               metric_value_col,
                               averaging_func=np.median,
                               transformation_func=lambda x: x):
    x_values, x_indices = np.unique(dataframe[x_col], return_index=True)
    x_values = x_values[np.argsort(x_indices)]
    x_indices = range(len(x_values))
    y_values, y_indices = np.unique(dataframe[y_col], return_index=True)
    y_values = y_values[np.argsort(y_indices)]
    y_indices = range(len(y_values))
    performance_matrix = np.ndarray((len(x_indices), len(y_indices)))
    for x, y in it.product(range(len(x_indices)), range(len(y_indices))):
        a = transformation_func(dataframe[(dataframe[x_col] == x_values[x]) &
                                          (dataframe[y_col] == y_values[y]) &
                                          (dataframe[metric_name_col] == metric_name)][metric_value_col].values)
        if np.size(a) > 1:
            performance_matrix[x, y] = averaging_func(a)
        else:
            performance_matrix[x, y] = a
    return performance_matrix, x_values, y_values


def compute_diff_matrix(dataframe, condition_col, metric_name_col='metric_name', metric_name='rmse',
                        metric_value_col='metric_value', averaging_func=np.median):
    condition_values, condition_indices = np.unique(dataframe[condition_col], return_index=True)
    condition_values = condition_values[np.argsort(condition_indices)]
    condition_indices = range(len(condition_values))
    diff_matrix = np.ndarray((len(condition_indices), len(condition_indices)))
    significance_matrix = np.ndarray(diff_matrix.shape)
    for x, y in it.product(range(len(condition_indices)), range(len(condition_indices))):
        a = get_dataframe_values_matching_two_criteria_in_two_columns(
            dataframe,
            condition_col,
            condition_values[x],
            metric_name_col,
            metric_name,
            metric_value_col)
        b = get_dataframe_values_matching_two_criteria_in_two_columns(
            dataframe,
            condition_col,
            condition_values[y],
            metric_name_col,
            metric_name,
            metric_value_col)
        if np.size(a) >= 10:
            diff_matrix[x, y] = averaging_func(a) - averaging_func(b)
        else:
            diff_matrix[x, y] = averaging_func(a - b)
        significance_matrix[x, y] = significance_test(a, b, alpha=0.5, alternative='two-sided', use_continuity=True)
    tril_indices = np.tril_indices_from(significance_matrix, k=-1)
    significance_matrix[tril_indices] = fdr_corrected_pvals(significance_matrix[tril_indices])
    return diff_matrix, significance_matrix, condition_values


def expand_row_with_multiple_values(df, column):
    new_df = df
    for row in df.index:
        for column in df.iloc[row]:
            tmp = np.size(column)
            if tmp > 1:
                new_df

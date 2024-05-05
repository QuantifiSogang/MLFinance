import pandas as pd
import numpy as np
from numba import jit, prange

def get_indicator_matrix(bar_idx, t1) :
    indM = pd.DataFrame(
        0,
        index = bar_idx,
        columns = range(t1.shape[0])
    )
    for i, (t0, t1) in enumerate(t1.items()) :
        indM.loc[t0:t1, i] = 1.
    return indM

def ind_matrix(samples_info_sets, price_bars):
    if bool(samples_info_sets.isnull().values.any()) is True or bool(
            samples_info_sets.index.isnull().any()) is True:
        raise ValueError('NaN values in triple_barrier_events, delete nans')

    triple_barrier_events = pd.DataFrame(samples_info_sets)
    trimmed_price_bars_index = price_bars[(price_bars.index >= triple_barrier_events.index.min()) &
                                          (price_bars.index <= triple_barrier_events.t1.max())].index

    label_endtime = triple_barrier_events.t1
    bar_index = list(triple_barrier_events.index)
    bar_index.extend(triple_barrier_events.t1)
    bar_index.extend(trimmed_price_bars_index)
    bar_index = sorted(list(set(bar_index)))
    sorted_timestamps = dict(zip(sorted(bar_index), range(len(bar_index))))

    tokenized_endtimes = np.column_stack((label_endtime.index.map(sorted_timestamps), label_endtime.map(
        sorted_timestamps).values))

    ind_mat = np.zeros((len(bar_index), len(label_endtime)))
    for sample_num, label_array in enumerate(tokenized_endtimes):
        label_index = label_array[0]
        label_endtime = label_array[1]
        ones_array = np.ones(
            (1, label_endtime - label_index + 1))
        ind_mat[label_index:label_endtime + 1, sample_num] = ones_array
    return ind_mat


def ind_mat_average_uniqueness(ind_mat):
    concurrency = ind_mat.sum(axis=1)
    uniqueness = ind_mat.T / concurrency

    avg_uniqueness = uniqueness[uniqueness > 0].mean()

    return avg_uniqueness

def ind_mat_label_uniqueness(ind_mat):
    concurrency = ind_mat.sum(axis=1)
    uniqueness = ind_mat.T / concurrency

    return uniqueness

@jit(parallel=True, nopython=True)
def _bootstrap_loop_run(ind_mat, prev_concurrency):
    # Initialize the average uniqueness array
    avg_unique = np.zeros(ind_mat.shape[1])

    # Calculate the average uniqueness for each column
    for i in prange(ind_mat.shape[1]):
        prev_average_uniqueness = 0
        number_of_elements = 0
        reduced_mat = ind_mat[:, i]
        for j in range(len(reduced_mat)):
            if reduced_mat[j] > 0:
                new_el = reduced_mat[j] / (reduced_mat[j] + prev_concurrency[j])
                average_uniqueness = (prev_average_uniqueness * number_of_elements + new_el) / (number_of_elements + 1)
                number_of_elements += 1
                prev_average_uniqueness = average_uniqueness
        avg_unique[i] = prev_average_uniqueness
    return avg_unique

def seq_bootstrap(
        ind_mat,
        sample_length=None,
        warmup_samples=None,
        compare=False,
        verbose=False,
        random_state=None):
    # Ensure the random state is initialized properly
    if random_state is None:
        random_state = np.random.RandomState()

    # Set default sample length to the number of columns
    if sample_length is None:
        sample_length = ind_mat.shape[1]

    # Initialize warmup_samples if not provided
    if warmup_samples is None:
        warmup_samples = []

    phi = []
    prev_concurrency = np.zeros(ind_mat.shape[0])
    while len(phi) < sample_length:
        avg_unique = _bootstrap_loop_run(ind_mat, prev_concurrency)
        prob = avg_unique / np.sum(avg_unique)
        try:
            choice = warmup_samples.pop(0)
        except IndexError:
            choice = random_state.choice(range(ind_mat.shape[1]), p=prob)
        phi.append(choice)
        prev_concurrency += ind_mat[:, choice]
        if verbose:
            print("Probabilities: ", prob)

    if compare:
        standard_indx = random_state.choice(ind_mat.shape[1], size=sample_length, replace=False)
        # Assuming ind_mat_average_uniqueness is defined somewhere
        standard_unq = ind_mat_average_uniqueness(ind_mat[:, standard_indx])
        sequential_unq = ind_mat_average_uniqueness(ind_mat[:, phi])
        print('Standard uniqueness: {}\nSequential uniqueness: {}'.format(standard_unq, sequential_unq))

    return phi

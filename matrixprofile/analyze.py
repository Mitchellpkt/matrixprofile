# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

range = getattr(__builtins__, 'xrange', range)
# end of py2 compatability boilerplate

import math

from matrixprofile.algorithms.top_k_discords import top_k_discords
from matrixprofile.algorithms.top_k_motifs import top_k_motifs
from matrixprofile.aglorithms import skimp
from matrixprofile.algorithms.mpx import mpx
from matrixprofile.algorithms.scrimp import scrimp_plus_plus
from matrixprofile.visualize import plot_mp


def analyze_pmp(ts, query, sample_pct, threshold, windows=None, n_jobs=-1):
	ts = core.to_np_array(ts)

	# when a threshold is passed, we compute the upper window
	if isinstance(windows, type(None)):
		upper_w = maximum_subsequence(ts, threshold)

		# determine windows to be computed
		# from 8 in steps of 2 until upper w
		start = 8
        end = int(math.floor(len(ts) / 2))
        windows = range(start, upper_w + 1)

    # compute the pmp
    pmp, idx, windows = skimp.skimp(ts, windows=windows, sample_pct=sample_pct)

    # TODO: These need to be implemented
    # extract top motifs
    # extract top discords    
    # plot top motifs
    # plot top discords

    # plot pmp
    pmp_plot = skimp.plot_pmp(pmp)

    return None # TODO!!!!!!!


def analyze_mp_exact(ts, query, window, n_jobs=-1):
	ts = core.to_np_array(ts)

	# compute mp
	profile = mpx(ts, query, window, n_jobs=n_jobs)

	# extract top motifs
	motifs = top_k_motifs(ts, profile)

	# extract top discords
	discords = top_k_discords(profile)

	# plot mp
	mp_plot = plot_mp(profile, data=ts)

	# TODO: need to figure out discord and motif plotting
	# plot top motifs

	# plot top discords

	return None # TODO!!!!!!!


def analyze_mp_approximate(ts, query, window, sample_pct, n_jobs=-1):
	ts = core.to_np_array(ts)

	# compute mp
	# TODO: scrimp++ is currently based on runtime and not sample pct!!!
	profile = scrimp_plus_plus(ts, query, window, sample_pct=sample_pct, n_jobs=n_jobs)

	# extract top motifs
	motifs = top_k_motifs(ts, profile)

	# extract top discords
	discords = top_k_discords(profile)

	# plot mp
	mp_plot = plot_mp(profile, data=ts)

	# TODO: need to figure out discord and motif plotting
	# plot top motifs

	# plot top discords

	return None # TODO!!!!!!!


def analyze(ts, query=None, windows=None, sample_pct=1.0, threshold=None, n_jobs=-1):
	"""
	TODO: Figure out if we should have parameters that allow end users to tweak
	the discord and motif parameters. Right now I think that it would be a
	"power user" thing.


	Runs an appropriate workflow based on the parameters passed in. The goal
	of this function is to compute all fundamental algorithms on the provided
	time series data. For now the following is computed:

	1. Matrix Profile - exact or approximate based on sample_pct given that a
	   window is provided.
	2. Top Motifs
	3. Top Discords
	4. Plot MP, Motifs and Discords

	When a window is not provided or more than a single window is provided,
	the PMP is computed:

	1. Compute UPPER window when no window is provided
	2. Compute PMP for all windows
	3. Top Motifs
	4. Top Discords
	5. Plot PMP, motifs and discords.
	"""
	result = None

	# determine what algorithm to use based on params
	no_window = isinstance(windows, type(None))
	many_windows = core.is_array_like(windows) and len(windows) > 1
	single_window = isinstance(windows, int) or \
		(core.is_array_like(windows) and len(windows) == 1)
	is_exact = sample_pct >= 1
	is_approx = sample_pct > 0 and sample_pct < 1

	# use PMP with no window provided
	if no_window or many_windows:
		result = analyze_pmp(ts, query, sample_pct, threshold, windows=windows, n_jobs=n_jobs)
	elif single_window and is_exact:
		result = analyze_mp_exact(ts, query, window, n_jobs=n_jobs)
	elif single_window and is_approx:
		result = analyze_mp_approximate(ts, query, window, sample_pct, n_jobs=n_jobs)
	else:
		raise RuntimeError('Param combination resulted in an uknown operation')

	return result
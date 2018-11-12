import os, sys
import numpy as np
import h5py
import json

from seg_watershed import watershed
from seg_util import create_border_mask, writeh5
from waterz import agglomerate

def getScoreFunc(scoreF):
    # aff50_his256
    config = {x[:3]: x[3:] for x in scoreF.split('_')}
    if 'aff' in config:
        if 'his' in config and config['his']!='0':
            return 'OneMinus<HistogramQuantileAffinity<RegionGraphType, %s, ScoreValue, %s>>' % (config['aff'],config['his'])
        else:
            return 'OneMinus<QuantileAffinity<RegionGraphType, '+config['aff']+', ScoreValue>>'
    elif 'max' in config:
            return 'OneMinus<MeanMaxKAffinity<RegionGraphType, '+config['max']+', ScoreValue>>'

def waterz(
        affs,
        thresholds,
        output_prefix = './',
        merge_function = None,
        gt = None,
        gt_border = 25/4.0,
        fragments = None,
        discretize_queue = 256,
        fragments_mask = None,
        aff_threshold  = [0.0001,0.9999],
        return_seg = True):

    # affs shape: 3*z*y*x
    thresholds = list(thresholds)
    print "waterz at thresholds " + str(thresholds)

    if fragments is None:
        fragments = watershed(affs, 'maxima_distance')
        if fragments_mask is not None:
            fragments[fragments_mask==False] = 0
    outs=[]
    if gt is not None and gt_border !=0:
        gt = create_border_mask(gt, gt_border, np.uint64(0))

    for i,out in enumerate(agglomerate(
            affs,
            thresholds,
            gt = gt,
            aff_threshold_low  = aff_threshold[0],
            aff_threshold_high = aff_threshold[1],
            fragments=fragments,
            scoring_function=getScoreFunc(merge_function),
            discretize_queue=discretize_queue,
            force_rebuild=True)):

        threshold = thresholds[i]
        output_basename = output_prefix+merge_function+'_%.2f'%threshold
        if gt is not None:
            seg = out[0]
        else:
            seg = out
        if return_seg:
            outs.append(seg.copy())
        else:
            print "Storing segmentation..."
            writeh5(output_basename + '.hdf', 'main', seg)
        if gt is not None:
            metrics = out[1]
            print "Storing record..."
            record = {
                'threshold': threshold,
                'merge_function': merge_function,
                'custom_fragments': custom_fragments,
                'discretize_queue': discretize_queue,
                'voi_split': metrics['V_Info_split'],
                'voi_merge': metrics['V_Info_merge'],
                'rand_split': metrics['V_Rand_split'],
                'rand_merge': metrics['V_Rand_merge'],
            }
            with open(output_basename + '.json', 'w') as f:
                json.dump(record, f)
    if return_seg:
        return outs

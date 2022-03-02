"""
adapted from Seisbench tutorial 01b_model_api.ipynb

This tutorial introduces the SeisBench model API. It explains how to load pretrained models and apply them to generate characteristic curves or discrete picks.

"""

print('===IMPORTS===')
import obspy
import seisbench
import seisbench.models as sbm
import torch
import util
import os
import pickle
root = '/home/earthquakes1/homes/Rebecca/phd/data/2018_2021_global_m5/'
print('=== IMPORTS FINISHED ===')

"""### Loading pretrained models

SeisBench offers pretrained models, which can be loaded with the `from_pretrained` method. To list available pretrained models, we can use `list_pretrained`. By setting `details=True`, we also get a docstring for each model.
pretrained_weights = sbm.GPD.list_pretrained(details=True)
for key, value in pretrained_weights.items():
    print(f"{key}:\n{value}\n-----------------------\n")
    
### Model interchangability

The standardized model API makes it easy to use different models. Let's try out EQTransformer. For this, we use the pretrained weights from Mousavi et al. (2020). Note that in addition to picks, EQTransformer returns detections.
"""

print('LOADING MODEL')
model = sbm.EQTransformer.from_pretrained("original")
#model = sbm.GPD.from_pretrained("original") # try GPD instead but that doesn't work either :(
print(model.weights_docstring)

print('=== FINISHED LOADING MODEL ===')

"""### Annotating waveform streams

SeisBench models can directly annotate obspy streams.
SeisBench models can generate characteristic curves, i.e., curves providing the probability of a pick at a certain time. For this, the annotate function is used.
Annotate automatically transforms the trace into a compatible format for the model and merges the preditions into traces.
For example, annotate will determine the correct component order and resample the trace to the required sampling rate.

### Batch processing

Processing is not limited to a single station, but can be applied to streams from different stations. SeisBench will automatically convert the traces into the correct tensors and the annotations back to streams.
For more efficient processing, let's first move the model to GPU. Moving a model to GPU will automatically process the computations of `annotate` and `classify` on GPU.

**Note:** This command will fail, if you do not have a properly configured GPU. In this case, just skip it.
"""

#print('=== WORK ON GPU ===')
#model.cuda();
#print('=== FINISH WORK ON GPU ===')


def save_obj(obj, eq_name):  # normally in utils but copy here for now
    with open(root+'/'+eq_name+'/picks.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)
        
print('===load cat===')        
cat = obspy.read_events('/home/earthquakes1/homes/Rebecca/phd/data/2018_2021_global_m5_catalog.xml')
# download_data(cat)

print('===eq with data===')
eq_with_data = []
for event in cat:
    eq_name = util.catEventToFileName(event)
    if os.path.isdir(root+eq_name) and os.path.isdir(root+eq_name+'/station_xml_files'):
        eq_with_data.append(eq_name)

print('===do===')
count = 0
for eq_name in eq_with_data[1:2]:
    print('earthquake number' + str(count) + 'done. It was' + eq_name)
    stream = obspy.read(root+eq_name+'/data/*/*')
    
    picks, detections = model.classify(stream)
    
    # save picks in pickled dictionary
    picks_dict = {}
    for pick in picks:
        #print(pick)
        #print(pick.trace_id)
        pick_dist = stream[0].stats.starttime - pick.peak_time
        if pick.phase=='P' and pick.trace_id not in picks_dict.keys() and abs(pick_dist)>200 and abs(pick_dist)<400: # how to deal with more than one earthquake
            picks_dict[pick.trace_id]=pick.peak_time
            #print('first pick')
        elif pick.phase=='P' and pick.trace_id in picks_dict.keys():
            #print('in elif')
            current_pick = picks_dict[pick.trace_id]
            current_dist = stream[0].stats.starttime - current_pick
            #print(current_pick, current_dist)
            
            #print(pick.peak_time, pick_dist)
            min_dist = min([current_dist, pick_dist], key=lambda x:abs(abs(x)-300))
            #print(min_dist)
            if min_dist == pick_dist:
                #print('if true')
                picks_dict[pick.trace_id]=pick.peak_time
            else:
                continue
                #print('current stands')
        else:
            continue
            #print('must be S')
    count += 1
    save_obj(picks_dict, eq_name)
    print('SAVED')
    

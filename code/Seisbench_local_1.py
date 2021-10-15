"""# Model API

This tutorial introduces the SeisBench model API. It explains how to load pretrained models and apply them to generate characteristic curves or discrete picks.

**Note:** Some familiarity with obspy is helpful for this tutorial, but not required.
"""
import obspy
import seisbench
import seisbench.models as sbm
import torch

"""### Loading pretrained models

The model created above consisted of random weights, i.e., it was not trained. While this is (often) the right approach when starting to train a model, for application we'll need a trained model. SeisBench offers pretrained models, which can be loaded with the `from_pretrained` method. To list available pretrained models, we can use `list_pretrained`. By setting `details=True`, we also get a docstring for each model.

### Model interchangability

The standardized model API makes it easy to use a different model. Let's try out EQTransformer. For this, we use the pretrained weights from Mousavi et al. (2020). Note that in addition to picks, EQTransformer returns detections.
"""
model = sbm.EQTransformer.from_pretrained("original")
print(model.weights_docstring)
"""### Annotating waveform streams

SeisBench models can directly annotate obspy streams. Let's download a 200 s long piece of waveforms from a station in Chile through FDSN and visualize it.

SeisBench models can generate characteristic curves, i.e., curves providing the probability of a pick at a certain time. For this, the annotate function is used. Annotate automatically transforms the trace into a compatible format for the model and merges the preditions into traces. For example, annotate will determine the correct component order and resample the trace to the required sampling rate.

### Batch processing

Processing is not limited to a single station, but can be applied to streams from different stations. SeisBench will automatically convert the traces into the correct tensors and the annotations back to streams. For more efficient processing, let's first move the model to GPU. Moving a model to GPU will automatically process the computations of `annotate` and `classify` on GPU.

**Note:** This command will fail, if you do not have a properly configured GPU. In this case, just skip it.
"""

model.cuda();

"""Now let's download the same time window as above, but for all stations in the CX network and generate the picks and detections with EQTransformer."""
def save_obj(obj, eq_name):
    with open(root+'/'+eq_name+'/picks.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)
        
cat = obspy.read_events('/home/earthquakes1/homes/Rebecca/phd/data/2019_global_m5_catalog.xml')
# download_data(cat)

eq_with_data = []
for event in cat:
    eq_name = util.catEventToFileName(event)
    if os.path.isdir(root+eq_name) and os.path.isdir(root+eq_name+'/station_xml_files'):
        eq_with_data.append(eq_name)
        
for eq_name in eq_with_data[:1]:
    stream = obspy.read(root+eq_name+'/data/*/*')
    
    picks, detections = model.classify(stream)
    
    # save picks in pickled dictionary
    picks_dict = {}
    for pick in picks:
        if pick.phase=='P':
            picks_dict[pick.trace_id]=pick.peak_time
    save_obj(picks, eq_name)

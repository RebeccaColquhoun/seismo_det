# based on seisbench example code
import obspy
import seisbench
import seisbench.models as sbm
import util
import os
import pickle
import setup_paths as paths
import matplotlib.pyplot as plt


root_path = '/home/earthquakes1/homes/Rebecca/phd/data/'

subfolders = ['2018_2021_global_m5', '2019_global_m3', '2005_2018_global_m5']

folder = subfolders[0]

root = os.path.join(root_path, folder)
seisbench.use_backup_repository()
# load EQT model
model = sbm.EQTransformer.from_pretrained("original", update=True)

# print model weights
print(model.weights_docstring)

def save_obj(obj, eq_name):
	with open(root + '/' + eq_name + '/picks_for_uncertainty.pkl', 'wb') as f:
		pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


print('===load cat===')
cat = obspy.read_events(root + '_catalog.xml')


print('===eq with data===')
# find which earthquakes have data and station responses
eq_with_data = []
mags = []
for event in cat:
	eq_name = util.catEventToFileName(event)
	
	print(eq_name)
	print(os.path.isdir(root + '/' + eq_name))
	print(os.path.isdir(root + '/' + eq_name + '/station_xml_files'))
	if os.path.isdir(root + '/' + eq_name) and os.path.isdir(root + '/' + eq_name + '/station_xml_files'):
		eq_with_data.append(eq_name)
		mags.append(event.magnitudes[0].mag)
print(eq_with_data)	# if count >=10:
	# 	break


count = 0
for eq_name, mag in zip(eq_with_data, mags):
	# if count >=10:
	# 	break
	try:
		print(eq_name)
		stream = obspy.read(root + '/' + eq_name + '/data/*/*')
		annotations = model.annotate(stream)
		print(annotations)
		print('earthquake number' + str(count) + 'done. It was' + eq_name)
		
		fig = plt.figure(figsize=(15, 10))
		axs = fig.subplots(1, 1, sharex=True, gridspec_kw={'hspace': 0})
		ax2 = axs.twinx()

		offset = annotations[0].stats.starttime - stream[0].stats.starttime
		for i in range(3):
			axs.plot(stream[i].times(), stream[i].data, label=stream[i].stats.channel, alpha=0.2)
			if annotations[i].stats.channel[-1] != "N":  # Do not plot noise curve
				ax2.plot(annotations[i].times() + offset, annotations[i].data, label=annotations[i].stats.channel)

		# Calculate STA/LTA
		sta_lta = obspy.signal.trigger.classic_sta_lta(stream[0].data, nsta=50, nlta=1000)
		ax2.plot(stream[0].times(), sta_lta, label='STA/LTA', color='r')
		ax2.set_ylim(-1,1)
		ax2.legend()

		axs.set_title(eq_name + '; M' + str(mags[count]))
		plt.savefig('/home/earthquakes1/homes/Rebecca/phd/seismo_det/figures/pick_uncert_figures_50_1000/' + str(mag) + '_' + eq_name + '.png')
		plt.show()
		plt.close()
	except Exception as e:
		print(e)
		continue
	count += 1
mags

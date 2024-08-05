# based on seisbench example code
import obspy
import seisbench
import seisbench.models as sbm
import util
import os
import pickle
import setup_paths as paths

root_path = paths.data_path

subfolders = paths.data_subfolders

for folder in subfolders:
    root = os.path.join(root_path, folder)
    seisbench.use_backup_repository()
    # load EQT model
    model = sbm.EQTransformer.from_pretrained("original", update=True)

    # print model weights
    print(model.weights_docstring)

    def save_obj(obj, eq_name):
        with open(root + '/' + eq_name + '/picks.pkl', 'wb') as f:
            pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

    print('===load cat===')
    cat = obspy.read_events(root + '_catalog.xml')

    print('===eq with data===')
    # find which earthquakes have data and station responses
    eq_with_data = []
    for event in cat:
        eq_name = util.catEventToFileName(event)
        print(eq_name)
        print(os.path.isdir(root + '/' + eq_name))
        print(os.path.isdir(root + '/' + eq_name + '/station_xml_files'))
        if os.path.isdir(root + '/' + eq_name) and os.path.isdir(root + '/' + eq_name + '/station_xml_files'):
            eq_with_data.append(eq_name)
    print(eq_with_data)

    count = 0
    # for each earthquake with data, pick P wave and save picks
    for eq_name in eq_with_data:
        try:
            print(eq_name)
            if os.path.exists(root + '/' + eq_name + '/picks.pkl') is False:
                print('earthquake number' + str(count) + 'done. It was' + eq_name)
                stream = obspy.read(root + '/' + eq_name + '/data/*/*')

                output = model.classify(stream)
                picks = output.picks
                detections = output.detections

                # interpret and save picks in pickled dictionary
                picks_dict = {}
                picks_samples = {}
                for pick in picks:
                    pick_dist = stream[0].stats.starttime - pick.peak_time
                    if (pick.phase == 'P'
                            and pick.trace_id not in picks_dict.keys()
                            and abs(pick_dist) > 200 and abs(pick_dist) < 400):
                        picks_dict[pick.trace_id] = pick.peak_time
                    elif pick.phase == 'P' and pick.trace_id in picks_dict.keys():
                        current_pick = picks_dict[pick.trace_id]
                        current_dist = stream[0].stats.starttime - current_pick
                        min_dist = min([current_dist, pick_dist], key=lambda x: abs(abs(x) - 300))
                        if min_dist == pick_dist:
                            picks_dict[pick.trace_id] = pick.peak_time
                            picks_samples[pick.trace_id] = pick.peak_time - stream[0].stats.starttime
                        else:
                            continue
                    else:
                        continue
                count += 1
                save_obj(picks_dict, eq_name)
                print('SAVED')
            else:
                print('already done')
                print(eq_name)
        except Exception:
            print('unsuitable in some way, onto next earthquake')
            continue

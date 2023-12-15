import numpy as np
import math
import lxml.etree as et
import pandas as pd
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QFileDialog, QMessageBox
import os

def primprocess(first, last, pp_mu, pp_dead_t, region_grid):
    # Generates a set of primary spatio-temporal events between first and last.
    # The time intervals between events are exponentially distributed with
    # mean pp_mu. The events are then uniformly distributed between the segments
    # of the region_grid, which serve as a constrain box for randomly selecting
    # the (x, y) location.
    # The pp_dead_t is the dead time after an event. It helps to avoid having 2
    # events ocurring at the exact same time. Finally, the times are given in seconds.
    events = np.array([first])
    aveInt = pp_mu + pp_dead_t

    # Generate all the primary processes between first and lastInp
    # drawing the interval between event from an exponential
    # distribution
    while events[-1] < last:
        numInts = int(np.round((last - events[-1]) / aveInt)) + 1
        newInts = np.random.exponential(scale=pp_mu, size=numInts) + pp_dead_t
        newInts = np.cumsum(newInts)
        events = np.concatenate([events, newInts + events[-1]])

    # Include only events between first and lastInp
    if events[-1] > last:
        events = events[events <= last]

    # Add spatial dimension to the primary process.
    # Create a numpy array of uniformly distributed random segments drawn
    # from the region_grid
    n = len(events)

    rand_segments = region_grid[np.random.randint(0, len(region_grid), n)]
    # Generate x and y from the 2 corners defined in each segment
    x = np.random.uniform(rand_segments[:,0,0], rand_segments[:,1,0])
    y = np.random.uniform(rand_segments[:,0,1], rand_segments[:,1,1])

    return np.column_stack((np.round(events).astype(np.int64), x, y))


def add_types(events, type_ratios):
    # We will uniformily distribute the events between 3 types: EMS, Fire, and Law.
    # Assigned a number from 0 to 99 using a uniform distribution, which will be
    # used as a threshold for randomly selecting the the emergency type based
    # on their type_ratios.
    random_ratio = np.random.randint(0, 100, events.shape[0])
    
    # With the ratios sorted in ascending order we set thresholds for the various
    # incident types using their cummulative sum. For instance, if we have ratios of
    # 15% EMS, 15% Fire, and 70% Law; we assign EMS when the uniformly distributed
    # random variable gets a value less than 15, Fire is assigned when it gets a
    # value between 15 and 29, and Law for values between 30 and 99.
    prev_threshold = 0
    cond_list = []
    choice_list = []
    for key, value in sorted(type_ratios.items(), key=lambda x:x[1]):
        threshold = prev_threshold + value * 100
        cond_list.append(random_ratio < threshold)
        # print('Threshold:', key, '= ', threshold)
        choice_list.append(key)
        prev_threshold = threshold
        
    type_list = np.select(cond_list, choice_list)
    return np.column_stack((events, type_list.astype('object')))


def secprocess(sp_sigma, duration_mean, duration_min, patience_mean, onsite_mean, prototypes,
               prim_evts):
    # Secondary process for clustering. Selects a prototype
    # from the dictionary of prototypes, which is used as the magnitude
    # an spread of the primary event. This determines the number of 
    # secondary events generated and their distribution in space.
    # It then generates a secondary point process by attaching
    # to each event in prim_evts a new cluster, with the interval between the
    # primary event and each secondary event being taken from an exponential
    # distribution with mean sp_sigma.
    # 
    # Each secondary events gets a duration drawn from an exponential
    # distribution with mean duration_mean, and a location (x, y) according
    # to the selected prototype.
    #
    # It returns the secondary events containing:
    # [time, duration, x, y, type].

    # Constraints:
    # 1. Values drawn from an exponential distribution get their outliers removed.
    #    The outliers are determines using Tukey's Fence criteria for the upper fence,
    #    calculated as (ln(4) + 1.5 * ln(3)) * SPSigma

    # The prototypes are selected base of 4 classes (0-3) where:
    #   class 0 = 40% of events
    #   class 1 = 50% of events
    #   class 2 = 9% of events
    #   class 3 = 1% of events
    # Each of this classes has a mean and standard deviation for the radius
    # and intensity of the generated secondary process
    proto_class = np.random.rand(len(prim_evts))
    proto_class[(proto_class >= 0.99)] = 3
    proto_class[proto_class < 0.4] = 0
    proto_class[(proto_class >= 0.4) & (proto_class < 0.9)] = 1
    proto_class[(proto_class >= 0.9) & (proto_class < 0.99)] = 2

    sec_evts_t = np.zeros(0) #np.zeros(len(primEvts) * expected_points_num)
    sec_evts_x = np.zeros(0) #np.zeros(len(primEvts) * expected_points_num)
    sec_evts_y = np.zeros(0) #np.zeros(len(primEvts) * expected_points_num)
    sec_evts_cid = np.zeros(0)

    # We need to compute the actual clusters on a per primary event basis
    for pe_num in range(len(prim_evts)):
        # get the radius and intensity
        pcls = proto_class[pe_num]
        # print('protoclass:', pcls)
        radius = np.random.normal(prototypes[pcls]['mu_r'],
                                  prototypes[pcls]['sdev_r'],
                                  size=1)[0]
        intensity = np.random.normal(prototypes[pcls]['mu_intensity'],
                                     prototypes[pcls]['sdev_intensity'],
                                     size=1)[0]
        
        expected_points_num = int(intensity * np.pi * radius**2)
        # Ensure that at least 1 call is generated
        if expected_points_num == 0:
            expected_points_num = 1
        
        # Use Tukey's boxplot method for calculating the fence for the outliers. Based on
        # Sim et al. (2005), the lower fence for an exponential distribution is effectively 0.
        # therefore, we only need to calculate the upper fence. The upper fence is calculated
        # as 1.5 times the interquartile range (IQR) above the third quartile (Q3), for an
        # exponential distribution those values are estimated as follows:
        #   UF = Q3 + 1.5 * IQR
        #   lambda = 1/scale_parameter
        #   Q3 = ln(4)/lambda = ln(4) * scale_parameter
        #   IQR = ln(3)/lambda = ln(3) * scale_parameter
        upper_fence = (math.log(4) + 1.5 * math.log(3)) * sp_sigma

        # Generate the clusters
        actClust = np.random.exponential(scale=sp_sigma, size=expected_points_num)
        outliers = np.where(actClust > upper_fence)[0]
        while len(outliers) > 0:
            actClust[outliers] = np.random.exponential(scale=sp_sigma, size=len(outliers))
            outliers = np.where(actClust > upper_fence)[0]
        
        sec_evts_t_tmp = prim_evts[pe_num][0] + actClust.reshape(expected_points_num)
        sec_evts_t = np.append(sec_evts_t, sec_evts_t_tmp)

        # We will locate the secondary events within a circle, with the primary event at the center
        center_x = prim_evts[pe_num][1]
        center_y = prim_evts[pe_num][2]

        # Generate polar coordinates in the circle
        r = np.random.uniform(0, radius, size=expected_points_num)
        theta = np.random.uniform(0, 2*np.pi, size=expected_points_num)

        # convert polar to Cartesian coordinates
        sec_evts_x_tmp = center_x + r * np.cos(theta)
        sec_evts_x = np.append(sec_evts_x, sec_evts_x_tmp)
        sec_evts_y_tmp = center_y + r * np.sin(theta)
        sec_evts_y = np.append(sec_evts_y, sec_evts_y_tmp)

        # assign the type of the primary event
        e_type = prim_evts[pe_num][3]
        sec_evts_cid = np.append(sec_evts_cid, np.full(expected_points_num, e_type))
        
    # Sort events by time, keeping x and y in sync
    indices = np.argsort(sec_evts_t)
    sec_evts_t = sec_evts_t[indices]
    sec_evts_x = sec_evts_x[indices]
    sec_evts_y = sec_evts_y[indices]
    sec_evts_cid = sec_evts_cid[indices]

    # Draw call duration from an exponential distribution.
    # We also trim outliers using the Tukey's Fences criteria
    duration_fence = (math.log(4) + 1.5 * math.log(3)) * duration_mean
    sec_evts_duration = np.random.exponential(scale=duration_mean, size=len(sec_evts_t))
    outliers = np.where(sec_evts_duration > duration_fence)[0]
    while len(outliers) > 0:
        sec_evts_duration[outliers] = np.random.exponential(scale=duration_mean, size=len(outliers))
        outliers = np.where(sec_evts_duration > duration_fence)[0]

    # Shift call duration distribution to the right by duration_min seconds to
    # avoid calls with 0 duration
    sec_evts_duration = sec_evts_duration + duration_min

    # Add exponentially distributed patience time
    sec_evts_patience = np.random.exponential(scale=patience_mean, size=len(sec_evts_t))
    # Add exponentially distributed on_site_time
    sec_evts_onsite_time = np.random.exponential(scale=onsite_mean, size=len(sec_evts_t))

    # Reshape numpy arrays so we can concatenate them column wise
    sec_evts_t = sec_evts_t.reshape(-1, 1)
    sec_evts_x = sec_evts_x.reshape(-1, 1)
    sec_evts_y = sec_evts_y.reshape(-1, 1)
    sec_evts_cid = sec_evts_cid.reshape(-1, 1)
    sec_evts_duration = sec_evts_duration.reshape(-1, 1)
    sec_evts_patience = sec_evts_patience.reshape(-1, 1)
    sec_evts_onsite_time = sec_evts_onsite_time.reshape(-1, 1)

    sec_evts = np.concatenate((np.round(sec_evts_t).astype(np.int64),
                               sec_evts_duration.astype(np.int64),
                               sec_evts_x.astype(np.float64),
                               sec_evts_y.astype(np.float64),
                               sec_evts_cid.astype(object),
                               sec_evts_patience.astype(np.int64),
                               sec_evts_onsite_time.astype(np.int64)),
                               axis=1)

    return pd.DataFrame(sec_evts, columns=['time', 'duration', 'x', 'y', 'type', 'patience',
                                           'on_site_time'])
 

def add_vertex_events(node, vertex_id, vertex_name, data):
    # Adds all rows in data as event elements of a vertex to
    # the given xml element tree node.
    # The vertex node gets the vertex_id as vertex_name as attributes,
    # and each event will have: time, duration, x, y, type, and vertex_id as
    # element attribues.
    vertex = et.SubElement(node, 'vertex', {'id': vertex_id, 'name': vertex_name})
    # This is to make sure we don't have calls happening at the exact same second
    prev_time = -1
    for idx, row in data.iterrows():
        d = row.to_dict()
        d['vertex_id'] = vertex_id

        # Ensure that we don't have calls at the same second
        if d['time'] <= prev_time:
            d['time'] = prev_time + 1
        prev_time = d['time']

        # convert everything to string
        for k, v in d.items():
            d[k] = str(v)
        
        # Add the event to the vertex
        event = et.SubElement(vertex, 'event', d)

    return node

class EventGenerator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("911 Call Data Generator")
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Input labels for GUI
        self.labels = [
            "First (seconds):",
            "Last (seconds):",
            "Mean Time Interval (seconds):",
            "Dead Time after Event (seconds):",
            "Mean Call Interval after incident (seconds):",
            "Mean Duration (seconds):",
            "Minimum Duration (seconds):",
            "Mean Patience Time (seconds):",
            "Mean On-Site Time (seconds):",
        ]

        self.entries = {}
        for label_text in self.labels:
            label = QLabel(label_text)
            entry = QLineEdit()
            self.entries[label_text] = entry

            layout.addWidget(label)
            layout.addWidget(entry)
        
        # Graph File input field
        graph_file_label = QLabel("Select Graph File (.graphml):")
        self.graph_file_label = QLineEdit()
        graph_file_button = QPushButton("Browse")
        graph_file_button.clicked.connect(self.browse_file)

        layout.addWidget(graph_file_label)
        layout.addWidget(self.graph_file_label)
        layout.addWidget(graph_file_button)

        # Graph ID input field
        graph_id_label = QLabel("Graph ID:")
        self.graph_id_entry = QLineEdit()

        layout.addWidget(graph_id_label)
        layout.addWidget(self.graph_id_entry)

        # Submit button
        generate_button = QPushButton("Generate Events")
        generate_button.clicked.connect(self.generate_events)
        layout.addWidget(generate_button)

        self.setLayout(layout)
        self.show()
    
    # Function that allows user to browse local files
    def browse_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_dialog = QFileDialog()
        file_dialog.setNameFilter("GraphML files (*.graphml)")
        file_dialog.setViewMode(QFileDialog.Detail)
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        file_dialog.setOptions(options)

        if file_dialog.exec_():
            selected_file = file_dialog.selectedFiles()
            if selected_file[0].endswith(".graphml"):
                self.graph_file_label.setText(selected_file[0])
            else:
                QMessageBox.warning(
                    self, "Invalid File Type", "Please select a .graphml file."
                )

    # Moved existing main methods to take user inputted data
    # Handles invalid inputs (string instead of int, wrong file 
    # type but not invalid logic)
    def generate_events(self):
        error_message = ""
        invalid_fields = []

        for label_text, entry in self.entries.items():
            if label_text != "Select Region Grid (.graphml):":
                text = entry.text().strip()
                if not text:
                    invalid_fields.append(label_text)
                else:
                    try:
                        float(text)  # Attempt to convert to float to check validity
                    except ValueError:
                        invalid_fields.append(label_text)

        # Error handling
        graph_file = self.graph_file_label.text().strip()
        if not graph_file:
            invalid_fields.append("Select Region Grid (.graphml):")
        elif not graph_file.endswith(".graphml"):
            invalid_fields.append("Select Region Grid (.graphml) must be a .graphml file.")

        if invalid_fields:
            error_message = "Invalid or empty values in the following fields:\n"
            for field in invalid_fields:
                error_message += f"- {field}\n"

        try:
            if error_message:
                raise ValueError(error_message)

            # Get other necessary inputs for functions
            first = float(self.entries["First (seconds):"].text())
            last = float(self.entries["Last (seconds):"].text())
            mu = float(self.entries["Mean Time Interval (seconds):"].text())
            pp_dead_t = float(self.entries["Dead Time after Event (seconds):"].text())
            sec_proc_sigma = float(self.entries["Mean Call Interval after incident (seconds):"].text())
            duration_mean = float(self.entries["Mean Duration (seconds):"].text())
            duration_min = float(self.entries["Minimum Duration (seconds):"].text())
            patience_mean = float(self.entries["Mean Patience Time (seconds):"].text())
            avg_on_site_time = float(self.entries["Mean On-Site Time (seconds):"].text())
                
            # Integration of the event generation code
            if graph_file:
                ###########################################################################
                # PRIMARY EVENTS
                ###########################################################################
                # Start your event generation process here based on the valid inputs
                graph = nx.read_graphml(graph_file)
                graph_id = self.graph_id_entry.text().strip()
                graph_attribute = graph.nodes[graph_id]['segments']
                graph_grid = np.array(eval(graph_attribute))
                
                # Seed numpy random number to get consistent results
                np.random.seed(20)
                
                # Call primprocess using the inputs from the interface
                incidents = primprocess(first, last, mu, pp_dead_t, graph_grid)
                print(f'Number of Primary events: {incidents.shape[0]}')

                # Ratios based on NORCOM 2022 report. NORCOM doesn't make a distinction
                # between EMS and Fire call types, so I split it in half.
                type_ratios = {'Law': 0.64,
                            'EMS': 0.18,
                            'Fire': 0.18}
                
                # Generate the incident types based on the type_ratios
                incidents_with_types = add_types(incidents, type_ratios)
                
                ###########################################################################
                # SECONDARY EVENTS
                ###########################################################################
                # Define prototypes for location of secondary spatio-temporal points
                # 0.001° is aproximately 111 meters (one footbal field plus both endzones)
                # intensity represent the expected number of points per square unit.
                # TODO: The values used for the prototypes are ballpark values not based on
                #       real data. Althoug, they give us around 70,000 - 75,000 calls in a month,
                #       which is close to what Seattle PD receives with 900,000 calls per year.
                prototypes = {0: {'mu_r':0.0005, 'sdev_r':0.0001, 'mu_intensity':500000, 'sdev_intensity': 50000},
                        1: {'mu_r':0.001, 'sdev_r':0.0001, 'mu_intensity':1000000, 'sdev_intensity': 60000},
                        2: {'mu_r':0.0015, 'sdev_r':0.001, 'mu_intensity':1100000, 'sdev_intensity': 70000},
                        3: {'mu_r':0.003, 'sdev_r':0.001, 'mu_intensity':1500000, 'sdev_intensity': 60000}}
                
                # Time the secondary process generation
                start_t = time.time()

                print('Generating Secondary events...')

                sec_events = secprocess(sec_proc_sigma, duration_mean, duration_min, patience_mean,
                                        avg_on_site_time, prototypes, incidents_with_types)
                
                end_t = time.time()

                print('Elapsed time:', round(end_t - start_t, 4), 'seconds')
                print('Number of Primary Events:', len(incidents_with_types))
                print('Number of Secondary Events:', sec_events.shape[0])

                # Output filenames are generic, will match the filename you inputted
                graph_file_path = self.graph_file_label.text()
                output_file_name = os.path.basename(graph_file_path)
                output_file = os.path.splitext(output_file_name)[0] + ".xml"
                # Commented out code that saves to a .csv file
                # sec_events_df = pd.DataFrame(sec_events, columns=['time', 'duration', 'x', 'y', 'type'])
                # sec_events_df.to_csv(output_file, index=False, header=True)

                ###########################################################################
                # TURN CALL LIST INTO AN XML TREE AND SAVE TO FILE
                ###########################################################################
                # The root element
                inputs = et.Element('simulator_inputs')

                # The data element will contain all calls grouped per vertex
                data = et.SubElement(inputs, 'data', {"description": "SPD Calls - Cluster Point Process", 
                                                    "clock_tick_size": "1",
                                                    "clock_tick_unit": "sec"})
                
                # Create the vertex element with all its associated calls (events)
                vertex_name = graph.nodes[graph_id]['name']
                data = add_vertex_events(data, graph_id, vertex_name, sec_events)

                tree = et.ElementTree(inputs)
                tree_out = tree.write(output_file,
                                    xml_declaration=True,
                                    encoding='UTF-8',
                                    pretty_print=True)

                print('Secondary process was saved to:', output_file)
                
                # Display message box indicating completion
                QMessageBox.information(
                    self, "Process Complete", "Event generation completed successfully."
                )
            else:
                QMessageBox.warning(
                    self, "Missing File", "Please select a graph file."
                )

        except ValueError as ve:
            error_box = QMessageBox()
            error_box.setIcon(QMessageBox.Warning)
            error_box.setWindowTitle("Input Error")
            error_box.setText(str(ve))
            error_box.exec_()

def main():
    app = QApplication(sys.argv)
    window = EventGenerator()
    sys.exit(app.exec_())

if __name__ == '__main__':
    import pandas as pd
    import networkx as nx
    import time
    main()
    
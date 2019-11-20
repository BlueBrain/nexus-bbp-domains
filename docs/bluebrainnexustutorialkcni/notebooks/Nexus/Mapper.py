import Nexus.Neuroshapes as nsp
import Nexus.Utils as nsu
import requests
import json

class Mapper():

    def __init__(self, deployment, org_label, project_label):

        self.base = f"{deployment}/resources/{org_label}/{project_label}/_/"

    def allencelltypesdb2neuroshapes(self, project_label, neuron_morphologies:list) -> dict:
        experiment = nsp.Experiment(project_label)
        entity_dict = dict()
        vocabulary = nsu.load_json("./vocabulary.json")
        ephys_protocol_at_id = "http://help.brain-map.org/download/attachments/8323525/CellTypes_Ephys_Overview.pdf?version=2&modificationDate=1508180425883&api=v2"
        reconstruction_protocol_at_id = "http://help.brain-map.org/download/attachments/8323525/CellTypes_Morph_Overview.pdf?version=4&modificationDate=1528310097913&api=v2"
        aibs_grid_identifier = "https://www.grid.ac/institutes/grid.417881.3"

        for morph in neuron_morphologies:
            subject_name = morph["donor__name"]
            subject_id = morph["donor__id"]
            subject_at_id = f"{self.base}subject_{subject_id}"
            subject_identifier = morph["donor__id"]
            if subject_at_id not in entity_dict.keys():
                species_label = vocabulary[morph["donor__species"]]["label"]
                species_id = vocabulary[morph["donor__species"]]["@id"]
                age_period = "Post-natal"
                age_unit = morph["donor__age"].split(" ")[-1]
                age_value = morph["donor__age"].split(" ")[0]
                if morph["line_name"] != "" and morph["line_name"] not in ["Esr2-IRES2-Cre-neo|PhiC31-neo"]:
                    strain_id = vocabulary[morph["line_name"]]["@id"]
                    strain_label = vocabulary[morph["line_name"]]["label"]
                else:
                    strain_id = None
                    strain_label = None
                if morph["donor__sex"] != "":
                    sex_id = vocabulary[morph["donor__sex"]]["@id"]
                    sex_label = vocabulary[morph["donor__sex"]]["label"]
                else:
                    sex_id = None
                    sex_label = None
                if morph["donor__disease_state"] != "":
                    disease_id = vocabulary[morph["donor__disease_state"]]["@id"]
                    disease_label = vocabulary[morph["donor__disease_state"]]["label"]
                else:
                    disease_id = None
                    disease_label = None

                subject = experiment.subject(name=subject_name, at_id=subject_at_id, species_label=species_label,
                                             species_id=species_id, identifier=subject_identifier,
                                             age_period=age_period,
                                             age_unit=age_unit, age_value=age_value, strain_id=strain_id,
                                             strain_label=strain_label, sex_id=sex_id, sex_label=sex_label,
                                             disease_id=disease_id,
                                             disease_label=disease_label)

                slicecollection_at_id = f"{self.base}slicecollection_{subject_id}"
                slicecollection = experiment.slicecollection(name=f"{subject_name} Slice Collection",
                                                             at_id=slicecollection_at_id)

                brainslicing_at_id = f"{self.base}brainslicing_{subject_id}"
                brainslicing = experiment.brainslicing(at_id=brainslicing_at_id, used_id=subject_at_id,
                                                       generated_id=slicecollection_at_id,
                                                       cutting_thickness_value="350", cutting_thickness_unit="µm")

                slicecollection_has_part_at_id = f"{self.base}collection_{subject_id}"
                slicecollection_has_part = experiment.slicecollection(name=f"{subject_name} Slice Collection",
                                                                      at_id=slicecollection_has_part_at_id)

                wholecellpatchclamp_at_id = f"{self.base}wholecellpatchclamp_{subject_id}"
                wholecellpatchclamp = experiment.wholecellpatchclamp(at_id=wholecellpatchclamp_at_id,
                                                                     used_id=slicecollection_at_id,
                                                                     generated_id=slicecollection_has_part_at_id,
                                                                     had_protocol_ids=[ephys_protocol_at_id],
                                                                     was_associated_with_ids=[aibs_grid_identifier])

                subject["donor__race"] = morph["donor__race"]
                subject["donor__years_of_seizure_history"] = morph["donor__years_of_seizure_history"]
                to_delete = list()
                for key, value in subject.items():
                        if value == "":
                            to_delete.append(key)
                for key in to_delete:
                    del subject[key]
                
                entity_dict[subject_at_id] = subject
                entity_dict[slicecollection_at_id] = slicecollection
                entity_dict[brainslicing_at_id] = brainslicing
                entity_dict[slicecollection_has_part_at_id] = slicecollection_has_part
                entity_dict[wholecellpatchclamp_at_id] = wholecellpatchclamp

            else:
                slicecollection_has_part_at_id = f"{self.base}collection_{subject_id}"

            cell_id = morph["specimen__id"]
            cell_name = morph["specimen__name"]
            structure_id = morph["structure__id"]
            brain_region_id = f"http://api.brain-map.org/api/v2/data/Structure/{structure_id}"
            brain_region_label = morph["structure__name"]
            layer = morph["structure__layer"]
            if layer not in ["2/3", "6a", "6b"]:
                layer_id = vocabulary[layer]["@id"]
                layer_label = vocabulary[layer]["label"]
            else:
                layer_id = None
                layer_label = None
            patchedcell_at_id = f"{self.base}patchedcell_{cell_id}"
            neuronmorphology_identifier = f"http://celltypes.brain-map.org/experiment/morphology/{cell_id}"

            patchedcell = experiment.patchedcell(name=f"{cell_name} Patched Cell", at_id=patchedcell_at_id,
                                                 brain_region_id=brain_region_id,
                                                 brain_region_label=brain_region_label,
                                                 dendrite_morphology=morph["tag__dendrite_type"])
            patchedcell["tag__apical"] = morph["tag__apical"]

            entity_dict[slicecollection_has_part_at_id]["hasPart"].append(
                {"@id": patchedcell_at_id, "@type": ["prov:Entity", "nsg:PatchedCell"]})

            labeledcell_at_id = f"{self.base}labeledcell_{cell_id}"
            labeledcell = experiment.labeledcell(name=f"{cell_name} Labeled Cell", at_id=labeledcell_at_id,
                                                 brain_region_id=brain_region_id,
                                                 brain_region_label=brain_region_label,
                                                 was_derived_from_id=patchedcell_at_id)

            neuronmorphology_at_id = f"{self.base}neuronmorphology_{cell_id}"
            reconstruction_at_id = f"{self.base}reconstruction_{cell_id}"
            tracecollection_at_id = f"{self.base}tracecollection_{cell_id}"
            neuronmorphology = experiment.reconstructedneuronmorphology(name=f"{cell_name} Neuron Morphology", at_id=neuronmorphology_at_id,
                                                           identifier=cell_id,
                                                           brain_region_id=brain_region_id,
                                                           brain_region_label=brain_region_label,
                                                           coordinate_value_x=morph["csl__x"],
                                                           coordinate_value_y=morph["csl__y"],
                                                           coordinate_value_z=morph["csl__z"],
                                                           layer_id=layer_id, layer_label=layer_label,
                                                           subject_id=subject_at_id,
                                                           license_id="https://alleninstitute.org/legal/terms-use/",
                                                           generation_id=reconstruction_at_id,
                                                           derivation_ids=[subject_at_id, slicecollection_at_id,
                                                                            slicecollection_has_part_at_id, patchedcell_at_id,
                                                                            labeledcell_at_id],
                                                           contribution_id=aibs_grid_identifier)


            reconstruction = experiment.reconstruction(generated_id=neuronmorphology_at_id,
                                                       used_id=labeledcell_at_id, at_id=reconstruction_at_id,
                                                       had_protocol_ids=[reconstruction_protocol_at_id],
                                                       was_associated_with_ids=[aibs_grid_identifier])

            
            tracecollection = experiment.tracecollection(name=f"{cell_name} Trace Collection", at_id=tracecollection_at_id,
                                                           identifier=cell_id,
                                                           brain_region_id=brain_region_id,
                                                           brain_region_label=brain_region_label,
                                                           subject_id=subject_at_id,
                                                           license_id="https://alleninstitute.org/legal/terms-use/",
                                                           derivation_ids=[subject_at_id, slicecollection_at_id,
                                                                            slicecollection_has_part_at_id, patchedcell_at_id],
                                                           contribution_id=aibs_grid_identifier)

            for key in ["csl__normalized_depth",
                        "m__biophys",
                        "m__biophys_all_active",
                        "m__biophys_perisomatic",
                        "m__glif",
                        "morph_thumb_path",
                        "nr__average_contraction",
                        "nr__average_parent_daughter_ratio",
                        "nr__max_euclidean_distance",
                        "nr__number_bifurcations",
                        "nr__number_stems",
                        "nr__reconstruction_type",
                        "nrwkf__id"]:
                neuronmorphology[key] = morph[key]
            
            to_delete = list()
            for key, value in neuronmorphology.items():
                    if value == "":
                        to_delete.append(key)
            for key in to_delete:
                del neuronmorphology[key]
            
            for key in ["ef__adaptation", 
                        "ef__avg_firing_rate", 
                        "ef__avg_isi", 
                        "ef__f_i_curve_slope",
                        "ef__fast_trough_v_long_square",
                        "ef__peak_t_ramp",
                        "ef__ri",
                        "ef__tau",
                        "ef__threshold_i_long_square",
                        "ef__upstroke_downstroke_ratio_long_square",
                        "ef__vrest",
                        "ephys_inst_thresh_thumb_path",
                       "ef__vrest",
                       "ephys_inst_thresh_thumb_path",
                       "ephys_thumb_path",
                       "erwkf__id",
                       "si__height",
                       "si__path",
                       "si__width",
                       "si__height"]:
                tracecollection[key] = morph[key]
            to_delete = list()
            for key, value in tracecollection.items():
                    if value == "":
                        to_delete.append(key)
            for key in to_delete:
                del tracecollection[key]
            
            
            entity_dict[patchedcell_at_id] = patchedcell
            entity_dict[labeledcell_at_id] = labeledcell
            entity_dict[neuronmorphology_at_id] = neuronmorphology
            entity_dict[reconstruction_at_id] = reconstruction
            entity_dict[tracecollection_at_id] = tracecollection

        entitiy_list = list()
        for key,value in entity_dict.items():
            entitiy_list.append(value)
        return entitiy_list
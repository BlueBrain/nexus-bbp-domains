import Nexus.Payload as nsp
import requests
import json

class Mapper:

    def __init__(self, base="https://neuroshapes.org/workshop/", context="https://bbp.neuroshapes.org"):

        self.context = context

    def allencelltypesdb2neuroshapes(self, neuron_morphologies:list, vocabulary:dict) -> dict:
        experiment = nsp.Experiment()
        graph = dict()

        organization_at_id = "https://www.grid.ac/institutes/grid.417881.3"
        organization = experiment.organization(at_id=organization_at_id,
                                               name="Allen Institute for Brain Science",
                                               address="615 Westlake Ave N, Seattle, WA 98109, USA")
        graph[organization_at_id] = organization

        experimentalprotocol_at_id = "http://help.brain-map.org/display/celltypes/Documentation"
        experimentalprotocol = experiment.experimentalprotocol(
            name="Technical White Paper: Cell Morphology and Histology",
            at_id=experimentalprotocol_at_id,
            author_id=organization_at_id,
            date_published="2017-10-00T00:00:00",
            description="Protocol used to generate Allen Cell Types Database",
            identifier="http://help.brain-map.org/display/celltypes/Documentation?preview=/8323525/10813530/CellTypes_Morph_Overview.pdf")
        graph[experimentalprotocol_at_id] = experimentalprotocol

        for morph in neuron_morphologies:
            subject_name = morph["donor__name"]
            subject_id = morph["donor__id"]
            subject_at_id = f"{self.base}subject_{subject_id}"
            subject_identifier = morph["donor__id"]
            if subject_at_id not in graph.keys():
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
                                                       was_associated_with_ids=[organization_at_id],
                                                       had_protocol_ids=[experimentalprotocol_at_id],
                                                       cutting_thickness_value="350", cutting_thickness_unit="µm")

                slicecollection_has_part_at_id = f"{self.base}collection_{subject_id}"
                slicecollection_has_part = experiment.slicecollection(name=f"{subject_name} Slice Collection",
                                                                      at_id=slicecollection_has_part_at_id)

                wholecellpatchclamp_at_id = f"{self.base}wholecellpatchclamp_{subject_id}"
                wholecellpatchclamp = experiment.wholecellpatchclamp(at_id=wholecellpatchclamp_at_id,
                                                                     used_id=slicecollection_at_id,
                                                                     generated_id=slicecollection_has_part_at_id,
                                                                     was_associated_with_ids=[organization_at_id],
                                                                     had_protocol_ids=[experimentalprotocol_at_id])

                subject["donor__race"] = morph["donor__race"]
                subject["donor__years_of_seizure_history"] = morph["donor__years_of_seizure_history"]
                for key,value in subject.items():
                    if value == "":
                        del subject[key]
                
                graph[subject_at_id] = subject
                graph[slicecollection_at_id] = slicecollection
                graph[brainslicing_at_id] = brainslicing
                graph[slicecollection_has_part_at_id] = slicecollection_has_part
                graph[wholecellpatchclamp_at_id] = wholecellpatchclamp

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

            graph[slicecollection_has_part_at_id]["hasPart"].append(
                {"@id": patchedcell_at_id, "@type": ["prov:Entity", "nsg:PatchedCell"]})

            labeledcell_at_id = f"{self.base}labeledcell_{cell_id}"
            labeledcell = experiment.labeledcell(name=f"{cell_name} Labeled Cell", at_id=labeledcell_at_id,
                                                 brain_region_id=brain_region_id,
                                                 brain_region_label=brain_region_label,
                                                 was_derived_from_id=patchedcell_at_id)

            neuronmorphology_at_id = f"{self.base}neuronmorphology_{cell_id}"
            reconstruction_at_id = f"{self.base}reconstruction_{cell_id}"
            tracecollection_at_id = f"{self.base}tracecollection_{cell_id}"
            neuronmorphology = experiment.neuronmorphology(name=f"{cell_name} Neuron Morphology", at_id=neuronmorphology_at_id,
                                                           brain_region_id=brain_region_id,
                                                           brain_region_label=brain_region_label,
                                                           coordinate_value_x=morph["csl__x"],
                                                           coordinate_value_y=morph["csl__y"],
                                                           coordinate_value_z=morph["csl__z"],
                                                           layer_id=layer_id, layer_label=layer_label,
                                                           distribution_url=neuronmorphology_identifier,
                                                           contribution_id=organization_at_id,
                                                           subject_id=subject_at_id,
                                                           license_id="https://alleninstitute.org/legal/terms-use/",
                                                           generation_id=reconstruction_at_id,
                                                           derivation_ids=[subject_at_id, slicecollection_at_id,
                                                                            slicecollection_has_part_at_id, patchedcell_at_id,
                                                                            labeledcell_at_id])


            reconstruction = experiment.reconstruction(generated_id=neuronmorphology_at_id,
                                                       used_id=labeledcell_at_id, at_id=reconstruction_at_id,
                                                       had_protocol_ids=[experimentalprotocol_at_id],
                                                       was_associated_with_ids=[organization_at_id])

            
            tracecollection = experiment.tracecollection(name=f"{cell_name} Trace Collection", at_id=tracecollection_at_id,
                                                           brain_region_id=brain_region_id,
                                                           brain_region_label=brain_region_label,
                                                           contribution_id=organization_at_id,
                                                           subject_id=subject_at_id,
                                                           license_id="https://alleninstitute.org/legal/terms-use/",
                                                           derivation_ids=[subject_at_id, slicecollection_at_id,
                                                                            slicecollection_has_part_at_id, patchedcell_at_id])

           
            neuronmorphology["csl__normalized_depth"] = morph["csl__normalized_depth"]
            neuronmorphology["m__biophys"] = morph["m__biophys"]
            neuronmorphology["m__biophys_all_active"] = morph["m__biophys_all_active"]
            neuronmorphology["m__biophys_perisomatic"] = morph["m__biophys_perisomatic"]
            neuronmorphology["m__glif"] = morph["m__glif"]
            neuronmorphology["morph_thumb_path"] = morph["morph_thumb_path"]
            neuronmorphology["nr__average_contraction"] = morph["nr__average_contraction"]
            neuronmorphology["nr__average_parent_daughter_ratio"] = morph["nr__average_parent_daughter_ratio"]
            neuronmorphology["nr__max_euclidean_distance"] = morph["nr__max_euclidean_distance"]
            neuronmorphology["nr__number_bifurcations"] = morph["nr__number_bifurcations"]
            neuronmorphology["nr__number_stems"] = morph["nr__number_stems"]
            neuronmorphology["nr__reconstruction_type"] = morph["nr__reconstruction_type"]
            neuronmorphology["nrwkf__id"] = morph["nrwkf__id"]
            for key,value in neuronmorphology.items():
                    if value == "":
                        del neuronmorphology[key]
            
            tracecollection["ef__adaptation"] = morph["ef__adaptation"]
            tracecollection["ef__avg_firing_rate"] = morph["ef__avg_firing_rate"]
            tracecollection["ef__avg_isi"] = morph["ef__avg_isi"]
            tracecollection["ef__f_i_curve_slope"] = morph["ef__f_i_curve_slope"]
            tracecollection["ef__fast_trough_v_long_square"] = morph["ef__fast_trough_v_long_square"]
            tracecollection["ef__peak_t_ramp"] = morph["ef__peak_t_ramp"]
            tracecollection["ef__ri"] = morph["ef__ri"]
            tracecollection["ef__tau"] = morph["ef__tau"]
            tracecollection["ef__threshold_i_long_square"] = morph["ef__threshold_i_long_square"]
            tracecollection["ef__upstroke_downstroke_ratio_long_square"] = morph["ef__upstroke_downstroke_ratio_long_square"]
            tracecollection["ef__vrest"] = morph["ef__vrest"]
            tracecollection["ephys_inst_thresh_thumb_path"] = morph["ephys_inst_thresh_thumb_path"]
            tracecollection["ephys_thumb_path"] = morph["ephys_thumb_path"]
            tracecollection["erwkf__id"] = morph["erwkf__id"]
            tracecollection["si__height"] = morph["si__height"]
            tracecollection["si__path"] = morph["si__path"]
            tracecollection["si__width"] = morph["si__width"]
            tracecollection["si__height"] = morph["si__height"]
            for key,value in tracecollection.items():
                    if value == "":
                        del tracecollection[key]
            
            
            graph[patchedcell_at_id] = patchedcell
            graph[labeledcell_at_id] = labeledcell
            graph[neuronmorphology_at_id] = neuronmorphology
            graph[reconstruction_at_id] = reconstruction
            graph[tracecollection_at_id] = tracecollection

   
        
        at_graph = dict()
        at_graph["@context"] = self.context
        at_graph["@id"] = "https://neuroshapes.org/graph/allen"
        at_graph["@graph"] = list()
        for key,value in graph.items():
            at_graph["@graph"].append(value)

        return at_graph
from collections import defaultdict


class Experiment:
    """
    Neuroshapes entities of the Allen Cell Types Database data 
    """
    
    def __init__(self, project_label):

        self.context = f"https://{project_label}.neuroshapes.org"
    
    def organization(self, at_id: str, name: str, address: str=None) -> dict:
        """
        
        :param at_id: @id of the organization (e.g. GRID identifier)
        :param name: Name of the organization
        :param address: Address of the organization
        :return: The organization payload as dict object
        """
        organization_payload = dict()
        organization_payload["@type"] = "Organization"
        organization_payload["@context"] = self.context
        organization_payload["@id"] = at_id
        organization_payload["name"] = name
        if address:
            organization_payload["address"] = address
        return organization_payload

    def person(self, at_id: str, family_name: str=None, given_name: str=None, email: str=None,
               affiliation_id: str=None) -> dict:
        """
        
        :param at_id: @id of the person
        :param family_name: Family name of the person
        :param given_name: Given name of the person
        :param email: Email address of the person
        :param affiliation_id: @id of the institute with which the person is affiliated (e.g. GRID identifier)
        :return: The person payload as dict object
        """
        person_payload = dict()
        person_payload["@type"] = "Person"
        person_payload["@context"] = self.context
        person_payload["@id"] = at_id
        person_payload["familyName"] = family_name
        person_payload["givenName"] = given_name
        if email:
            person_payload["email"] = email
        if affiliation_id:
            person_payload["affiliation"] = {"@id": affiliation_id, "@type": "Organization"}
        return person_payload

    def experimentalprotocol(self, at_id: str, name: str, author_type: str, author_id: str=None,
                             date_published: str=None, description: str=None, identifier: str=None) -> dict:
        """
        
        :param at_id: @id of the experimental protocol
        :param name: Name of the experimental protocol
        :param author_type: Data type of the author (Organization or Person)
        :param author_id: The Nexus identifier of the author of the experimental protocol
        :param date_published: The publishing date of the experimental protocol
        :param description: The description of the experimental protocol
        :param identifier: The identifier (e.g. DOI) of the experimental protocol
        :return: The experimental protocol payload as dict object
        """
        experimentalprotocol_payload = dict()
        experimentalprotocol_payload["@context"] = self.context
        experimentalprotocol_payload["@type"] = "ExperimentalProtocol"
        experimentalprotocol_payload["@id"] = at_id
        experimentalprotocol_payload["name"] = name
        if author_id:
            experimentalprotocol_payload["author"] = {"@id": author_id,
                                                      "@type": author_type}
        if date_published:
            experimentalprotocol_payload["datePublished"] = date_published
        if description:
            experimentalprotocol_payload["description"] = description
        if identifier:
            experimentalprotocol_payload["identifier"] = identifier
        return experimentalprotocol_payload

    def subject(self, at_id: str, name: str, species_label: str, species_id: str, identifier: str=None,
                age_period: str=None, age_unit: str=None, age_value: int =None, strain_id: str=None,
                strain_label: str=None, sex_id: str=None, sex_label: str=None, transgenic_id: str=None,
                transgenic_label: str=None, birth_date: str=None, death_date: str=None, date_of_surgery: str=None,
                disease_model_id: str=None, disease_model_label: str=None, disease_id: str=None,
                disease_label: str=None, treatment_id: str=None, treatment_label: str=None, weight_value: str=None,
                weight_unit: str=None) -> dict:
        """
        
        :param at_id: @id of the subject    
        :param name: name of the subject
        :param species_id: URI of species
        :param species_label: corresponding label
        :param identifier: provider ID of the subject
        :param age_period: age period (Post-natal, Pre-natal)
        :param age_unit: age unit (e.g. days, months, years)
        :param age_value: numerical value of age
        :param strain_id: URI of strain
        :param strain_label: corresponding label
        :param sex_id: URI of sex 
        :param sex_label: corresponding label
        :param transgenic_id: URI of transgenic
        :param transgenic_label: corresponding label
        :param birth_date: birth date of subject
        :param death_date: death date of subject
        :param date_of_surgery: date of surgery of subject (e.g. for human subjects)
        :param disease_model_id: URI of disease model (e.g. Specific genetic forms of Alzheimer's modelled in rodents)
        :param disease_model_label: corresponding label
        :param disease_id: URI of disease
        :param disease_label: corresponding label
        :param treatment_id: URI of treatment
        :param treatment_label: corresponding label
        :param weight_value: numerical value of weight
        :param weight_unit: weight unit (e.g. grams)
        :return: The subject payload as dict object
        """

        subject_payload = dict()
        subject_payload["@type"] = "Subject"
        subject_payload["@context"] = self.context
        subject_payload["@id"] = at_id
        subject_payload["name"] = name
        subject_payload["species"] = {"@id": species_id, "label": species_label}
        if identifier:
            subject_payload["identifier"] = identifier
        if age_value:
            subject_payload["age"] = {"period": age_period, "unitCode": age_unit, "value": {"@value": age_value,
                                                                                            "@type": "xsd:integer"}}
        if strain_id:
            subject_payload["strain"] = {"@id": strain_id, "label": strain_label}
        if sex_id:
            subject_payload["sex"] = {"@id": sex_id, "label": sex_label}
        if transgenic_id:
            subject_payload["transgenic"] = {"@id": transgenic_id, "label": transgenic_label}
        if birth_date:
            subject_payload["birthDate"] = birth_date
        if death_date:
            subject_payload["deathDate"] = death_date
        if date_of_surgery:
            subject_payload["dateOfSurgery"] = date_of_surgery
        if disease_model_id:
            subject_payload["diseaseModel"] = {"@id": disease_model_id, "label": disease_model_label}
        if disease_id:
            subject_payload["disease"] = {"@id": disease_id, "label": disease_label}
        if treatment_id:
            subject_payload["treatment"] = {"@id": treatment_id, "label": treatment_label}
        if weight_value:
            subject_payload["weight"] = {"value": weight_value, "unitCode": weight_unit}

        return subject_payload

    def slicecollection(self, at_id: str, name: str, identifier: str=None, has_part_ids: list=None) -> dict:
        """

        :param name: provider name of the slicecollection
        :param at_id: @id of the slicecollection
        :param identifier: provider ID of the slicecollection
        :param has_part_ids: The list of @id values of slices which are part of this collection 
        :return: The slicecollection payload as dict object
        """

        slicecollection_payload = defaultdict(list)
        slicecollection_payload["@type"] = "SliceCollection"
        slicecollection_payload["@context"] = self.context
        slicecollection_payload["@id"] = at_id
        slicecollection_payload["name"] = name
        if identifier:
            slicecollection_payload["identifier"] = identifier
        if has_part_ids:
            for has_part_id in has_part_ids:
                slicecollection_payload["hasPart"].append(
                    {"@id": has_part_id, "@type": "Entity"})
        return slicecollection_payload

    def brainslicing(self, at_id: str, used_id: str, generated_id: str, started_at_time: str=None,
                     ended_at_time: str=None, was_associated_with_ids: list=None, had_protocol_ids: list=None,
                     brain_region_id: str=None, brain_region_label: str=None, slicing_plane: str=None,
                     slicing_angle: str=None, cutting_thickness_value: str=None, cutting_thickness_unit: str=None,
                     hemisphere: str=None, solution: str=None) -> dict:
        """
        
        :param at_id: The @id of the brain slicing activity
        :param used_id: The identifier of the subject which was used in the brain slicing activity
        :param generated_id: The identifier of the brain slice collection which was generated by the brain slicing 
        activity
        :param started_at_time: Date time at which the activity started
        :param ended_at_time: Date time at which the activity ended
        :param was_associated_with_ids: The identifiers of the agents which were associated with the activity
        :param had_protocol_ids: The identifier of the protocol of this activity
        :param brain_region_id: The identifier of the brain region which was sliced
        :param brain_region_label: The label of the brain region which was sliced 
        :param slicing_plane: The slicing plane (i.e. Horizontal, Coronal, Sagittal, Para-Sagittal)
        :param slicing_angle: The slicing angle
        :param cutting_thickness_value: The value of the cutting thickness (e.g. 300) 
        :param cutting_thickness_unit: The unit of the cutting thickness (e.g. μm)
        :param hemisphere: The brain hemisphere (i.e. Left, Right)
        :param solution: The cutting solution used in the brain slicing
        :return: The brain slicing payload as dict object
        """
        brainslicing_payload = defaultdict(list)
        brainslicing_payload["@type"] = "BrainSlicing"
        brainslicing_payload["@context"] = self.context
        brainslicing_payload["@id"] = at_id
        brainslicing_payload["used"] = {"@id": used_id, "@type": ["Subject", "Entity"]}
        brainslicing_payload["generated"] = {"@id": generated_id, "@type": ["SliceCollection", "Entity"]}
        if started_at_time:
            brainslicing_payload["startedAtTime"] = {"@value": started_at_time, "@type": "xsd:dateTime"}
        if ended_at_time:
            brainslicing_payload["endedAtTime"] = {"@value": ended_at_time, "@type": "xsd:dateTime"}
        if was_associated_with_ids:
            for agent_id in was_associated_with_ids:
                brainslicing_payload["wasAssociatedWith"].append({"@id": agent_id, "@type": "Agent"})
        if had_protocol_ids:
            for protocol_id in had_protocol_ids:
                brainslicing_payload["hadProtocol"].append({"@id": protocol_id, "@type": ["ExperimentalProtocol",
                                                                                          "Protocol"]})
        if brain_region_id:
            brainslicing_payload["brainLocation"] = {"brainRegion": {"@id": brain_region_id,
                                                                     "label": brain_region_label}}
        if slicing_plane:
            brainslicing_payload["slicingPlane"] = slicing_plane
        if slicing_angle:
            brainslicing_payload["slicingAngle"] = slicing_angle
        if cutting_thickness_value:
            brainslicing_payload["cuttingThickness"] = {"value": {"@value": cutting_thickness_value,
                                                                  "@type": "xsd:integer"},
                                                        "unitCode": cutting_thickness_unit}
        if hemisphere:
            brainslicing_payload["hemisphere"] = hemisphere
        if solution:
            brainslicing_payload["solution"] = solution
        return brainslicing_payload

    def wholecellpatchclamp(self, at_id: str, used_id: str, generated_id: str, started_at_time: str=None,
                            ended_at_time: str=None, was_associated_with_ids: list=None,
                            had_protocol_ids: list=None) -> dict:
        """
        
        :param used_id: The identifier of the slice which was used in the whole cell patch-clamp activity
        :param generated_id: The identifier of the patched slice which was generated by the whole cell patch-clamp 
        activity
        :param at_id: @id of the whole cell patch-clamp
        :param started_at_time: Date time at which the activity started
        :param ended_at_time: Date time at which the activity ended
        :param was_associated_with_ids: The @id values of the agents which were associated with the activity
        :param had_protocol_ids: The @id values of the protocols of this activity
        :return: The whole cell patch-clamp payload as dict object
        """
        wholecellpatchclamp_payload = defaultdict(list)
        wholecellpatchclamp_payload["@type"] = "WholeCellPatchClamp"
        wholecellpatchclamp_payload["@context"] = self.context
        wholecellpatchclamp_payload["@id"] = at_id
        wholecellpatchclamp_payload["used"] = {"@id": used_id, "@type": ["SliceCollection", "Entity"]}
        wholecellpatchclamp_payload["generated"] = {"@id": generated_id, "@type": ["SliceCollection", "Entity"]}
        if started_at_time:
            wholecellpatchclamp_payload["startedAtTime"] = {
                "@value": started_at_time,
                "@type": "xsd:dateTime"
                }
        if ended_at_time:
            wholecellpatchclamp_payload["endedAtTime"] = {
                "@value": ended_at_time,
                "@type": "xsd:dateTime"
                }
        if was_associated_with_ids:
            for agent_id in was_associated_with_ids:
                wholecellpatchclamp_payload["wasAssociatedWith"].append({"@id": agent_id, "@type": "Agent"})
        if had_protocol_ids:
            for protocol_id in had_protocol_ids:
                wholecellpatchclamp_payload["hadProtocol"].append({"@id": protocol_id, "@type": ["ExperimentalProtocol",
                                                                                          "Protocol"]})
        return wholecellpatchclamp_payload

    def reconstructedneuronmorphology(self, at_id: str, name: str, brain_region_id: str, brain_region_label: str,
                                      coordinate_value_x: float =None, coordinate_value_y: float =None,
                                      coordinate_value_z: float =None, layer_id: str=None, layer_label: str=None,
                                      m_type_label: str=None, m_type_pref_label: str=None, m_type_id: str=None,
                                      identifier: str=None, distribution_url: str=None, contribution_id: str=None,
                                      subject_id: str=None, license_id: str=None, generation_id: str=None,
                                      derivation_ids: list=None) -> dict:
        """
        
        :param at_id: The @id value of the neuron morphology        
        :param name: The name of the reconstructed neuron morphology
        :param brain_region_id: The @id value of the brain region in which the soma of the neuron morphology is located
        :param brain_region_label: The label of the brain region in which the soma of the neuron morphology is located
        :param coordinate_value_x: The x value of the brain atlas coordinate
        :param coordinate_value_y: The y value of the brain atlas coordinate
        :param coordinate_value_z: The z value of the brain atlas coordinate
        :param layer_id: The @id value of the brain layer in which the soma of the neuron morphology is located
        :param layer_label: The label of the brain layer in which the soma of the neuron morphology is located
        :param m_type_label: The label of the morphological type of the neuron morphology
        :param m_type_pref_label: The preferred label of the morphological type of the neuron morphology
        :param m_type_id: The @id value of the morphological type of the neuron morphology
        :param identifier: The identifier of the neuron morphology (e.g. from the provider)
        :param distribution_url: The url to downlooad the neuron morphology
        :param contribution_id: The @id of the contributor
        :param subject_id: The @id of the subject
        :param license_id: The @id of the license of the data
        :param generation_id: The @id of the generation of the data
        :param derivation_ids: The @id values of entities from which the data was derived
        :return: The neuron morphology payload as dict object
        """

        reconstructedneuronmorphology_payload = defaultdict(list)
        reconstructedneuronmorphology_payload["@type"] = "ReconstructedNeuronMorphology"
        reconstructedneuronmorphology_payload["@context"] = self.context
        reconstructedneuronmorphology_payload["@id"] = at_id
        reconstructedneuronmorphology_payload["name"] = name
        reconstructedneuronmorphology_payload["objectOfStudy"] = {
            "@type": "ObjectOfStudy",
            "@id": "http://bbp.epfl.ch/neurosciencegraph/taxonomies/objectsofstudy/singlecells",
            "label": "Single Cell"}
        reconstructedneuronmorphology_payload["brainLocation"] = {
            "@type": "BrainLocation",
            "brainRegion": {"@id": brain_region_id, "label": brain_region_label}}
        if coordinate_value_x:
            reconstructedneuronmorphology_payload["brainLocation"]["coordinatesInBrainAtlas"] = {
                    "valueX": {
                        "@value": coordinate_value_x,
                        "@type": "xsd:float"
                    },
                    "valueY": {
                        "@value": coordinate_value_y,
                        "@type": "xsd:float"
                    },
                    "valueZ": {
                        "@value": coordinate_value_z,
                        "@type": "xsd:float"
                    }}
        if layer_id:
            reconstructedneuronmorphology_payload["brainLocation"]["layer"] = {
                "@id": layer_id,
                "label": layer_label}
        if m_type_label:
            reconstructedneuronmorphology_payload["mType"] = {
                "@id": m_type_id,
                "label": m_type_label,
                "prefLabel": m_type_pref_label
            }
        if identifier:
            reconstructedneuronmorphology_payload["identifier"] = identifier

        if distribution_url:
            reconstructedneuronmorphology_payload["distribution"] = {"@type": "DataDownload",
                                                                     "url": distribution_url}
        if license_id:
            reconstructedneuronmorphology_payload["license"] = {
                "@type": "nsg:License",
                "@id": license_id
            }
        if contribution_id:
            reconstructedneuronmorphology_payload["contribution"] = {
                "@type": "Contribution",
                "agent": {
                    "@id": contribution_id,
                    "@type": "Organization"
                }
            }
        if subject_id:
            reconstructedneuronmorphology_payload["subject"] = {
                "@type": "Subject",
                "@id": subject_id
            }
        if derivation_ids:
            for derivation_id in derivation_ids:
                reconstructedneuronmorphology_payload["derivation"].append({"@type": "Derivation",
                                                                            "entity": {"@id": derivation_id,
                                                                                       "@type": "Entity"}})
        if generation_id:
            reconstructedneuronmorphology_payload["generation"] = {
                "@type": "Generation",
                "activity": {"@id": generation_id, "@type": "Activity"}}
        return reconstructedneuronmorphology_payload

    def labeledcell(self, at_id: str, name: str, brain_region_id: str=None, brain_region_label: str=None,
                    was_derived_from_id: str=None) -> dict:
        """
        
        :param at_id: The @id of the labeled cell        
        :param name: The name of the labeled cell
        :param brain_region_id: The @id of the brain region in which the soma of the neuron morphology is locoated
        :param brain_region_label: The label of the brain region in which the soma of the neuron morphology is locoated
        :param was_derived_from_id: The patched cell from which the labeled cell was derived
        :return: The labeled cell payload as dict object
        """
        labeledcell_payload = dict()
        labeledcell_payload["@type"] = "LabeledCell"
        labeledcell_payload["@context"] = self.context        
        labeledcell_payload["@id"] = at_id
        labeledcell_payload["name"] = name
        if brain_region_id:
            labeledcell_payload["brainLocation"] = {"brainRegion": {"@id": brain_region_id,
                                                                    "label": brain_region_label}}
        if was_derived_from_id:
            labeledcell_payload["wasDerivedFrom"] = {"@id": was_derived_from_id,
                                                     "@type": ["Entity", "PatchedCell"]}
        return labeledcell_payload

    def reconstruction(self, generated_id: str, used_id: str, at_id: str=None, had_protocol_ids: list=None,
                       ended_at_time: str=None, started_at_time: str=None,
                       was_associated_with_ids: list=None) -> dict:
        """
        
        :param generated_id: The @id of the reconstructed cell which was generated by the reconstruction activity
        :param used_id: The @id of the labeled cell which was used in the reconstruction activity
        :param at_id: @id of the reconstruction
        :param had_protocol_ids: The @id values of the protocols of this activity
        :param ended_at_time: Date time at which the activity ended 
        :param started_at_time: Date time at which the activity started
        :param was_associated_with_ids: The @id values of the agents which were associated with the activity
        :return: The reconstruction payload as dict object
        """
        reconstruction_payload = defaultdict(list)
        reconstruction_payload["@id"] = at_id
        reconstruction_payload["@type"] = "Reconstruction"
        reconstruction_payload["@context"] = self.context        
        reconstruction_payload["generated"] = {"@id": generated_id, "@type": ["ReconstructedCell", "Entity"]}
        reconstruction_payload["used"] = {"@id": used_id, "@type": ["LabeledCell", "Entity"]}
        if had_protocol_ids:
            for protocol_id in had_protocol_ids:
                reconstruction_payload["hadProtocol"].append({"@id": protocol_id, "@type": ["ExperimentalProtocol",
                                                                                          "Protocol"]})
        if started_at_time:
            reconstruction_payload["startedAtTime"]: started_at_time
        if ended_at_time:
            reconstruction_payload["endedAtTime"] = ended_at_time
        if was_associated_with_ids:
            for agent_id in was_associated_with_ids:
                reconstruction_payload["wasAssociatedWith"].append({"@id": agent_id, "@type": "Agent"})
        return reconstruction_payload

    def patchedcell(self, name: str, at_id: str, brain_region_id: str=None, brain_region_label: str=None,
                    cell_type_id: str=None, cell_type_label: str=None, was_derived_from_id: str=None,
                    dendrite_morphology: str=None)-> dict:
        """
        
        :param name: The name of the patched cell
        :param at_id: The @id of the patched cell
        :param brain_region_id: The @id of the brain region in which the soma of the patched cell is located
        :param brain_region_label: The label of the brain region in which the soma of the patched cell is located
        :param cell_type_id: The @id of the cell type of the patched cell
        :param cell_type_label: The label of the cell type of the patched cell
        :param was_derived_from_id: The entity from which the labeled cell was derived (e.g. subject)
        :param dendrite_morphology: The morphology of the dendrite (e.g. spiny, aspiny)
        :return: The patched cell as dict object
        """
        patchedcell_payload = dict()
        patchedcell_payload["@id"] = at_id
        patchedcell_payload["@type"] = "PatchedCell"
        patchedcell_payload["@context"] = self.context
        patchedcell_payload["name"] = name
        if brain_region_id:
            patchedcell_payload["brainLocation"] = {"brainRegion": {
                "@id": brain_region_id,
                "label": brain_region_label}
            }
        if cell_type_id:
            patchedcell_payload["cellType"] = {"@id": cell_type_id, "label": cell_type_label}
        if was_derived_from_id:
            patchedcell_payload["wasDerivedFrom"] = {"@id": was_derived_from_id, "@type": "Subject"}
        if dendrite_morphology:
            patchedcell_payload["dendriteMorphology"] = dendrite_morphology
        return patchedcell_payload
    
    def tracecollection(self, at_id: str, name: str, brain_region_id: str=None, brain_region_label: str=None,
                        was_derived_from_id: str=None, identifier: str=None, distribution_url: str=None,
                        contribution_id: str=None, subject_id: str=None, license_id: str=None, generation_id: str=None,
                        derivation_ids: list=None) -> dict:
        """
        
        :param at_id: The @id of the trace collection        
        :param name: The name of the trace collection
        :param brain_region_id: The identifier of the brain region
        :param brain_region_label: The label of the brain region
        :param was_derived_from_id: The @id of the entity from which the trace collection was derived
        :param identifier: The provider ID of the trace collection
        :param distribution_url: The url of the distribution of the trace collection
        :param contribution_id: The @id of the contributor
        :param subject_id: The @id of the subject
        :param license_id: The identifier of the license of the data
        :param generation_id: The @id of the entity which generated the trace collection
        :param derivation_ids: The @id values of the entities from which the trace collection was derived
        :return: The trace collection payload as dict object
        """
        tracecollection_payload = defaultdict(list)
        tracecollection_payload["@id"] = at_id
        tracecollection_payload["@type"] = "TraceCollection"
        tracecollection_payload["@context"] = self.context
        tracecollection_payload["name"] = name
        tracecollection_payload["objectOfStudy"] = {
            "@type": "ObjectOfStudy",
            "@id": "http://bbp.epfl.ch/neurosciencegraph/taxonomies/objectsofstudy/singlecells",
            "label": "Single Cell"}
        if brain_region_id:
            tracecollection_payload["brainLocation"] = {"brainRegion": {
                "@id": brain_region_id,
                "label": brain_region_label}
            }
        if was_derived_from_id:
            tracecollection_payload["wasDerivedFrom"] = {"@id": was_derived_from_id, "@type": "PatchedCell"}
        if identifier:
            tracecollection_payload["identifier"] = identifier
        if distribution_url:
            tracecollection_payload["distribution"] = {"@type": "DataDownload", "url": distribution_url}
        if license_id:
            tracecollection_payload["license"] = {
                "@type": "nsg:License",
                "@id": license_id}
        if contribution_id:
            tracecollection_payload["contribution"] = {
                "@type": "Contribution",
                "agent": {
                    "@id": contribution_id,
                    "@type": "Organization"}
            }
        if subject_id:
            tracecollection_payload["subject"] = {
                "@type": "Subject",
                "@id": subject_id
            }
        if derivation_ids:
            for derivation_id in derivation_ids:
                tracecollection_payload["derivation"].append({"@type": "Derivation", "entity": {"@id": derivation_id,
                                                                                                "@type": "Entity"}})
        if generation_id:
            tracecollection_payload["generation"] = {
                "@type": "Generation",
                "activity": {
                    "@id": generation_id,
                    "@type": "Activity"
                }}
        return tracecollection_payload

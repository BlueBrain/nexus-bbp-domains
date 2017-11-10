# Whole-cell patch-clamp recording

## Use case

### Description

This specification describes metadata collected for in vitro intracellular electrophysiology recordings using the whole-cell patch-clamp configuration. Metadata is collected on the subject used in the experiment, the slice, the patched cell which was recorded as well as the recording traces and protocols. Additionally, metadata for the brain slicing, the whole-cell patch-clamp and the stimulus used to generate traces are captured.

### Competency questions (to be completed)

The following points describe a subset of questions the provenance pattern above can support:
 
* Retrieve all electrophysiology traces generated from rat somatosensory cortex using selected stimuli
* Retrieve electrophysiology traces by recording day
* For a given stimulus / sweep / repetition, get a specific voltage and/or current trace.
* Get the liquid junction potential for an individual trace.


## Provenance pattern

![Whole-cell patch-clamp-recording](../assets/provtemplates/wholecellpatchclamp-recording-prov-template.svg)


## Entities

The different entity types involved are described below.

| Type  | Description|
| -------------                                                             | ------------- |
| [Subject](../entities/experiment/subject.html)                            |     Specimen that was used for the experimental analysis      |
| [Slice](../entities/experiment/slice.html)                                |     Brain slice obtained from the specimen      |
| [PatchedSlice](../entities/experiment/patchedslice.html)                  |     Brain slice with patched cells      |
| [PatchedCellCollection](../entities/experiment/patchedcellcollection.html)|     Collection of patched cells in a single slice |
| [PatchedCell](../entities/experiment/patchedcell.html)                    |     Cell that was patched in the slice      |
| [Trace](../entities/electrophysiology/trace.html)                         |     Individual recording trace of the patched cell (StimulationTrace and ResponseTrace)     |
| [Protocol](../entities/experiment/protocol.html)                          |     Document that describes the method used in the design and implementation of an experiment      |
    
## Activities

The different activity types involved are described below.

| Type  | Description|
| ------------- | ------------- |
| [BrainSlicing](../entities/experiment/brainslicing.html)                      |     Technique used to obtain a slice of brain tissue for patching      |
| [WholeCellPatchClamp](../entities/experiment/wholecellpatchclamp.html)        |     Technique used to study ionic currents of individual living cells    |
| [StimulusExperiment](../entities/electrophysiology/stimulusexperiment.html)   |     Technique used to obtain the electrical signature of cells through injection of a defined current patternuio |

## Agents

The different agent types involved are described below.

| Type  | Description|
| ------------- | ------------- |
| [Person](../entities/core/person.html)                                        |    Person associated with an activity      |
| [SoftwareAgent](../entities/core/softwareagent.html)                          |    Software associated with an activity      |
| [Organization](../entities/core/organization.html)                            |    Organization associated with an activity      |


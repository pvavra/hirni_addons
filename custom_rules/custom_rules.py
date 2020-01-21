"""custom rules for dicom2spec for sfb_cuetarget study"""

import json as js

class MyDICOM2SpecRules(object):

    def __init__(self, dicommetadata):
        """

        Parameter
        ----------
        dicommetadata: list of dict
            dicom metadata as extracted by datalad; one dict per image series
        """
        self._dicom_series = dicommetadata

    def __call__(self, subject=None, anon_subject=None, session=None):
        """

        Parameters
        ----------

        Returns
        -------
        list of tuple (dict, bool)
        """
        spec_dicts = []

        # check whether any "active task" present in thte current series_dict
        # we can use that to infer the session as 1 or 4 based on that
        if session == None and any(s['SeriesDescription'].startswith("fMRI_task") for s in self._dicom_series):
            session = "004"
        else:
            session = "001"

        # print("session == ")
        # print(session)
        # print("\n")

        for dicom_dict in self._dicom_series:
            spec_dicts.append((self._rules(dicom_dict,
                                           subject=subject,
                                           anon_subject=anon_subject,
                                           session=session),
                               self.series_is_valid(dicom_dict)
                               )
                              )
        return spec_dicts

    def _rules(self, series_dict, subject=None, anon_subject=None,
               session=None):

        # use this to figure out which fields you have available in the dict.
        # print('\n-----------------------\n')
        # print('\nnext series dict:\n')
        # print(series_dict)

        # figure out modality:
        task = None
        modality = None
        comment = ''
        run = None
        acquisition = None
        if series_dict['SeriesDescription'].startswith("t1"):
            modality = 'T1w'
            acquisition = 'mprage'
        if series_dict['SeriesDescription'].startswith("gre_field_mapping"):
            if "M" in series_dict['ImageType']:
                print('here')
                modality = 'magnitude' # will infer magnitude1/magnitude2 automatically
            else:
                modality = 'phasediff'
        if series_dict['SeriesDescription'].startswith("IR-EPI"):
            # c.f. https://www.ncbi.nlm.nih.gov/pubmed/14635150
            modality = 'T1w'
            acquisition = 'irepi'
        if series_dict['SeriesDescription'].startswith("DTI") and \
            series_dict['SeriesDescription'].endswith("PA"):
            modality = 'dwi'
        if series_dict['SeriesDescription'].startswith("DTI") and \
            series_dict['SeriesDescription'].endswith("AP"):
            # the A >> P series does have any diffusion-weighting, and is
            # essentially only for the correction of distortions for the SE-EPI
            modality = 'epi'
        if series_dict['SeriesDescription'].startswith("fMRI_loc"):
            modality = 'bold'
            task = 'localizer'
        if series_dict['SeriesDescription'].startswith("fMRI_task"):
            modality = 'bold'
            task = 'active'
            # number afterwards indicates run number (range: 1 to 4)
            run = series_dict['SeriesDescription'][len("fMRI_task")]
        if series_dict['SeriesDescription'].startswith("fMRI_withouttask"):
            modality = 'bold'
            task = 'passive'
            # number afterwards indicates run number (range: 1 to 4)
            run = series_dict['SeriesDescription'][len("fMRI_withouttask")]
        if series_dict['SeriesDescription'].startswith("fMRI_resting"):
            modality = 'bold'
            task = 'rest'
        # for any single-band reference image, overwrite to `sbref` instead of bold
        if series_dict['SeriesDescription'].endswith("SBRef"):
            modality = 'sbref'

        if series_dict['SeriesDescription'].startswith("AAHead_Scout"):
            comment = "Localizer - will be ignored for BIDS"

        return {'description': series_dict['SeriesDescription']
                if "SeriesDescription" in series_dict else '',
                'comment': comment,
                'subject': series_dict['PatientID'] if not subject else subject,
                'anon-subject': anon_subject if anon_subject else None,
                'bids-session': session if session else None,
                'bids-modality' : modality,
                'bids-task': task,
                'bids-run': run,
                'bids-acquisition': acquisition
                }

    def series_is_valid(self, series_dict):
        # For all series which this returns `false`, the hirni-spec2bids will
        # skip the conversion to niftis.

        # Skip all localizers
        if series_dict['SeriesDescription'].startswith("AAHead_Scout"):
            valid = False
        else:
            valid = True

        return valid

__datalad_hirni_rules = MyDICOM2SpecRules

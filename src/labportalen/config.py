# Python import

# Django import

# Self import
HEALTH_CHECK_TYPE = '0ec720fc-669c-48b4-8c72-5802f0b88c4d'  # fixed for the time beign


class Config:
    analysis_dict = {
        "ALAT": {
            'AnalysisName': 'ALAT',
            'AnalysisCode': 'NPU19981',
            'QuestionIds': None
        },
        "ALP": {
            'AnalysisName': 'ALP',
            'AnalysisCode': 'NPU01144',
            'QuestionIds': None
        },
        "Natrium (Na)": {
            'AnalysisName': 'Natrium (Na)',
            'AnalysisCode': 'NPU03429',
            'QuestionIds': None
        },
        "K": {
            'AnalysisName': 'K',
            'AnalysisCode': 'SWE05127',
            'QuestionIds': None
        },
        "Kreatinin (krea)": {
            'AnalysisName': 'Kreatinin (krea)',
            'AnalysisCode': 'ML200899',
            'QuestionIds': None
        },
        "Korrigerat calcium (korr-Ca)": {
            'AnalysisName': 'Korrigerat calcium (korr-Ca)',
            'AnalysisCode': 'ML100372',
            'QuestionIds': None
        },
        "HbA1c (långtidsblodsocker)": {
            'AnalysisName': 'HbA1c (långtidsblodsocker)',
            'AnalysisCode': 'NPU27300',
            'QuestionIds': None
        },
        "Total Kolesterol (blodfetter)": {
            'AnalysisName': 'Total Kolesterol (blodfetter)',
            'AnalysisCode': 'NPU01566',
            'QuestionIds': None
        },
        "LDL -onda kolesterolet": {
            'AnalysisName': 'LDL -onda kolesterolet',
            'AnalysisCode': 'NPU01568',
            'QuestionIds': None
        },
        "HDL": {
            'AnalysisName': 'HDL',
            'AnalysisCode': 'NPU01567',
            'QuestionIds': None
        },
        "Triglycerider": {
            'AnalysisName': 'Triglycerider',
            'AnalysisCode': 'NPU04094',
            'QuestionIds': None
        },
        "Ferritin": {
            'AnalysisName': 'Ferritin',
            'AnalysisCode': 'NPU19763',
            'QuestionIds': None
        },
        "TSH": {
            'AnalysisName': 'TSH',
            'AnalysisCode': 'NPU03577',
            'QuestionIds': None
        },
        "T4 fritt": {
            'AnalysisName': 'T4 fritt',
            'AnalysisCode': 'NPU03579',
            'QuestionIds': None
        },
        "Hb (Hemoglobin, blodvärde)": {
            'AnalysisName': 'Hb (Hemoglobin, blodvärde)',
            'AnalysisCode': 'SWE05074',
            'QuestionIds': None
        },
        "Faste blodglukos (fB-glc, blodsocker)": {
            'AnalysisName': 'Faste blodglukos (fB-glc, blodsocker)',
            'AnalysisCode': 'ML201041',
            'QuestionIds': None
        }
    }

    lab_list = [
        {
            "lab_code": "ALMED",
            "lab_name": "SYNLAB (Medilab)"
        },

        {
            "lab_code": "A1345",
            "lab_name": "Infosolutions Lab"
        }
    ]

    type_1_analysis_list = [analysis_dict['ALAT'], analysis_dict['ALP'], analysis_dict['Natrium (Na)'], analysis_dict['K'], analysis_dict['Kreatinin (krea)'], analysis_dict['Korrigerat calcium (korr-Ca)'], analysis_dict['HbA1c (långtidsblodsocker)'],
                            analysis_dict['Total Kolesterol (blodfetter)'], analysis_dict['LDL -onda kolesterolet'], analysis_dict['HDL'], analysis_dict['Triglycerider'], analysis_dict['Ferritin'], analysis_dict['TSH'], analysis_dict['T4 fritt']]
    hc_type_analysis_dict = {  # keys are the code_names of health check type
        HEALTH_CHECK_TYPE: type_1_analysis_list
    }
from collections import OrderedDict

#
# define types for synthea schema
#
class ModelSyntheaPandas:
    #
    # Check the model matches
    #
    def __init__(self):
       self.model_schema = self.syntheaSchema()

    #
    # define omop schema here
    # The DATE fields are read in as string.  They can be converted to DATE
    # objects if necessary
    # OMOP V5.3.1
    #
    def syntheaSchema(self):
        model_schema = OrderedDict([])
        #
        # Standardized vocabulary
        #
        model_schema['allergies'] = OrderedDict([
            ('START', 'object'),
            ('STOP', 'object'),
            ('PATIENT', 'object'),
            ('ENCOUNTER', 'object'),
            ('CODE', 'category'),
            ('DESCRIPTION', 'category')
        ])

        model_schema['careplans'] = OrderedDict([
            ('Id', 'object'),
            ('START', 'object'),
            ('STOP', 'object'),
            ('PATIENT', 'object'),
            ('ENCOUNTER', 'object'),
            ('CODE', 'category'),
            ('DESCRIPTION', 'category'),
            ('REASONCODE', 'category'),
            ('REASONDESCRIPTION', 'category')
        ])

        model_schema['conditions'] = OrderedDict([
            ('START', 'category'),
            ('STOP', 'category'),
            ('PATIENT', 'category'),
            ('ENCOUNTER', 'category'),
            ('CODE', 'category'),
            ('DESCRIPTION', 'category')
        ])

        model_schema['encounters'] = OrderedDict([
            ('Id', 'object'),
            ('START', 'category'),
            ('STOP', 'category'),
            ('PATIENT', 'category'),
            ('PROVIDER', 'category'),
            ('PAYER', 'category'),
            ('ENCOUNTERCLASS', 'category'),
            ('CODE', 'category'),
            ('DESCRIPTION', 'category'),
            ('BASE_ENCOUNTER_COST', 'float16'),
            ('TOTAL_CLAIM_COST', 'float16'),
            ('PAYER_COVERAGE', 'float16'),
            ('REASONCODE', 'category'),
            ('REASONDESCRIPTION', 'category')
        ])

        model_schema['imaging_studies'] = OrderedDict([
            ('Id', 'object'),
            ('DATE', 'object'),
            ('PATIENT', 'object'),
            ('ENCOUNTER', 'object'),
            ('BODY_SITE_CODE', 'category'),
            ('BODY_SITE_DESCRIPTION', 'category'),
            ('MODALITY_CODE', 'category'),
            ('MODALITY_DESCRIPTION', 'category'),
            ('SOP_CODE', 'category'),
            ('SOP_DESCRIPTION', 'category')
        ])

        model_schema['immunizations'] = OrderedDict([
            ('DATE', 'object'),
            ('PATIENT', 'object'),
            ('ENCOUNTER', 'object'),
            ('CODE', 'category'),
            ('DESCRIPTION', 'category'),
            ('COST', 'float32')
        ])

        model_schema['medications'] = OrderedDict([
            ('START', 'object'),
            ('STOP', 'object'),
            ('PATIENT', 'category'),
            ('PAYER', 'category'),
            ('ENCOUNTER', 'object'),
            ('CODE', 'category'),
            ('DESCRIPTION', 'category'),
            ('BASE_COST', 'float32'),
            ('PAYER_coverage', 'float16'),
            ('DISPENSES', 'int8'),
            ('TOTALCOST', 'float16'),
            ('REASONCODE', 'category'),
            ('REASONDESCRIPTION', 'category')
        ])

        model_schema['observations'] = OrderedDict([
            ('DATE', 'category'),
            ('PATIENT', 'category'),
            ('ENCOUNTER', 'category'),
            ('CODE', 'category'),
            ('DESCRIPTION', 'category'),
            ('VALUE', 'category'),
            ('UNITS', 'category'),
            ('TYPE', 'category')
        ])

        model_schema['organizations'] = OrderedDict([
            ('Id', 'object'),
            ('NAME', 'object'),
            ('ADDRESS', 'object'),
            ('CITY', 'category'),
            ('STATE', 'category'),
            ('ZIP', 'category'),
            ('LAT', 'float32'),
            ('LON', 'float32'),
            ('PHONE', 'object'),
            ('REVENUE', 'float32'),
            ('utilization', 'float32')
        ])

        model_schema['patients'] = OrderedDict([
            ('Id', 'object'),
            ('BIRTHDATE', 'object'),
            ('DEATHDATE', 'object'),
            ('SSN', 'object'),
            ('DRIVERS', 'object'),
            ('PASSPORT', 'object'),
            ('PREFIX', 'category'),
            ('FIRST', 'category'),
            ('LAST', 'category'),
            ('SUFFIX', 'category'),
            ('MAIDEN', 'category'),
            ('MARITAL', 'category'),
            ('RACE', 'category'),
            ('ETHNICITY', 'category'),
            ('GENDER', 'category'),
            ('BIRTHPLACE', 'category'),
            ('ADDRESS', 'object'),
            ('CITY', 'category'),
            ('COUNTY', 'category'),
            ('STATE', 'category'),
            ('ZIP', 'category'),
            ('LAT', 'float32'),
            ('LON', 'float32'),
            ('HEALTHCARE_EXPENSE', 'float32'),
            ('HEALTHCARE_COVERAGE', 'float32')
        ])

        model_schema['payer_transitions'] = OrderedDict([
            ('PATIENT', 'object'),
            ('START_YEAR', 'object'),
            ('STOP_YEAR', 'object'),
            ('PATIENT', 'object'),
            ('PAYER', 'category'),
            ('OWNERSHIP', 'category')
        ])

        model_schema['payers'] = OrderedDict([
            ('Id', 'object'),
            ('NAME', 'object'),
            ('ADDRESS', 'object'),
            ('CITY', 'object'),
            ('STATE_HEADQUARTERED', 'category'),
            ('ZIP', 'category'),
            ('PHONE', 'cateogry'),
            ('AMOUNT_COVERED', 'float32'),
            ('REVENUE', 'float32'),
            ('COVERED_ENCOUNTERs', 'float32'),
            ('UNCOVERED_ENCOUNTERs', 'float32'),
            ('COVERED_MEDICATIONS', 'float32'),
            ('UNCOVERED_MEDICATIONS', 'float32'),
            ('COVERED_PROCESURES', 'float32'),
            ('UNCOVERED_PROCESURES', 'float32'),
            ('COVERED_IMMUNIZATIONS', 'float32'),
            ('UNCOVERED_IMMUNIZATIONS', 'float32'),
            ('UNIQUE_CUSTOMERS', 'float32'),
            ('QOLS_AVG', 'float32'),
            ('MEMBER_MONTHS', 'float32')
        ])

        model_schema['procedures'] = OrderedDict([
            ('DATE', 'object'),
            ('PATIENT', 'category'),
            ('ENCOUNTER', 'object'),
            ('CODE', 'category'),
            ('DESCRIPTION', 'category'),
            ('BASE_COST', 'category'),
            ('REASONCODE', 'category'),
            ('REASONDESCRIPTION', 'category')
        ])

        model_schema['providers'] = OrderedDict([
            ('Id', 'object'),
            ('ORGANIZATION', 'object'),
            ('NAME', 'object'),
            ('GENDER', 'category'),
            ('SPECIALITY', 'category'),
            ('ADDRESS', 'object'),
            ('CITY', 'category'),
            ('STATE', 'category'),
            ('ZIP', 'category'),
            ('LAT', 'float32'),
            ('LON', 'float32'),
            ('UTILIZATION', 'float32')
        ])

        # resource files providers model
        model_schema['zipcodes'] = OrderedDict([
            ('USPS', 'object'),
            ('ST', 'object'),
            ('NAME', 'object'),
            ('ZCTA5', 'object'),
            ('LAT', 'object'),
            ('LON', 'object'),
        ])

        model_schema['hospitals'] = OrderedDict([
            ('id', 'object'),
            ('name', 'object'),
            ('address', 'object'),
            ('city', 'category'),
            ('state', 'category'),
            ('zip', 'category'),
            ('county', 'category'),
            ('phone', 'category'),
            ('type', 'category'),
            ('ownership', 'object'),
            ('emergency', 'category'),
            ('quality', 'float32'),
            ('LAT', 'float32'),
            ('LON', 'float32')
        ])

        model_schema['primary_care_facilities'] = OrderedDict([
            ('name', 'object'),
            ('address', 'object'),
            ('city', 'object'),
            ('state', 'object'),
            ('zip', 'object'),
            ('phone', 'object'),
            ('LAT', 'object'),
            ('LON', 'object'),
            ('hasSpecialties', 'object'),
            ('ADDICTION MEDICINE', 'object'),
            ('ADVANCED HEART FAILURE AND TRANSPLANT CARDIOLOGY', 'object'),
            ('ALLERGY/IMMUNOLOGY', 'object'),
            ('ANESTHESIOLOGY', 'object'),
            ('ANESTHESIOLOGY ASSISTANT', 'object'),
            ('AUDIOLOGIST', 'object'),
            ('CARDIAC ELECTROPHYSIOLOGY', 'object'),
            ('CARDIAC SURGERY', 'object'),
            ('CARDIOVASCULAR DISEASE (CARDIOLOGY)', 'object'),
            ('CERTIFIED NURSE MIDWIFE', 'object'),
            ('CERTIFIED REGISTERED NURSE ANESTHETIST', 'object'),
            ('CHIROPRACTIC', 'object'),
            ('CLINICAL NURSE SPECIALIST', 'object'),
            ('CLINICAL PSYCHOLOGIST', 'object'),
            ('CLINICAL SOCIAL WORKER', 'object'),
            ('COLORECTAL SURGERY (PROCTOLOGY)', 'object'),
            ('CRITICAL CARE (INTENSIVISTS)', 'object'),
            ('DENTIST', 'object'),
            ('DERMATOLOGY', 'object'),
            ('DIAGNOSTIC RADIOLOGY', 'object'),
            ('EMERGENCY MEDICINE', 'object'),
            ('ENDOCRINOLOGY', 'object'),
            ('FAMILY PRACTICE', 'object'),
            ('GASTROENTEROLOGY', 'object'),
            ('GENERAL PRACTICE', 'object'),
            ('GENERAL SURGERY', 'object'),
            ('GERIATRIC MEDICINE', 'object'),
            ('GERIATRIC PSYCHIATRY', 'object'),
            ('GYNECOLOGICAL ONCOLOGY', 'object'),
            ('HAND SURGERY', 'object'),
            ('HEMATOLOGY', 'object'),
            ('HEMATOLOGY/ONCOLOGY', 'object'),
            ('HEMATOPOIETIC CELL TRANSPLANTATION AND CELLULAR TH', 'object'),
            ('HOSPICE/PALLIATIVE CARE', 'object'),
            ('HOSPITALIST', 'object'),
            ('INFECTIOUS DISEASE', 'object'),
            ('INTERNAL MEDICINE', 'object'),
            ('INTERVENTIONAL CARDIOLOGY', 'object'),
            ('INTERVENTIONAL PAIN MANAGEMENT', 'object'),
            ('INTERVENTIONAL RADIOLOGY', 'object'),
            ('MAXILLOFACIAL SURGERY', 'object'),
            ('MEDICAL ONCOLOGY', 'object'),
            ('NEPHROLOGY', 'object'),
            ('NEUROLOGY', 'object'),
            ('NEUROPSYCHIATRY', 'object'),
            ('NEUROSURGERY', 'object'),
            ('NUCLEAR MEDICINE', 'object'),
            ('NURSE PRACTITIONER', 'object'),
            ('OBSTETRICS/GYNECOLOGY', 'object'),
            ('OCCUPATIONAL THERAPY', 'object'),
            ('OPHTHALMOLOGY', 'object'),
            ('OPTOMETRY', 'object'),
            ('ORAL SURGERY', 'object'),
            ('ORTHOPEDIC SURGERY', 'object'),
            ('OSTEOPATHIC MANIPULATIVE MEDICINE', 'object'),
            ('OTOLARYNGOLOGY', 'object'),
            ('PAIN MANAGEMENT', 'object'),
            ('PATHOLOGY', 'object'),
            ('PEDIATRIC MEDICINE', 'object'),
            ('PERIPHERAL VASCULAR DISEASE', 'object'),
            ('PHYSICAL MEDICINE AND REHABILITATION', 'object'),
            ('PHYSICAL THERAPY', 'object'),
            ('PHYSICIAN ASSISTANT', 'object'),
            ('PLASTIC AND RECONSTRUCTIVE SURGERY', 'object'),
            ('PODIATRY', 'object'),
            ('PREVENTATIVE MEDICINE', 'object'),
            ('PSYCHIATRY', 'object'),
            ('PULMONARY DISEASE', 'object'),
            ('RADIATION ONCOLOGY', 'object'),
            ('REGISTERED DIETITIAN OR NUTRITION PROFESSIONAL', 'object'),
            ('RHEUMATOLOGY,', 'object'),
            ('SLEEP MEDICINE', 'object'),
            ('SPEECH LANGUAGE PATHOLOGIST', 'object'),
            ('SPORTS MEDICINE', 'object'),
            ('SURGICAL ONCOLOGY', 'object'),
            ('THORACIC SURGERY', 'object'),
            ('UNDEFINED PHYSICIAN TYPE (SPECIFY)', 'object'),
            ('UROLOGY,', 'object'),
            ('VASCULAR SURGERY', 'object'),
            ('id', 'object')
        ])

        model_schema['providers'] = OrderedDict([
            ('Id', 'object'),
            ('ORGANIZATION', 'object'),
            ('NAME', 'object'),
            ('GENDER', 'category'),
            ('SPECIALITY', 'category'),
            ('ADDRESS', 'object'),
            ('CITY', 'category'),
            ('STATE', 'category'),
            ('ZIP', 'category'),
            ('LAT', 'object'),
            ('LON', 'object'),
            ('UTILIZATION', 'float32')
        ])

        model_schema['urgent_care_facilities'] = OrderedDict([
            ('id', 'object'),
            ('name', 'object'),
            ('address', 'object'),
            ('city', 'category'),
            ('state', 'category'),
            ('zip', 'category'),
            ('county', 'category'),
            ('phone', 'category'),
            ('type', 'category'),
            ('ownership', 'object'),
            ('emergency', 'category'),
            ('quality', 'float32'),
            ('LAT', 'object'),
            ('LON', 'object')
        ])

        model_schema['demographics'] = OrderedDict([
            ('ID', 'object'),
            ('COUNTY', 'object'),
            ('NAME', 'object'),
            ('STNAME', 'category'),
            ('POPESTIMATE2015', 'object'),
            ('CTYNAME', 'category'),
            ('TOT_POP', 'object'),
            ('TOT_MALE', 'object'),
            ('TOT_FEMALE', 'object'),
            ('WHITE', 'object'),
            ('HISPANIC', 'object'),
            ('BLACK', 'object'),
            ('ASIAN', 'object'),
            ('NATIVE', 'object'),
            ('OTHER', 'object'),
            ('1', 'object'),
            ('2', 'object'),
            ('3', 'object'),
            ('4', 'object'),
            ('5', 'object'),
            ('6', 'object'),
            ('7', 'object'),
            ('8', 'object'),
            ('9', 'object'),
            ('10', 'object'),
            ('11', 'object'),
            ('12', 'object'),
            ('13', 'object'),
            ('14', 'object'),
            ('15', 'object'),
            ('16', 'object'),
            ('17', 'object'),
            ('18', 'object'),
            ('00..10', 'object'),
            ('10..15', 'object'),
            ('15..25', 'object'),
            ('25..35', 'object'),
            ('35..50', 'object'),
            ('50..75', 'object'),
            ('75..100', 'object'),
            ('100..150', 'object'),
            ('150..200', 'object'),
            ('200..999', 'object'),
            ('LESS_THAN_HS', 'object'),
            ('HS_DEGREE', 'object'),
            ('SOME_COLLEGE', 'object'),
            ('BS_DEGRE', 'object')
        ])

        return model_schema

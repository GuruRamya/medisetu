import re
REFERENCE_RANGES = {
    "hemoglobin": {
        "aliases": ["hemoglobin", "hb", "haemoglobin"],
        "male": {"min": 13.0, "max": 17.0},
        "female": {"min": 12.0, "max": 15.5},
        "default": {"min": 12.0, "max": 17.0},
        "unit": "g/dL",
        "description": "Red blood cell protein that carries oxygen"
    },
    "wbc": {
        "aliases": ["wbc", "white blood cells", "total wbc", "total leucocyte count", "tlc", "leukocytes"],
        "default": {"min": 4000, "max": 11000},
        "unit": "cells/mcL",
        "description": "White blood cells that fight infection"
    },
    "rbc": {
        "aliases": ["rbc", "red blood cells", "red blood cell count"],
        "male": {"min": 4.5, "max": 5.9},
        "female": {"min": 4.0, "max": 5.2},
        "default": {"min": 4.0, "max": 5.9},
        "unit": "million/mcL",
        "description": "Red blood cells that carry oxygen"
    },
    "platelets": {
        "aliases": ["platelets", "platelet count", "plt", "thrombocytes"],
        "default": {"min": 150000, "max": 400000},
        "unit": "cells/mcL",
        "description": "Cells that help blood clot"
    },
    "hematocrit": {
        "aliases": ["hematocrit", "hct", "packed cell volume", "pcv"],
        "male": {"min": 40, "max": 52},
        "female": {"min": 36, "max": 48},
        "default": {"min": 36, "max": 52},
        "unit": "%",
        "description": "Percentage of blood made up of red blood cells"
    },
    "mcv": {
        "aliases": ["mcv", "mean corpuscular volume"],
        "default": {"min": 80, "max": 100},
        "unit": "fL",
        "description": "Average size of red blood cells"
    },
    "mch": {
        "aliases": ["mch", "mean corpuscular hemoglobin"],
        "default": {"min": 27, "max": 33},
        "unit": "pg",
        "description": "Average amount of hemoglobin per red blood cell"
    },
    "mchc": {
        "aliases": ["mchc", "mean corpuscular hemoglobin concentration"],
        "default": {"min": 32, "max": 36},
        "unit": "g/dL",
        "description": "Concentration of hemoglobin in red blood cells"
    },
    "neutrophils": {
        "aliases": ["neutrophils", "neutrophil"],
        "default": {"min": 40, "max": 70},
        "unit": "%",
        "description": "Type of white blood cell that fights bacterial infections"
    },
    "lymphocytes": {
        "aliases": ["lymphocytes", "lymphocyte"],
        "default": {"min": 20, "max": 40},
        "unit": "%",
        "description": "Type of white blood cell that fights viral infections"
    },
    "monocytes": {
        "aliases": ["monocytes", "monocyte"],
        "default": {"min": 2, "max": 8},
        "unit": "%",
        "description": "Type of white blood cell that fights infections"
    },
    "eosinophils": {
        "aliases": ["eosinophils", "eosinophil"],
        "default": {"min": 1, "max": 6},
        "unit": "%",
        "description": "Type of white blood cell involved in allergic reactions"
    },
    "basophils": {
        "aliases": ["basophils", "basophil"],
        "default": {"min": 0, "max": 1},
        "unit": "%",
        "description": "Type of white blood cell involved in inflammation"
    },
    "fasting_glucose": {
        "aliases": ["fasting glucose", "fbs", "fasting blood sugar", "fasting blood glucose", "glucose fasting"],
        "default": {"min": 70, "max": 100},
        "unit": "mg/dL",
        "description": "Blood sugar level after fasting",
        "zones": {
            "normal": {"min": 70, "max": 100},
            "prediabetes": {"min": 100, "max": 126},
            "diabetes": {"min": 126, "max": 99999}
        }
    },
    "postprandial_glucose": {
        "aliases": ["pp glucose", "ppbs", "post prandial", "postprandial glucose", "2hr pp"],
        "default": {"min": 70, "max": 140},
        "unit": "mg/dL",
        "description": "Blood sugar level 2 hours after eating"
    },
    "random_glucose": {
        "aliases": ["random glucose", "rbs", "random blood sugar"],
        "default": {"min": 70, "max": 140},
        "unit": "mg/dL",
        "description": "Blood sugar level at any time"
    },
    "hba1c": {
        "aliases": ["hba1c", "glycated hemoglobin", "glycosylated hemoglobin", "a1c"],
        "default": {"min": 4.0, "max": 5.7},
        "unit": "%",
        "description": "3-month average blood sugar level",
        "zones": {
            "normal": {"min": 4.0, "max": 5.7},
            "prediabetes": {"min": 5.7, "max": 6.5},
            "diabetes": {"min": 6.5, "max": 99999}
        }
    },
    "total_cholesterol": {
        "aliases": ["total cholesterol", "cholesterol total", "cholesterol"],
        "default": {"min": 0, "max": 200},
        "unit": "mg/dL",
        "description": "Total amount of cholesterol in blood"
    },
    "ldl": {
        "aliases": ["ldl", "ldl cholesterol", "low density lipoprotein"],
        "default": {"min": 0, "max": 100},
        "unit": "mg/dL",
        "description": "Bad cholesterol — high levels increase heart disease risk"
    },
    "hdl": {
        "aliases": ["hdl", "hdl cholesterol", "high density lipoprotein"],
        "male": {"min": 40, "max": 999},
        "female": {"min": 50, "max": 999},
        "default": {"min": 40, "max": 999},
        "unit": "mg/dL",
        "description": "Good cholesterol — higher is better"
    },
    "triglycerides": {
        "aliases": ["triglycerides", "tg", "trigs"],
        "default": {"min": 0, "max": 150},
        "unit": "mg/dL",
        "description": "Type of fat in blood — high levels increase heart disease risk"
    },
    "vldl": {
        "aliases": ["vldl", "very low density lipoprotein"],
        "default": {"min": 2, "max": 30},
        "unit": "mg/dL",
        "description": "Very bad cholesterol type"
    },
    "alt": {
        "aliases": ["alt", "sgpt", "alanine aminotransferase", "alanine transaminase"],
        "male": {"min": 7, "max": 56},
        "female": {"min": 7, "max": 45},
        "default": {"min": 7, "max": 56},
        "unit": "U/L",
        "description": "Liver enzyme — high levels indicate liver damage"
    },
    "ast": {
        "aliases": ["ast", "sgot", "aspartate aminotransferase", "aspartate transaminase"],
        "male": {"min": 10, "max": 40},
        "female": {"min": 10, "max": 35},
        "default": {"min": 10, "max": 40},
        "unit": "U/L",
        "description": "Liver enzyme — high levels indicate liver or heart damage"
    },
    "alp": {
        "aliases": ["alp", "alkaline phosphatase"],
        "default": {"min": 44, "max": 147},
        "unit": "U/L",
        "description": "Enzyme found in liver and bones"
    },
    "bilirubin_total": {
        "aliases": ["bilirubin total", "total bilirubin", "t bilirubin", "tbil"],
        "default": {"min": 0.2, "max": 1.2},
        "unit": "mg/dL",
        "description": "Yellow pigment from red blood cell breakdown"
    },
    "bilirubin_direct": {
        "aliases": ["bilirubin direct", "direct bilirubin", "d bilirubin", "dbil"],
        "default": {"min": 0.0, "max": 0.3},
        "unit": "mg/dL",
        "description": "Direct bilirubin processed by liver"
    },
    "bilirubin_indirect": {
        "aliases": ["bilirubin indirect", "indirect bilirubin", "i bilirubin"],
        "default": {"min": 0.2, "max": 0.9},
        "unit": "mg/dL",
        "description": "Indirect bilirubin not yet processed by liver"
    },
    "total_protein": {
        "aliases": ["total protein", "protein total"],
        "default": {"min": 6.0, "max": 8.3},
        "unit": "g/dL",
        "description": "Total protein in blood"
    },
    "albumin": {
        "aliases": ["albumin", "serum albumin"],
        "default": {"min": 3.5, "max": 5.0},
        "unit": "g/dL",
        "description": "Main protein made by liver"
    },
    "globulin": {
        "aliases": ["globulin", "serum globulin"],
        "default": {"min": 2.0, "max": 3.5},
        "unit": "g/dL",
        "description": "Group of proteins in blood"
    },
    "creatinine": {
        "aliases": ["creatinine", "serum creatinine", "s creatinine"],
        "male": {"min": 0.7, "max": 1.3},
        "female": {"min": 0.5, "max": 1.1},
        "default": {"min": 0.5, "max": 1.3},
        "unit": "mg/dL",
        "description": "Waste product filtered by kidneys"
    },
    "urea": {
        "aliases": ["urea", "blood urea", "serum urea", "bun", "blood urea nitrogen"],
        "default": {"min": 7, "max": 25},
        "unit": "mg/dL",
        "description": "Waste product from protein breakdown filtered by kidneys"
    },
    "uric_acid": {
        "aliases": ["uric acid", "serum uric acid"],
        "male": {"min": 3.5, "max": 7.2},
        "female": {"min": 2.6, "max": 6.0},
        "default": {"min": 2.6, "max": 7.2},
        "unit": "mg/dL",
        "description": "Waste product from purine breakdown"
    },
    "egfr": {
        "aliases": ["egfr", "gfr", "estimated gfr", "glomerular filtration rate"],
        "default": {"min": 60, "max": 999},
        "unit": "mL/min/1.73m²",
        "description": "Kidney filtration rate — higher is better"
    },
    "sodium": {
        "aliases": ["sodium", "na", "serum sodium"],
        "default": {"min": 136, "max": 145},
        "unit": "mEq/L",
        "description": "Electrolyte that controls fluid balance"
    },
    "potassium": {
        "aliases": ["potassium", "k", "serum potassium"],
        "default": {"min": 3.5, "max": 5.0},
        "unit": "mEq/L",
        "description": "Electrolyte important for heart and muscle function"
    },
    "chloride": {
        "aliases": ["chloride", "cl", "serum chloride"],
        "default": {"min": 98, "max": 107},
        "unit": "mEq/L",
        "description": "Electrolyte that maintains fluid balance"
    },
    "calcium": {
        "aliases": ["calcium", "ca", "serum calcium", "total calcium"],
        "default": {"min": 8.5, "max": 10.5},
        "unit": "mg/dL",
        "description": "Mineral important for bones, muscles and nerves"
    },
    "phosphorus": {
        "aliases": ["phosphorus", "phosphate", "serum phosphorus"],
        "default": {"min": 2.5, "max": 4.5},
        "unit": "mg/dL",
        "description": "Mineral important for bones and energy"
    },
    "tsh": {
        "aliases": ["tsh", "thyroid stimulating hormone"],
        "default": {"min": 0.4, "max": 4.0},
        "unit": "mIU/L",
        "description": "Hormone that controls thyroid function"
    },
    "t3": {
        "aliases": ["t3", "triiodothyronine", "total t3"],
        "default": {"min": 80, "max": 200},
        "unit": "ng/dL",
        "description": "Active thyroid hormone"
    },
    "t4": {
        "aliases": ["t4", "thyroxine", "total t4"],
        "default": {"min": 5.0, "max": 12.0},
        "unit": "mcg/dL",
        "description": "Main thyroid hormone"
    },
    "free_t3": {
        "aliases": ["free t3", "ft3", "free triiodothyronine"],
        "default": {"min": 2.3, "max": 4.2},
        "unit": "pg/mL",
        "description": "Free active thyroid hormone"
    },
    "free_t4": {
        "aliases": ["free t4", "ft4", "free thyroxine"],
        "default": {"min": 0.8, "max": 1.8},
        "unit": "ng/dL",
        "description": "Free main thyroid hormone"
    },
    "iron": {
        "aliases": ["iron", "serum iron", "fe"],
        "male": {"min": 65, "max": 175},
        "female": {"min": 50, "max": 170},
        "default": {"min": 50, "max": 175},
        "unit": "mcg/dL",
        "description": "Mineral needed to make hemoglobin"
    },
    "ferritin": {
        "aliases": ["ferritin", "serum ferritin"],
        "male": {"min": 20, "max": 250},
        "female": {"min": 10, "max": 120},
        "default": {"min": 10, "max": 250},
        "unit": "ng/mL",
        "description": "Protein that stores iron in body"
    },
    "tibc": {
        "aliases": ["tibc", "total iron binding capacity"],
        "default": {"min": 250, "max": 370},
        "unit": "mcg/dL",
        "description": "Capacity of blood to carry iron"
    },
    "vitamin_d": {
        "aliases": ["vitamin d", "vit d", "25 oh vitamin d", "25-hydroxyvitamin d"],
        "default": {"min": 30, "max": 100},
        "unit": "ng/mL",
        "description": "Vitamin important for bone health and immunity",
        "zones": {
            "deficient": {"min": 0, "max": 20},
            "insufficient": {"min": 20, "max": 30},
            "normal": {"min": 30, "max": 100},
            "toxic": {"min": 100, "max": 99999}
        }
    },
    "vitamin_b12": {
        "aliases": ["vitamin b12", "vit b12", "cobalamin", "b12"],
        "default": {"min": 200, "max": 900},
        "unit": "pg/mL",
        "description": "Vitamin important for nerves and blood cells"
    },
    "crp": {
        "aliases": ["crp", "c reactive protein", "c-reactive protein"],
        "default": {"min": 0, "max": 5},
        "unit": "mg/L",
        "description": "Marker of inflammation in the body"
    },
    "esr": {
        "aliases": ["esr", "erythrocyte sedimentation rate"],
        "male": {"min": 0, "max": 15},
        "female": {"min": 0, "max": 20},
        "default": {"min": 0, "max": 20},
        "unit": "mm/hr",
        "description": "Marker of inflammation"
    },
    "insulin_fasting": {
        "aliases": ["insulin fasting", "fasting insulin", "serum insulin"],
        "default": {"min": 2.6, "max": 24.9},
        "unit": "mcIU/mL",
        "description": "Insulin level after fasting — checks for insulin resistance"
    },
    "homa_ir": {
        "aliases": ["homa ir", "homa-ir", "insulin resistance"],
        "default": {"min": 0, "max": 2.5},
        "unit": "",
        "description": "Measure of insulin resistance"
    },
    "psa": {
        "aliases": ["psa", "prostate specific antigen"],
        "default": {"min": 0, "max": 4.0},
        "unit": "ng/mL",
        "description": "Prostate cancer screening marker (males)"
    },
    "amylase": {
        "aliases": ["amylase", "serum amylase"],
        "default": {"min": 28, "max": 100},
        "unit": "U/L",
        "description": "Enzyme from pancreas — high levels indicate pancreatitis"
    },
    "lipase": {
        "aliases": ["lipase", "serum lipase"],
        "default": {"min": 10, "max": 140},
        "unit": "U/L",
        "description": "Enzyme from pancreas that digests fat"
    },
    "ggt": {
        "aliases": ["ggt", "gamma gt", "gamma glutamyl transferase"],
        "male": {"min": 9, "max": 48},
        "female": {"min": 9, "max": 32},
        "default": {"min": 9, "max": 48},
        "unit": "U/L",
        "description": "Liver enzyme — elevated in liver disease and alcohol use"
    },
    "ldh": {
        "aliases": ["ldh", "lactate dehydrogenase", "lactic dehydrogenase"],
        "default": {"min": 140, "max": 280},
        "unit": "U/L",
        "description": "Enzyme released when tissue is damaged"
    },
    "cpk": {
        "aliases": ["cpk", "ck", "creatine phosphokinase", "creatine kinase"],
        "male": {"min": 39, "max": 308},
        "female": {"min": 26, "max": 192},
        "default": {"min": 26, "max": 308},
        "unit": "U/L",
        "description": "Enzyme from muscles and heart — high levels indicate muscle damage"
    },
    "troponin": {
        "aliases": ["troponin", "troponin i", "troponin t"],
        "default": {"min": 0, "max": 0.04},
        "unit": "ng/mL",
        "description": "Heart muscle protein — elevated in heart attack"
    },
    "bnp": {
        "aliases": ["bnp", "brain natriuretic peptide", "nt-probnp"],
        "default": {"min": 0, "max": 100},
        "unit": "pg/mL",
        "description": "Heart failure marker"
    },
    "magnesium": {
        "aliases": ["magnesium", "mg", "serum magnesium"],
        "default": {"min": 1.7, "max": 2.4},
        "unit": "mg/dL",
        "description": "Mineral important for muscle and nerve function"
    },
    "zinc": {
        "aliases": ["zinc", "serum zinc"],
        "default": {"min": 70, "max": 120},
        "unit": "mcg/dL",
        "description": "Mineral important for immunity and wound healing"
    },
    "folate": {
        "aliases": ["folate", "folic acid", "serum folate"],
        "default": {"min": 2.7, "max": 17.0},
        "unit": "ng/mL",
        "description": "Vitamin B9 — important for cell growth and pregnancy"
    },
    "prothrombin_time": {
        "aliases": ["prothrombin time", "pt", "pt inr", "inr"],
        "default": {"min": 11, "max": 13.5},
        "unit": "seconds",
        "description": "Measures how long blood takes to clot"
    },
    "aptt": {
        "aliases": ["aptt", "ptt", "activated partial thromboplastin time"],
        "default": {"min": 25, "max": 35},
        "unit": "seconds",
        "description": "Measures clotting ability of blood"
    },
    "fibrinogen": {
        "aliases": ["fibrinogen", "serum fibrinogen"],
        "default": {"min": 200, "max": 400},
        "unit": "mg/dL",
        "description": "Protein involved in blood clotting"
    },
    "d_dimer": {
        "aliases": ["d dimer", "d-dimer"],
        "default": {"min": 0, "max": 0.5},
        "unit": "mg/L",
        "description": "Clot breakdown marker — elevated in blood clots"
    },
    "cortisol": {
        "aliases": ["cortisol", "serum cortisol", "morning cortisol"],
        "default": {"min": 6.2, "max": 19.4},
        "unit": "mcg/dL",
        "description": "Stress hormone produced by adrenal glands"
    },
    "testosterone": {
        "aliases": ["testosterone", "serum testosterone", "total testosterone"],
        "male": {"min": 300, "max": 1000},
        "female": {"min": 15, "max": 70},
        "default": {"min": 15, "max": 1000},
        "unit": "ng/dL",
        "description": "Male sex hormone"
    },
    "estradiol": {
        "aliases": ["estradiol", "e2", "oestradiol"],
        "male": {"min": 10, "max": 40},
        "female": {"min": 20, "max": 350},
        "default": {"min": 10, "max": 350},
        "unit": "pg/mL",
        "description": "Female sex hormone"
    },
    "prolactin": {
        "aliases": ["prolactin", "serum prolactin"],
        "male": {"min": 2, "max": 18},
        "female": {"min": 2, "max": 29},
        "default": {"min": 2, "max": 29},
        "unit": "ng/mL",
        "description": "Hormone that stimulates milk production"
    },
    "lh": {
        "aliases": ["lh", "luteinizing hormone"],
        "male": {"min": 1.5, "max": 9.3},
        "female": {"min": 1.0, "max": 18.0},
        "default": {"min": 1.0, "max": 18.0},
        "unit": "mIU/mL",
        "description": "Hormone that controls reproductive function"
    },
    "fsh": {
        "aliases": ["fsh", "follicle stimulating hormone"],
        "male": {"min": 1.5, "max": 12.4},
        "female": {"min": 1.0, "max": 21.0},
        "default": {"min": 1.0, "max": 21.0},
        "unit": "mIU/mL",
        "description": "Hormone that controls reproductive function"
    },
    "hcg": {
        "aliases": ["hcg", "beta hcg", "human chorionic gonadotropin"],
        "default": {"min": 0, "max": 5},
        "unit": "mIU/mL",
        "description": "Pregnancy hormone"
    },
    "cea": {
        "aliases": ["cea", "carcinoembryonic antigen"],
        "default": {"min": 0, "max": 3.0},
        "unit": "ng/mL",
        "description": "Cancer marker — elevated in some cancers"
    },
    "afp": {
        "aliases": ["afp", "alpha fetoprotein"],
        "default": {"min": 0, "max": 8.5},
        "unit": "ng/mL",
        "description": "Cancer marker for liver and testicular cancer"
    },
    "ca125": {
        "aliases": ["ca125", "ca 125", "cancer antigen 125"],
        "default": {"min": 0, "max": 35},
        "unit": "U/mL",
        "description": "Ovarian cancer marker"
    },
    "ca199": {
        "aliases": ["ca199", "ca 19-9", "cancer antigen 19-9"],
        "default": {"min": 0, "max": 37},
        "unit": "U/mL",
        "description": "Pancreatic cancer marker"
    },
    "urine_protein": {
        "aliases": ["urine protein", "urinary protein", "protein urine"],
        "default": {"min": 0, "max": 150},
        "unit": "mg/24hr",
        "description": "Protein in urine — elevated indicates kidney damage"
    },
    "microalbumin": {
        "aliases": ["microalbumin", "urine microalbumin", "albumin creatinine ratio"],
        "default": {"min": 0, "max": 30},
        "unit": "mg/g",
        "description": "Early marker of kidney damage in diabetics"
    },
    "urine_glucose": {
        "aliases": ["urine glucose", "urinary glucose", "glucose urine"],
        "default": {"min": 0, "max": 0},
        "unit": "mg/dL",
        "description": "Glucose in urine — should be absent normally"
    },
    "hemoglobin_a1c": {
        "aliases": ["hemoglobin a1c", "hgb a1c"],
        "default": {"min": 4.0, "max": 5.7},
        "unit": "%",
        "description": "3-month average blood sugar level"
    },
    "bicarbonate": {
        "aliases": ["bicarbonate", "hco3", "co2"],
        "default": {"min": 22, "max": 29},
        "unit": "mEq/L",
        "description": "Electrolyte that maintains blood pH"
    },
    "anion_gap": {
        "aliases": ["anion gap"],
        "default": {"min": 8, "max": 16},
        "unit": "mEq/L",
        "description": "Measure of acid-base balance in blood"
    },
    "reticulocyte": {
        "aliases": ["reticulocyte", "reticulocyte count", "retic count"],
        "default": {"min": 0.5, "max": 2.5},
        "unit": "%",
        "description": "Immature red blood cells — shows bone marrow activity"
    },
    "absolute_neutrophil": {
        "aliases": ["anc", "absolute neutrophil count"],
        "default": {"min": 1800, "max": 7700},
        "unit": "cells/mcL",
        "description": "Absolute count of infection-fighting white blood cells"
    },
    "stool_occult_blood": {
        "aliases": ["occult blood", "stool occult blood", "fecal occult blood"],
        "default": {"min": 0, "max": 0},
        "unit": "",
        "description": "Hidden blood in stool — should be absent"
    },
}

UNIT_CONVERSIONS = {
    "mmol/l_to_mg/dl_glucose": 18.0,
    "mmol/l_to_mg/dl_cholesterol": 38.67,
    "umol/l_to_mg/dl_creatinine": 0.0113,
    "g/l_to_g/dl": 0.1,
    "mg/l_to_mg/dl": 0.1,
}

def normalize_unit(value: float, raw_unit: str, param_key: str) -> float:
    raw_unit = raw_unit.lower().strip()
    glucose_params = ["fasting_glucose", "postprandial_glucose", "random_glucose"]
    cholesterol_params = ["total_cholesterol", "ldl", "hdl", "triglycerides", "vldl"]
    if raw_unit in ["mmol/l"]:
        if param_key in glucose_params:
            return round(value * 18.0, 2)
        if param_key in cholesterol_params:
            return round(value * 38.67, 2)
    if raw_unit in ["umol/l", "µmol/l"] and param_key == "creatinine":
        return round(value * 0.0113, 2)
    if raw_unit in ["g/l"] and param_key in ["total_protein", "albumin", "globulin"]:
        return round(value * 0.1, 2)
    if raw_unit in ["mg/l"] and param_key == "crp":
        return round(value * 0.1, 2)
    if raw_unit in ["gm%", "gm/dl", "gms/dl", "gm/100ml"]:
        return value
    if raw_unit in ["10^3/ul", "10^3/µl", "thou/ul", "k/ul", "x10^3/ul"]:
        if param_key == "wbc":
            return value * 1000
        if param_key == "platelets":
            return value * 1000
    if raw_unit in ["10^6/ul", "10^6/µl", "mil/ul", "m/ul"]:
        return value
    return value


def extract_value(text: str, param_key: str = "") -> tuple:
    tl = text.lower().strip()
    lakh_m = re.search(r'(\d+\.?\d*)\s*lakh', tl)
    if lakh_m:
        return round(float(lakh_m.group(1)) * 100_000, 2), "cells/mcL"
    k_m = re.search(r'(\d+\.?\d*)\s*k\b(?!\s*/)', tl)
    if k_m:
        return round(float(k_m.group(1)) * 1_000, 2), "cells/mcL"
    unit_m = re.search(
        r'(\d+\.?\d*)\s*(mmol/l|µmol/l|umol/l|g/dl|mg/dl|g/l|mg/l'
        r'|u/l|iu/l|meq/l|ng/ml|pg/ml|mcg/dl|ng/dl|miu/l|miu/ml'
        r'|ml/min|cells/mcl|million/mcl|mm/hr|seconds|%)',
        tl, re.IGNORECASE
    )
    if unit_m:
        val = float(unit_m.group(1))
        unit = unit_m.group(2)
        return normalize_unit(val, unit, param_key), unit
    large_m = re.search(r'\b(\d{4,7})\b', tl)
    if large_m:
        return float(large_m.group(1)), ""
    num_m = re.search(r'(\d+\.?\d*)', tl)
    if num_m:
        return float(num_m.group(1)), ""
    return None, ""


def get_severity(value, ref_range):
    min_val = ref_range["min"]
    max_val = ref_range["max"]
    if max_val == 999 or max_val == 99999:
        if value < min_val:
            deviation = ((min_val - value) / min_val) * 100
        else:
            return "NORMAL", "Within normal range"
    elif value < min_val:
        deviation = ((min_val - value) / min_val) * 100
    elif value > max_val:
        deviation = ((value - max_val) / max_val) * 100
    else:
        return "NORMAL", "Within normal range"
    if deviation > 50:
        return "DANGER", f"{'Critically low' if value < min_val else 'Critically high'} — immediate attention needed"
    elif deviation > 20:
        return "MONITOR", f"{'Significantly low' if value < min_val else 'Significantly high'} — needs monitoring"
    else:
        return "MILD", f"{'Slightly low' if value < min_val else 'Slightly high'} — monitor and manage"


def analyse_blood_report_engine(report_text: str, gender: str = "default") -> dict:
    results = []
    abnormal = []
    seen_params = set()
    raw_lines = report_text.split("\n")
    lines = []
    for raw in raw_lines:
        sub = re.split(r'\s{2,}(?=[A-Z])', raw)
        lines.extend(sub)
    for line in lines:
        line = line.strip()
        line_lower = line.lower()
        if not line_lower:
            continue
        for param_key, param_data in REFERENCE_RANGES.items():
            if param_key in seen_params:
                continue
            matched = False
            for alias in param_data["aliases"]:
                if re.search(rf'\b{re.escape(alias)}\b', line_lower):
                    matched = True
                    break
            if not matched:
                continue
            value, raw_unit = extract_value(line, param_key)
            if value is None:
                continue
            ref_range = param_data.get(gender) if gender in param_data and gender != "default" else param_data["default"]
            severity, message = get_severity(value, ref_range)
            result = {
                "name": param_key.replace("_", " ").title(),
                "value": value,
                "unit": param_data["unit"],
                "raw_unit": raw_unit,
                "min": ref_range["min"],
                "max": ref_range["max"],
                "status": severity,
                "message": message,
                "description": param_data["description"]
            }
            results.append(result)
            seen_params.add(param_key)
            if severity != "NORMAL":
                abnormal.append(result)
            break
    for param_key, param_data in REFERENCE_RANGES.items():
        if param_key in seen_params:
            continue
        text_lower = report_text.lower()
        matched_alias = None
        for alias in param_data["aliases"]:
            if re.search(rf'\b{re.escape(alias)}\b', text_lower):
                matched_alias = alias
                break
        if not matched_alias:
            continue
        # Extract value from a window around the alias match
        m = re.search(rf'\b{re.escape(matched_alias)}\b(.{{0,40}})', text_lower)
        if not m:
            continue
        window = m.group(0)
        value, raw_unit = extract_value(window, param_key)
        if value is None:
            continue
        ref_range = param_data.get(gender) if gender in param_data and gender != "default" else param_data["default"]
        severity, message = get_severity(value, ref_range)
        result = {
            "name": param_key.replace("_", " ").title(),
            "value": value,
            "unit": param_data["unit"],
            "raw_unit": raw_unit,
            "min": ref_range["min"],
            "max": ref_range["max"],
            "status": severity,
            "message": message,
            "description": param_data["description"]
        }
        results.append(result)
        seen_params.add(param_key)
        if severity != "NORMAL":
            abnormal.append(result)
    return {
        "all_values": results,
        "abnormal_values": abnormal,
        "total_checked": len(results),
        "total_abnormal": len(abnormal)
    }
def format_engine_results_for_llm(engine_results: dict) -> str:
    if not engine_results["all_values"]:
        return "No standard blood values detected in the report."
    text = "VALIDATED BLOOD VALUES (rule-based analysis):\n\n"
    for item in engine_results["all_values"]:
        status_emoji = "✅" if item["status"] == "NORMAL" else ("🚨" if item["status"] == "DANGER" else ("⚠️" if item["status"] == "MONITOR" else "🟡"))
        text += f"{status_emoji} {item['name']}: {item['value']} {item['unit']}\n"
        text += f"   Normal range: {item['min']} - {item['max']} {item['unit']}\n"
        text += f"   Status: {item['status']} — {item['message']}\n\n"
    if engine_results["abnormal_values"]:
        text += f"\nABNORMAL VALUES DETECTED: {engine_results['total_abnormal']} out of {engine_results['total_checked']} checked\n"
    else:
        text += f"\nAll {engine_results['total_checked']} detected values are within normal range.\n"
    return text
RADIOLOGY_RED_KEYWORDS = {
    "DANGER": [
        "hemorrhage", "intracranial hemorrhage", "intracerebral hemorrhage",
        "intraventricular hemorrhage", "subarachnoid hemorrhage", "sah",
        "subdural hematoma", "acute subdural hematoma", "sdh",
        "epidural hematoma", "extradural hematoma", "edh",
        "hematoma", "cerebral hematoma", "traumatic hematoma",
        "brain hemorrhage", "hemorrhagic transformation", "hemorrhagic infarction",
        "hemorrhagic contusion", "cerebral contusion", "cortical contusion",
        "diffuse axonal injury", "dai", "shear injury",
        "midline shift", "subfalcine herniation", "transtentorial herniation",
        "uncal herniation", "cerebellar tonsillar herniation", "brain herniation",
        "downward herniation", "upward herniation", "central herniation",
        "cerebral edema", "diffuse cerebral edema", "cytotoxic edema",
        "vasogenic edema", "malignant cerebral edema",
        "acute infarction", "acute ischemic stroke", "acute stroke",
        "large vessel occlusion", "lvo", "basilar artery occlusion",
        "internal carotid occlusion", "mca occlusion", "middle cerebral artery occlusion",
        "diffusion restriction", "restricted diffusion", "acute diffusion abnormality",
        "malignant mca infarction", "malignant infarction",
        "cerebral venous thrombosis", "cvt", "sagittal sinus thrombosis",
        "transverse sinus thrombosis", "cavernous sinus thrombosis",
        "cortical vein thrombosis", "venous infarction",
        "hydrocephalus", "obstructive hydrocephalus", "acute hydrocephalus",
        "non-communicating hydrocephalus", "tension hydrocephalus",
        "intracranial hypertension", "raised icp", "elevated icp",
        "mass effect", "significant mass effect", "severe mass effect",
        "cerebral abscess", "brain abscess", "intracranial abscess",
        "subdural empyema", "epidural abscess intracranial",
        "encephalitis", "herpes encephalitis", "bacterial encephalitis",
        "meningitis", "bacterial meningitis", "meningeal enhancement",
        "ventriculitis", "cerebritis",
        "ruptured aneurysm", "aneurysmal rupture", "ruptured cerebral aneurysm",
        "giant aneurysm", "mycotic aneurysm",
        "arteriovenous malformation", "avm", "ruptured avm",
        "cavernous malformation", "cavernous hemangioma bleeding",
        "glioblastoma", "gbm", "glioblastoma multiforme",
        "brain metastasis", "cerebral metastasis", "multiple brain metastases",
        "leptomeningeal metastasis", "leptomeningeal carcinomatosis",
        "leptomeningeal disease", "carcinomatous meningitis",
        "primary cns lymphoma", "pituitary apoplexy", "pituitary hemorrhage",
        "tension pneumothorax", "pneumothorax", "large pneumothorax",
        "bilateral pneumothorax", "open pneumothorax",
        "massive hemothorax", "hemothorax", "massive hemopneumothorax",
        "aortic dissection", "type a dissection", "type b dissection",
        "aortic rupture", "aortic transection", "traumatic aortic injury",
        "ruptured thoracic aortic aneurysm", "ruptured aorta",
        "pulmonary embolism", "pe", "saddle embolism", "saddle pulmonary embolism",
        "bilateral pulmonary embolism", "massive pulmonary embolism",
        "central pulmonary embolism", "pulmonary infarction",
        "right heart strain", "right ventricular strain",
        "cardiac tamponade", "pericardial tamponade",
        "acute myocardial infarction", "ami", "stemi",
        "myocardial infarction", "transmural infarction",
        "ventricular rupture", "free wall rupture",
        "papillary muscle rupture", "chordae tendineae rupture",
        "acute aortic syndrome", "mediastinitis", "descending necrotizing mediastinitis",
        "esophageal perforation", "boerhaave syndrome", "esophageal rupture",
        "tracheal rupture", "bronchial rupture", "tracheobronchial injury",
        "tracheal deviation", "mediastinal shift",
        "acute respiratory distress syndrome", "ards",
        "diffuse alveolar damage", "dad",
        "pulmonary hemorrhage", "diffuse pulmonary hemorrhage", "alveolar hemorrhage",
        "lung abscess", "necrotizing pneumonia", "cavitation",
        "tension hydrothorax", "massive pleural effusion",
        "hemopericardium", "pneumopericardium",
        "diaphragmatic rupture", "diaphragmatic tear",
        "flail chest", "multiple rib fractures",
        "sternal fracture", "cardiac contusion", "myocardial contusion",
        "bowel perforation", "gastric perforation", "colonic perforation",
        "free air", "pneumoperitoneum", "free intraperitoneal air",
        "mesenteric ischemia", "bowel ischemia", "bowel infarction",
        "bowel necrosis", "ischemic colitis severe",
        "ruptured aortic aneurysm", "ruptured abdominal aortic aneurysm", "ruptured aaa",
        "splenic rupture", "ruptured spleen", "splenic laceration grade",
        "liver laceration", "hepatic rupture", "hepatic laceration",
        "renal laceration", "renal rupture", "kidney laceration",
        "perforated appendicitis", "perforated viscus",
        "abdominal abscess", "intra-abdominal abscess",
        "retroperitoneal hemorrhage", "retroperitoneal hematoma",
        "superior mesenteric artery occlusion", "sma occlusion", "sma thrombosis",
        "portal vein thrombosis", "pvt", "acute portal vein thrombosis",
        "hepatic vein thrombosis", "budd-chiari syndrome",
        "mesenteric vein thrombosis", "volvulus", "sigmoid volvulus", "cecal volvulus", "gastric volvulus",
        "intussusception", "adult intussusception",
        "strangulated hernia", "incarcerated hernia",
        "hemorrhagic pancreatitis", "necrotizing pancreatitis",
        "pancreatic necrosis", "infected pancreatic necrosis",
        "ruptured ectopic pregnancy", "hemoperitoneum",
        "splenic infarction", "hepatic infarction", "renal infarction",
        "adrenal hemorrhage", "deep vein thrombosis", "dvt", "proximal dvt", "iliofemoral thrombosis",
        "arterial occlusion", "acute arterial occlusion", "limb ischemia",
        "acute limb ischemia", "carotid dissection", "internal carotid dissection",
        "vertebral artery dissection", "vertebrobasilar dissection",
        "aortic aneurysm", "thoracic aortic aneurysm", "abdominal aortic aneurysm",
        "aneurysm rupture", "peripheral arterial occlusion", "femoral artery occlusion",
        "popliteal artery occlusion", "spinal cord compression", "acute spinal cord compression",
        "cervical cord compression", "thoracic cord compression",
        "lumbar cord compression", "cauda equina syndrome",
        "spinal cord infarction", "spinal cord ischemia",
        "epidural hematoma spine", "spinal epidural hematoma",
        "spinal epidural abscess", "vertebral osteomyelitis acute",
        "unstable fracture", "burst fracture", "chance fracture",
        "hangman fracture", "jefferson fracture",
        "atlantoaxial instability", "atlantoaxial subluxation",
        "odontoid fracture", "dens fracture",
        "cervical instability", "cervical dislocation",
        "traumatic disc herniation", "acute disc extrusion",
        "spinal cord signal change acute",
        "complete cord transection", "epiglottitis", "retropharyngeal abscess", "parapharyngeal abscess",
        "ludwig angina", "deep neck infection",
        "internal carotid artery occlusion",
        "jugular vein thrombosis", "internal jugular thrombosis",
        "orbital cellulitis", "orbital abscess",
        "cavernous sinus thrombosis", "malignant", "malignancy", "carcinoma", "cancer",
        "metastasis", "metastases", "metastatic disease",
        "sarcoma", "osteosarcoma", "chondrosarcoma", "ewing sarcoma",
        "lymphoma", "high grade lymphoma", "burkitt lymphoma",
        "leukemia infiltration", "tumor", "tumour", "neoplasm", "neoplasia", "mass lesion",
        "adenocarcinoma", "squamous cell carcinoma",
        "hepatocellular carcinoma", "hcc", "renal cell carcinoma", "rcc",
        "pancreatic carcinoma", "pancreatic ductal adenocarcinoma",
        "cholangiocarcinoma", "bile duct carcinoma",
        "colorectal carcinoma", "rectal carcinoma",
        "gastric carcinoma", "stomach cancer",
        "ovarian carcinoma", "ovarian cancer",
        "cervical carcinoma", "endometrial carcinoma",
        "bladder carcinoma", "transitional cell carcinoma",
        "prostate carcinoma", "prostate cancer",
        "thyroid carcinoma", "papillary thyroid carcinoma",
        "lung carcinoma", "nsclc", "small cell lung cancer", "sclc",
        "pleural mesothelioma", "mesothelioma",
        "pathological fracture", "cord compression from tumor",
        "malignant pleural effusion", "malignant ascites",
        "tumor thrombus", "vascular invasion",
        "perineural invasion", "lymphovascular invasion",
        "non-accidental trauma", "child abuse pattern",
        "intussusception pediatric", "necrotizing enterocolitis", "nec",
        "hirschsprung disease complication", "wilms tumor", "nephroblastoma",
        "neuroblastoma",
    ],
    "MONITOR": [
        "chronic subdural", "chronic subdural hematoma",
        "subacute subdural", "bilateral subdural",
        "old hemorrhage", "old infarct", "chronic infarction",
        "lacunar infarct", "lacunar infarction", "lacunes",
        "white matter changes", "white matter hyperintensities",
        "leukoaraiosis", "periventricular white matter changes",
        "periventricular hyperintensities", "deep white matter changes",
        "small vessel disease", "cerebrovascular disease",
        "cerebral microbleed", "microbleed", "microbleeds",
        "hemosiderin deposition", "enlarged ventricles", "ventriculomegaly", "mild hydrocephalus",
        "communicating hydrocephalus", "normal pressure hydrocephalus",
        "cerebral atrophy", "cortical atrophy", "global atrophy",
        "frontotemporal atrophy", "hippocampal atrophy",
        "cerebral calcification", "basal ganglia calcification",
        "intracranial calcification", "demyelination", "demyelinating lesion", "demyelinating disease",
        "multiple sclerosis", "ms plaque", "ms lesion",
        "periventricular plaques", "juxtacortical lesion",
        "pituitary adenoma", "pituitary macroadenoma", "pituitary microadenoma",
        "meningioma", "convexity meningioma", "falcine meningioma",
        "acoustic neuroma", "vestibular schwannoma",
        "craniopharyngioma", "ependymoma", "astrocytoma", "low grade glioma", "high grade glioma",
        "oligodendroglioma", "pilocytic astrocytoma",
        "arachnoid cyst", "dermoid cyst", "epidermoid cyst",
        "pineal cyst large", "colloid cyst",
        "chiari malformation", "arnold chiari", "tonsillar ectopia",
        "syringomyelia", "syrinx", "dural arteriovenous fistula", "davf",
        "carotid stenosis intracranial", "intracranial stenosis",
        "basilar stenosis", "vertebral stenosis",
        "cerebral aneurysm unruptured", "unruptured aneurysm",
        "cavernous malformation", "cerebral cavernoma",
        "moyamoya disease", "posterior reversible encephalopathy", "pres",
        "reversible cerebral vasoconstriction syndrome",
        "pleural effusion", "bilateral pleural effusion",
        "moderate pleural effusion", "large pleural effusion",
        "loculated pleural effusion", "pleural effusion right", "pleural effusion left",
        "consolidation", "lobar consolidation", "segmental consolidation",
        "right lower lobe consolidation", "left lower lobe consolidation",
        "right upper lobe consolidation", "pneumonia", "community acquired pneumonia",
        "atypical pneumonia", "interstitial pneumonia",
        "organizing pneumonia", "cryptogenic organizing pneumonia", "cop",
        "pulmonary fibrosis", "interstitial fibrosis", "ipf",
        "usual interstitial pneumonia", "uip",
        "non-specific interstitial pneumonia", "nsip",
        "ground glass opacity", "ground glass opacities", "ggo",
        "bilateral ground glass", "multifocal ground glass",
        "crazy paving pattern", "tree in bud", "tree-in-bud",
        "bronchiectasis", "cylindrical bronchiectasis",
        "cystic bronchiectasis", "varicose bronchiectasis",
        "emphysema", "bullous emphysema", "centrilobular emphysema",
        "paraseptal emphysema", "panlobular emphysema",
        "pulmonary nodule", "lung nodule", "solitary pulmonary nodule",
        "multiple pulmonary nodules", "miliary nodules",
        "ground glass nodule", "part solid nodule",
        "pulmonary mass", "lung mass", "mediastinal mass", "anterior mediastinal mass",
        "posterior mediastinal mass", "middle mediastinal mass",
        "mediastinal lymphadenopathy", "mediastinal adenopathy",
        "hilar lymphadenopathy", "hilar enlargement", "bilateral hilar enlargement",
        "cardiomegaly", "enlarged heart", "cardiac enlargement",
        "pericardial effusion", "moderate pericardial effusion",
        "pericardial thickening", "constrictive pericarditis",
        "aortic ectasia", "aortic dilatation", "aortic enlargement",
        "ascending aorta dilatation", "descending aorta dilatation",
        "atelectasis", "subsegmental atelectasis", "lobar atelectasis",
        "compressive atelectasis", "passive atelectasis",
        "pleural thickening", "bilateral pleural thickening", "pleural plaques",
        "pleural calcification", "tracheal stenosis", "subglottic stenosis", "airway narrowing",
        "pulmonary hypertension", "enlarged pulmonary artery",
        "mosaic attenuation", "air trapping",
        "opacity", "haziness", "infiltrate", "air space opacity",
        "perihilar opacity", "basal opacity",
        "bronchial wall thickening", "peribronchial thickening",
        "interlobular septal thickening", "septal thickening",
        "honeycombing", "cystic lung disease",
        "pulmonary cyst", "pneumatocele", "thymus enlargement", "thymoma",
        "lymphoma chest", "sarcoidosis", "rib destruction", "rib lesion",
        "chest wall mass", "left ventricular hypertrophy", "lvh",
        "right ventricular hypertrophy", "rvh",
        "ventricular dilatation", "left ventricular dilatation",
        "right ventricular dilatation", "wall motion abnormality", "hypokinesia", "akinesia", "dyskinesia",
        "myocardial scar", "myocardial fibrosis",
        "delayed enhancement", "late gadolinium enhancement",
        "cardiomyopathy", "dilated cardiomyopathy", "hypertrophic cardiomyopathy",
        "restrictive cardiomyopathy", "valvular disease", "mitral valve disease", "aortic valve disease",
        "aortic stenosis", "aortic regurgitation", "tricuspid regurgitation",
        "mitral stenosis", "mitral regurgitation", "mitral valve prolapse",
        "cardiac thrombus", "intracardiac thrombus", "left atrial thrombus",
        "atrial enlargement", "left atrial enlargement", "right atrial enlargement",
        "patent foramen ovale", "pfo", "atrial septal defect", "asd",
        "ventricular septal defect", "vsd",
        "coronary artery calcification", "coronary calcification",
        "coronary stenosis", "pericarditis",
        "hepatomegaly", "enlarged liver",
        "fatty liver", "hepatic steatosis", "moderate steatosis",
        "steatohepatitis", "nash", "liver cirrhosis", "cirrhosis", "hepatic fibrosis",
        "liver lesion", "hepatic lesion", "hepatic mass",
        "liver cyst", "hepatic cyst", "simple hepatic cyst",
        "hemangioma", "hepatic hemangioma",
        "focal nodular hyperplasia", "fnh",
        "hepatic adenoma", "biliary dilatation", "dilated bile duct", "intrahepatic biliary dilatation",
        "choledocholithiasis", "common bile duct stone",
        "gallstones", "cholelithiasis", "multiple gallstones",
        "cholecystitis", "acute cholecystitis", "chronic cholecystitis",
        "gallbladder wall thickening", "gallbladder distension",
        "mirizzi syndrome", "portal hypertension", "portosystemic collaterals",
        "varices", "esophageal varices", "gastric varices",
        "splenomegaly", "enlarged spleen", "massive splenomegaly",
        "splenic cyst", "splenic lesion",
        "pancreatitis", "acute pancreatitis", "chronic pancreatitis",
        "pancreatic edema", "peripancreatic fluid",
        "pancreatic mass", "pancreatic lesion", "pancreatic head mass",
        "pancreatic cyst", "pancreatic pseudocyst",
        "ipmn", "intraductal papillary mucinous neoplasm",
        "mucinous cystic neoplasm", "mcn pancreas",
        "pancreatic ductal dilatation", "dilated pancreatic duct",
        "double duct sign", "pancreatic atrophy",
        "renal mass", "renal lesion", "kidney mass",
        "renal cyst complex", "bosniak cyst", "bosniak iii", "bosniak iv",
        "hydronephrosis", "bilateral hydronephrosis", "urinary obstruction",
        "ureteric obstruction", "ureteropelvic junction obstruction", "upj obstruction",
        "renal calculus", "renal stone", "kidney stone", "urolithiasis",
        "staghorn calculus", "nephrolithiasis",
        "renal parenchymal thinning", "renal scarring",
        "renal artery stenosis", "bladder mass", "bladder wall thickening", 
        "bladder tumor", "ureteric lesion",
        "adrenal mass", "adrenal adenoma", "adrenal hyperplasia",
        "adrenal lesion", "adrenal nodule", "adrenal incidentaloma",
        "pheochromocytoma", "adrenocortical carcinoma",
        "retroperitoneal mass", "retroperitoneal lymphadenopathy",
        "bowel wall thickening", "colitis", "enteritis", "ileitis",
        "crohn disease", "ulcerative colitis",
        "bowel obstruction", "small bowel obstruction", "large bowel obstruction",
        "transition point", "closed loop obstruction",
        "appendiceal thickening", "acute appendicitis",
        "periappendiceal fat stranding",
        "diverticulitis", "perforated diverticulitis", "diverticular abscess",
        "colorectal polyp", "colonic polyp",
        "colorectal thickening", "rectal mass",
        "mesenteric fat stranding", "mesenteric inflammatory changes",
        "lymph node mesenteric", "mesenteric lymphadenopathy",
        "pneumatosis intestinalis", "pneumatosis coli",
        "ascites", "free fluid abdomen", "moderate ascites",
        "peritoneal thickening", "peritoneal nodularity",
        "peritoneal deposits", "omental deposits", "omental caking",
        "hernia", "inguinal hernia", "hiatal hernia", "umbilical hernia",
        "ventral hernia", "incisional hernia",
        "abdominal wall mass", "lymphadenopathy", "abdominal lymphadenopathy",
        "celiac lymphadenopathy", "para-aortic lymphadenopathy",
        "ovarian cyst", "ovarian mass", "complex ovarian cyst",
        "dermoid cyst ovary", "teratoma ovary",
        "ovarian torsion", "tubo-ovarian abscess",
        "endometriosis", "endometrioma",
        "uterine fibroid", "uterine mass", "uterine leiomyoma",
        "uterine enlargement", "bulky uterus",
        "endometrial thickening", "endometrial polyp",
        "hydrosalpinx", "pyosalpinx",
        "pelvic free fluid", "pelvic mass",
        "cervical lesion", "prostate enlargement", "benign prostatic hyperplasia", "bph",
        "prostate lesion", "prostate nodule", "seminal vesicle lesion",
        "testicular mass", "testicular lesion", "testicular microlithiasis",
        "epididymo-orchitis", "epididymitis",
        "hydrocele", "varicocele",
        "atherosclerosis", "calcified plaque", "vascular calcification",
        "stenosis", "carotid stenosis", "significant carotid stenosis",
        "peripheral arterial disease", "pad",
        "pseudoaneurysm", "iliac aneurysm", "femoral aneurysm",
        "popliteal aneurysm", "thrombosis", "venous thrombosis",
        "venous insufficiency", "varicose veins",
        "inferior vena cava thrombosis", "ivc thrombosis",
        "renal vein thrombosis", "splenic vein thrombosis",
        "disc herniation", "disc protrusion", "disc extrusion",
        "disc sequestration", "extruded disc",
        "cervical disc herniation", "lumbar disc herniation",
        "thoracic disc herniation", "nerve root compression", "nerve root impingement",
        "foraminal stenosis", "neural foraminal narrowing",
        "lateral recess stenosis", "thoracic spinal stenosis",
        "spinal stenosis", "lumbar spinal stenosis", "cervical spinal stenosis",
        "spondylolisthesis", "anterolisthesis", "retrolisthesis",
        "degenerative spondylolisthesis",
        "vertebral fracture", "compression fracture", "wedge fracture",
        "bone marrow edema", "bone marrow signal change", "bone marrow infiltration",
        "osteomyelitis", "discitis", "spondylodiscitis", "vertebral osteomyelitis",
        "sacroiliitis", "bilateral sacroiliitis",
        "facet joint arthropathy", "facet joint effusion",
        "ligamentum flavum hypertrophy", "ossification of ligamentum flavum",
        "ossification of posterior longitudinal ligament", "opll",
        "joint effusion", "synovial thickening", "synovitis",
        "meniscal tear", "medial meniscal tear", "lateral meniscal tear",
        "acl tear", "anterior cruciate ligament tear",
        "pcl tear", "posterior cruciate ligament tear",
        "mcl tear", "lcl tear", "rotator cuff tear", "full thickness rotator cuff tear",
        "partial rotator cuff tear", "rotator cuff tendinopathy",
        "supraspinatus tear", "infraspinatus tear",
        "labral tear", "hip labral tear", "shoulder labral tear",
        "bankart lesion", "hill-sachs lesion",
        "stress fracture", "insufficiency fracture",
        "avascular necrosis", "osteonecrosis",
        "bone lesion", "lytic lesion", "sclerotic lesion",
        "mixed lytic sclerotic", "aggressive bone lesion",
        "periosteal reaction", "periosteal elevation",
        "cortical destruction", "cortical break",
        "soft tissue mass", "soft tissue lesion",
        "joint space narrowing", "cartilage loss",
        "subchondral cyst", "subchondral sclerosis",
        "chondromalacia", "osteitis", "inflammatory arthritis",
        "ankylosing spondylitis", "thyroid nodule", "thyroid mass", "thyroid lesion",
        "multinodular goiter", "thyroid enlargement", "goiter",
        "cervical lymphadenopathy", "neck lymphadenopathy",
        "level ii lymphadenopathy", "level iii lymphadenopathy",
        "parotid mass", "parotid lesion", "necrotic lymph node",
        "salivary gland mass", "submandibular mass",
        "neck mass", "soft tissue neck mass",
        "lymph node enlargement", "enlarged lymph node",
        "lesion", "mass", "enlarged", "thickening", "fibrosis",
        "effusion", "cyst", "polyp", "displacement",
        "prominent", "distension", "restricted diffusion",
        "calcification", "suspicious calcification",
        "fat stranding", "surrounding fat stranding",
        "contrast enhancement", "ring enhancement", "peripheral enhancement",
        "heterogeneous enhancement", "avid enhancement",
        "signal abnormality", "signal change", "marrow replacement",
    ],
    "MILD": [
        "mild", "minimal", "slight", "early", "borderline", "trace",
        "subtle", "small", "minor", "insignificant",
        "degenerative", "degenerative changes",
        "age-related", "age related changes", "age related",
        "incidental", "incidental finding", "incidental note",
        "chronic", "chronic changes",
        "stable", "stable appearance", "unchanged",
        "post-operative", "post-surgical", "post-traumatic",
        "spondylosis", "cervical spondylosis", "lumbar spondylosis",
        "thoracic spondylosis", "multilevel spondylosis",
        "osteophyte", "osteophytes", "marginal osteophytes",
        "anterior osteophytes", "posterior osteophytes",
        "bridging osteophytes", "disc desiccation", "disc degeneration",
        "disc space narrowing", "disc height loss",
        "multilevel disc disease", "facet hypertrophy", "facet degeneration",
        "ligamentum flavum thickening", "schmorl node", "schmorl nodes",
        "disc bulge", "mild disc bulge", "broad disc bulge",
        "annular bulge", "annular tear", "chondrocalcinosis",
        "scoliosis", "mild scoliosis", "levoscoliosis", "dextroscoliosis",
        "kyphosis", "mild kyphosis", "thoracic kyphosis",
        "lordosis loss", "loss of lordosis", "straightening",
        "transitional vertebra", "sacralization", "lumbarization",
        "mild compression", "mild wedging",
        "mild osteoarthritis", "early osteoarthritis",
        "mild joint space narrowing", "mild cartilage thinning",
        "mild synovitis", "mild joint effusion",
        "bursitis", "subacromial bursitis", "trochanteric bursitis",
        "prepatellar bursitis", "pes anserine bursitis",
        "tendinopathy", "tendinosis", "tendon thickening",
        "mild tendinopathy", "patellar tendinopathy",
        "achilles tendinopathy", "plantar fasciitis",
        "bone spur", "heel spur", "calcaneal spur",
        "mild effusion", "trace joint effusion",
        "prominent sulci", "cortical atrophy mild",
        "mild cerebral atrophy", "pineal cyst small", "pineal cyst",
        "choroid plexus cyst", "small arachnoid cyst",
        "empty sella", "partial empty sella",
        "developmental venous anomaly", "dva",
        "enlarged perivascular spaces", "virchow-robin spaces",
        "mild white matter changes", "early white matter changes",
        "mild small vessel disease", "calcification pineal gland", "pineal calcification",
        "mild ventriculomegaly", "slightly prominent ventricles",
        "old lacunar infarct", "remote lacunar infarct",
        "mild cardiomegaly", "borderline cardiomegaly",
        "mild pleural thickening", "small nodule", "tiny nodule", "subcentimeter nodule",
        "trace pleural effusion", "trace left pleural effusion",
        "mild atelectasis", "bibasal atelectasis", "dependent atelectasis",
        "passive atelectasis", "early emphysema", "mild emphysema",
        "mild bronchiectasis", "mild bronchial wall thickening",
        "calcified granuloma", "old granuloma", "healed granuloma",
        "granulomatous calcification", "mild pulmonary vascular prominence",
        "mild aortic ectasia", "prominent aortic knuckle",
        "mild cardiomegaly", "incidental pulmonary nodule",
        "old rib fracture", "healed rib fracture",
        "costochondral calcification", "mild hepatomegaly", "borderline hepatomegaly",
        "simple renal cyst", "cortical cyst", "simple cyst kidney",
        "small gallstone", "biliary sludge",
        "mild fatty liver", "grade 1 fatty liver",
        "mild splenomegaly", "borderline splenomegaly",
        "small hernia", "small hiatal hernia",
        "mild bowel distension", "gaseous distension",
        "colonic faecal loading", "faecal loading",
        "mild mesenteric fat stranding", "mild peritoneal fat",
        "small simple ovarian cyst", "small uterine fibroid",
        "mild bladder wall thickening", "mild prostate enlargement",
        "mild atherosclerosis", "early atherosclerosis",
        "mild calcification", "vascular wall calcification",
        "mild aortic ectasia", "mild carotid intimal thickening", "intimal thickening",
        "mild stenosis", "small thyroid nodule", "tiny thyroid nodule",
        "mild thyroid enlargement", "small cervical lymph node",
        "reactive lymph node", "reactive lymphadenopathy",
    ],
    "NORMAL_VARIANTS": [
        "normal study", "normal examination", "normal scan",
        "no acute findings", "no acute abnormality",
        "no acute intracranial abnormality",
        "unremarkable", "within normal limits", "wnl",
        "no significant abnormality", "no significant finding",
        "no abnormality detected", "nad",
        "no evidence of", "no evidence of malignancy",
        "no evidence of fracture", "no evidence of metastasis",
        "no focal lesion", "no focal abnormality",
        "clear lungs", "clear lung fields", "lungs are clear",
        "no pleural effusion", "no effusion",
        "normal bone density", "normal alignment",
        "no fracture", "no dislocation", "no subluxation",
        "patent", "no stenosis detected", "no occlusion",
        "no lymphadenopathy", "no significant lymphadenopathy",
        "normal in size", "normal appearance",
        "no free fluid", "no ascites",
        "normal liver", "normal spleen", "normal kidneys",
        "normal pancreas", "normal adrenals",
        "no mass", "no lesion identified",
        "no suspicious lesion", "intact", "preserved", "maintained",
        "no disc herniation", "no nerve root compression",
        "no cord compression", "normal signal", "normal signal intensity",
        "no enhancement", "no abnormal enhancement", "no restricted diffusion",
        "no vascular occlusion", "no pulmonary embolism", "no pneumothorax",
    ],
}

PRESCRIPTION_RISK_KEYWORDS = {
    "HIGH_RISK_DRUGS": [
        "warfarin", "heparin", "enoxaparin", "fondaparinux",
        "rivaroxaban", "apixaban", "dabigatran", "edoxaban",
        "digoxin", "lithium", "phenytoin", "carbamazepine",
        "valproate", "valproic acid", "phenobarbitone", "phenobarbital",
        "theophylline", "aminophylline",
        "methotrexate", "cyclosporine", "tacrolimus", "sirolimus",
        "azathioprine", "mycophenolate", "cyclophosphamide",
        "mercaptopurine", "fluorouracil", "capecitabine",
        "amiodarone", "flecainide", "sotalol", "quinidine",
        "procainamide", "disopyramide",
        "insulin", "insulin glargine", "insulin aspart", "insulin lispro",
        "insulin detemir", "insulin nph",
        "glibenclamide", "glyburide", "glipizide", "glimepiride",
        "chlorpropamide", "clozapine", "haloperidol",
        "metformin",  "colchicine",  "dapsone", "thalidomide",
    ],
 
    "CONTROLLED_SUBSTANCES": [
        "morphine", "oxycodone", "hydrocodone", "hydromorphone",
        "fentanyl", "buprenorphine", "methadone", "codeine",
        "tramadol", "tapentadol", "pethidine", "meperidine",
        "oxymorphone", "nalbuphine",
        "alprazolam", "diazepam", "lorazepam", "clonazepam",
        "midazolam", "triazolam", "temazepam", "nitrazepam",
        "chlordiazepoxide", "oxazepam", "zolpidem", "zopiclone", "eszopiclone", "zaleplon",
        "methylphenidate", "amphetamine", "dextroamphetamine",
        "lisdexamfetamine", "modafinil", "ketamine", "dronabinol", "nabilone",
        "pregabalin", "gabapentin", "barbiturate", "phenobarbitone", "carisoprodol",
    ],
    "PREGNANCY_CAUTION": [
        "isotretinoin", "acitretin", "thalidomide",
        "methotrexate", "mycophenolate",
        "warfarin", "valproate", "valproic acid",
        "lithium", "carbamazepine", "phenytoin",
        "tetracycline", "doxycycline", "minocycline",
        "fluoroquinolone", "ciprofloxacin", "levofloxacin",
        "ofloxacin", "misoprostol", "mifepristone",
        "ace inhibitor", "enalapril", "lisinopril", "ramipril",
        "losartan", "valsartan", "telmisartan", "olmesartan",
        "atorvastatin", "rosuvastatin", "simvastatin",
        "nsaid", "ibuprofen", "diclofenac", "naproxen",
        "aspirin high dose", "metronidazole first trimester",
        "trimethoprim", "sulfamethoxazole", "chloramphenicol", "spironolactone", "danazol",
    ],
    "NEPHROTOXIC": [
        "gentamicin", "amikacin", "tobramycin", "streptomycin",
        "vancomycin", "colistin", "polymyxin",
        "amphotericin b", "cidofovir", "foscarnet",
        "contrast media", "iodinated contrast",
        "lithium", "cyclosporine", "tacrolimus",
        "nsaid", "ibuprofen", "diclofenac",
        "metformin", "tenofovir",
    ],
    "HEPATOTOXIC": [
        "isoniazid", "rifampicin", "pyrazinamide",
        "methotrexate", "amiodarone",
        "valproate", "carbamazepine",
        "fluconazole", "ketoconazole", "itraconazole",
        "atorvastatin", "simvastatin",
        "paracetamol overdose", "acetaminophen overdose",
        "halothane", "methyl dopa", "diclofenac", "sulfonamide", "nitrofurantoin",
    ],
    "DRUG_INTERACTIONS_HIGH": [
        "ssri", "snri", "maoi", "tramadol", "linezolid",
        "sertraline", "fluoxetine", "paroxetine",
        "venlafaxine", "duloxetine",
        "triptans", "sumatriptan",
        "amiodarone", "sotalol", "haloperidol", "methadone",
        "chlorpromazine", "domperidone", "azithromycin",
        "clarithromycin", "moxifloxacin", "hydroxychloroquine",
        "rifampicin", "rifampin", "ketoconazole", "fluconazole",
        "carbamazepine",
    ],
    "ANTIBIOTIC_RISK": [
        "vancomycin", "colistin", "linezolid",
        "meropenem", "imipenem", "ertapenem",
        "tigecycline", "daptomycin", "ceftriaxone high dose",
        "chloramphenicol", "ciprofloxacin", "levofloxacin",
    ],
}

SKIN_CANCER_KEYWORDS = {
    "ABCDE_HIGH_RISK": [
        "asymmetry", "asymmetric", "irregular shape", "uneven shape",
        "non-circular", "not round",
        "irregular border", "uneven edge", "ragged border",
        "notched border", "scalloped edge", "indistinct border",
        "poorly defined border", "multiple colors", "multicolored", "variegated color",
        "black", "blue-black", "jet black",
        "red and black", "dark brown and black",
        "white area within lesion", "depigmented area", "color variation",
        "larger than 6mm", "growing lesion", "rapidly growing",
        "increasing size", "expanding lesion",
        "changing lesion", "evolving", "new lesion",
        "recently changed", "doubling in size",
    ],
    "HIGH_RISK_FEATURES": [
        "nodular", "nodular melanoma",
        "amelanotic", "amelanotic melanoma",
        "satellite lesion", "satellite nodule",
        "in situ melanoma", "melanoma in situ",
        "superficial spreading melanoma",
        "lentigo maligna", "lentigo maligna melanoma",
        "acral lentiginous", "subungual melanoma",
        "nail matrix melanoma",
        "thick lesion", "raised lesion raised",
        "ulcerated", "ulceration",
        "bleeding", "spontaneous bleeding",
        "oozing", "crusting with bleeding",
        "induration", "indurated border",
        "firm to touch", "hard lesion",
        "pearly border", "rolled edge",
        "central depression", "central ulcer",
        "pearly nodule", "translucent", "waxy",
        "rodent ulcer", "telangiectasia on lesion", "arborizing vessels",
        "keratinous", "hyperkeratotic", "wart-like growth",
        "cutaneous horn", "actinic keratosis severe",
        "erythroplasia", "bowen disease",
        "tender hard nodule", "fixed to skin",
    ],
    "MEDIUM_RISK_FEATURES": [
        "raised", "elevated", "dome-shaped",
        "dark brown", "dark pigmented",
        "crusty", "scaly", "scaling",
        "rough surface", "verrucous",
        "itching", "pruritic", "persistent itch",
        "pain", "painful lesion", "tenderness",
        "discharge", "weeping", "spreading", "expanding",
        "thickened", "thickening of skin",
        "actinic keratosis", "solar keratosis",
        "leukoplakia", "erythroplakia",
        "dysplastic nevus", "atypical mole", "atypical nevus",
        "suspicious mole", "mole changing",
        "sun exposed area", "chronic sun damage",
        "immunosuppressed", "organ transplant patient",
        "radiation exposed area", "burn scar lesion",
        "chronic wound lesion", "marjolin ulcer",
        "multiple lesions", "new pigmented lesion",
        "irregular network", "atypical pigment network",
        "regression structures", "blue-white veil",
        "atypical dots", "atypical globules",
    ],
    "LOW_RISK_FEATURES": [
        "red", "pink", "flesh colored",
        "flat", "smooth surface",
        "round", "oval", "symmetric",
        "well defined border", "clear border", "regular border",
        "uniform color", "single color",
        "soft", "soft to touch", "compressible",
        "stable", "unchanged for years",
        "slow growing", "present since birth", "congenital lesion",
        "sebaceous cyst", "epidermal cyst",
        "lipoma", "fibroma", "dermatofibroma",
        "seborrheic keratosis", "stuck on appearance",
        "solar lentigo", "age spot",
        "cherry angioma", "campbell de morgan", "freckle", "ephelis",
        "nevus spilus", "spitz nevus",
        "hemangioma", "capillary hemangioma", "pyogenic granuloma",
        "molluscum contagiosum", "wart", "verruca",
        "milia", "comedone", "psoriatic plaque",
        "eczema", "eczematous", "insect bite reaction",
    ],
    "URGENT_REFERRAL_SIGNS": [
        "rapidly enlarging", "ulcerated and bleeding",
        "fixed to underlying tissue", "lymph node enlargement near lesion",
        "regional lymphadenopathy", "palpable node", "hard lymph node",
        "satellite metastasis", "in transit metastasis",
        "recurrent lesion", "recurrence after treatment",
        "previously excised melanoma", "breslow thickness",
        "clark level", "positive margins", "incomplete excision",
        "perineural spread skin",
    ],
}

def is_negated(text, keyword):
    import re
    keyword_pattern = rf"{keyword}s?"
    sentences = re.split(r'[.,;]', text.lower())
    for sentence in sentences:
        if re.search(rf"\b{keyword_pattern}\b", sentence):
            patterns = [
                r"no",
                r"no evidence of",
                r"without",
                r"absence of",
                r"negative for",
                r"free of",
                r"rule out",
                r"no signs of",
                r"no definite",
                r"not seen",
                r"is not seen",
                r"absent",
                r"is absent",
                r"unlikely"
            ]
            for p in patterns:
                if re.search(p, sentence):
                    return True
    return False
def analyse_radiology_engine(report_text: str) -> dict:
    text_lower = report_text.lower()
    findings = {"DANGER": [], "MONITOR": [], "MILD": [], "overall_risk": "LOW"}
    for keyword in RADIOLOGY_RED_KEYWORDS["DANGER"]:
        if re.search(rf"\b{keyword}s?\b", text_lower) and not is_negated(text_lower, keyword):
            findings["DANGER"].append(keyword)
    for keyword in RADIOLOGY_RED_KEYWORDS["MONITOR"]:
        if re.search(rf"\b{keyword}s?\b", text_lower) and not is_negated(text_lower, keyword):
            findings["MONITOR"].append(keyword)
    for keyword in RADIOLOGY_RED_KEYWORDS["MILD"]:
        if re.search(rf"\b{keyword}s?\b", text_lower) and not is_negated(text_lower, keyword):
            findings["MILD"].append(keyword)
    if findings["DANGER"]:
        findings["overall_risk"] = "HIGH"
    elif findings["MONITOR"]:
        findings["overall_risk"] = "MEDIUM"
    elif findings["MILD"]:
        findings["overall_risk"] = "LOW"
    else:
        findings["overall_risk"] = "NORMAL"
    return findings

def analyse_prescription_engine(prescription_text: str) -> dict:
    text_lower = prescription_text.lower()
    warnings = {
        "high_risk_drugs": [],
        "controlled_substances": [],
        "pregnancy_caution": [],
        "drug_count": 0,
        "overall_risk": "LOW"
    }
    drug_indicators = ["tab.", "cap.", "syp.", "inj.", "tab ", "cap ", "mg", "ml"]
    count = sum(1 for indicator in drug_indicators if indicator in text_lower)
    warnings["drug_count"] = min(count, 10)
    for drug in PRESCRIPTION_RISK_KEYWORDS["HIGH_RISK_DRUGS"]:
        if drug in text_lower:
            warnings["high_risk_drugs"].append(drug)
    for drug in PRESCRIPTION_RISK_KEYWORDS["CONTROLLED_SUBSTANCES"]:
        if drug in text_lower:
            warnings["controlled_substances"].append(drug)
    for drug in PRESCRIPTION_RISK_KEYWORDS["PREGNANCY_CAUTION"]:
        if drug in text_lower:
            warnings["pregnancy_caution"].append(drug)
    if warnings["high_risk_drugs"] or warnings["controlled_substances"]:
        warnings["overall_risk"] = "HIGH"
    elif warnings["pregnancy_caution"]:
        warnings["overall_risk"] = "MEDIUM"
    else:
        warnings["overall_risk"] = "LOW"
    return warnings


def analyse_skin_engine(skin_input: str) -> dict:
    text_lower = skin_input.lower()
    signals = {
        "high_risk_signals": [],
        "medium_risk_signals": [],
        "low_risk_signals": [],
        "overall_risk": "LOW",
        "abcde_flags": {}
    }
    abcde = {
        "asymmetry": ["asymmetry", "asymmetric", "uneven", "irregular shape"],
        "border": ["irregular border", "uneven edge", "ragged", "notched"],
        "color": ["multiple colors", "multicolored", "black", "dark brown", "red and black"],
        "diameter": ["larger than", "growing", "expanding", "cm", "mm"],
        "evolution": ["changing", "growing", "spreading", "evolving", "new"]
    }
    for criterion, keywords in abcde.items():
        for kw in keywords:
            if kw in text_lower:
                abcde_count = len(signals["abcde_flags"])
                break
    for keyword in SKIN_CANCER_KEYWORDS["HIGH_RISK_FEATURES"]:
        if keyword in text_lower:
            signals["high_risk_signals"].append(keyword)
    for keyword in SKIN_CANCER_KEYWORDS["MEDIUM_RISK_FEATURES"]:
        if keyword in text_lower:
            signals["medium_risk_signals"].append(keyword)
    for keyword in SKIN_CANCER_KEYWORDS["LOW_RISK_FEATURES"]:
        if keyword in text_lower:
            signals["low_risk_signals"].append(keyword)
    abcde_count = len(signals["abcde_flags"])
    if abcde_count >= 3 or len(signals["high_risk_signals"]) >= 2:
        signals["overall_risk"] = "HIGH"
    elif abcde_count >= 1 or len(signals["medium_risk_signals"]) >= 2:
        signals["overall_risk"] = "MEDIUM"
    else:
        signals["overall_risk"] = "LOW"
    return signals
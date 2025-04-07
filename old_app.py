

import streamlit as st
import lightgbm as lgb
import numpy as np
import pandas as pd

# Load the AKD and CKD models
# Load the AKD and CKD models
aki_model = lgb.Booster(model_file='aki.txt')
akd_model = lgb.Booster(model_file='akd.txt')
mortality_model = lgb.Booster(model_file='death.txt')

# Mapping dictionaries for encoding categorical variables
AKI_stage_mapping = {"Stage 0": 0, "Stage 1": 1, "Stage 2": 2, "Stage 3": 3}
Aspirin_mapping = Coronary_heart_disease_mapping = beta_lactam_antibiotics_mapping = \
CCB_mapping = Omeprazole_mapping = Cardiac_glycosides_mapping = {"Yes": 1, "NO": 0}
Enzymes_antithrombotics_mapping = Shock_mapping = MODS_mapping = PDE_inhibitor_mapping = {"Yes": 1, "NO": 0}
dynamic_mapping = {
    "NKD": 0,
    "AKI recovery": 1,
    "subacute AKD": 2,
    "AKD with AKI": 3
}

# Prediction functions
def predict_aki_probability(features):
    aki_prob = aki_model.predict(features)
    return aki_prob[0]

def predict_akd_probability(features):
    akd_prob = akd_model.predict(features)
    return akd_prob[0]

def predict_mortality_probability(features):
    mortality_prob = mortality_model.predict(features)
    return mortality_prob[0]

def main():
    st.title('AKD, AKI and Mortality Probability Prediction in Elderly Hospitalized Patients')

    # Radio button to switch between views
    selected_content = st.radio("", ("Model Introduction", "AKD, AKI and mortality Prediction"))
    
    if selected_content == "Model Introduction":
        st.subheader("Model Introduction")
        st.write("The online application employs the LightGBM model to forecast the probability of acute kidney disease (AKD), acute kidney injury (AKI), and mortality in elderly hospitalized patients using patient metrics.")
        # Disclaimer
        st.subheader("Disclaimer")
        st.write("The predictions generated by this model are based on historical data and statistical patterns, and they may not be entirely accurate or applicable to every individual.")
        st.write("**For Patients:**")
        st.write("- The predictions presented by this platform are intended for informational purposes only and should not be regarded as a substitute for professional medical advice, diagnosis, or treatment.")
        st.write("- Consult with your healthcare provider for personalized medical guidance and decisions concerning your health.")
        st.write("**For Healthcare Professionals:**")
        st.write("- This platform should be considered as a supplementary tool to aid clinical decision-making and should not be the sole determinant of patient care.")
        st.write("- Clinical judgment and expertise should always take precedence in medical practice.")
        st.write("**For Researchers:**")
        st.write("- While this platform can serve as a valuable resource for research purposes, it is crucial to validate its predictions within your specific clinical context and patient population.")
        st.write("- Ensure that your research adheres to all ethical and regulatory standards.")
        st.write("The creators of this online platform and model disclaim any responsibility for decisions or actions taken based on the predictions provided herein. Please use this tool responsibly and always consider individual patient characteristics and clinical context when making medical decisions.")
        st.write("By utilizing this online platform, you agree to the terms and conditions outlined in this disclaimer.")

        # [Omitted rest of disclaimer for brevity]

    elif selected_content == "AKD, AKI and mortality Prediction":
        st.subheader("AKD, AKI and Mortality Prediction in Elderly Hospitalized Patients")
        prediction_type = st.radio("Select Prediction Type", ("AKD Prediction", "AKI Prediction", "mortality Prediction"))

        features = []

        if prediction_type == "AKD Prediction":
            st.subheader("AKD Features")

            AKI_stage = st.selectbox("AKI stage", ["Stage 0", "Stage 1", "Stage 2", "Stage 3"], key="AKI_stage_AKD")
            ALB = st.number_input("Albumin (ALB, g/L)", value=0.0, format="%.2f", key="ALB_AKD")
            LDH = st.number_input("Lactate Dehydrogenase (LDH, U/L)", value=0.0, format="%.2f", key="LDH_AKD")
            Aspirin = st.selectbox("Aspirin", ["NO", "Yes"], key="Aspirin_AKD")
            CHD = st.selectbox("Coronary Heart Disease (CHD)", ["NO", "Yes"], key="CHD_AKD")
            Na = st.number_input("Sodium (Na, mmol/L)", value=0.0, format="%.2f", key="Na_AKD")
            CK = st.number_input("Creatine Kinase (CK, U/L)", value=0.0, format="%.2f", key="CK_AKD")
            Cys = st.number_input("Cystatin C (Cys, mg/L)", value=0.0, format="%.2f", key="Cys_AKD")
            GGT = st.number_input("Gamma-GT (GGT, U/L)", value=0.0, format="%.2f", key="GGT_AKD")
            Scr = st.number_input("Serum Creatinine (Scr, μmol/L)", value=0.0, format="%.2f", key="Scr_AKD")
            beta_lactam_antibiotics = st.selectbox("β-lactam antibiotics", ["Yes", "NO"], key="beta_lactam_antibiotics_AKD")
            CCB = st.selectbox("Calcium Channel Blockers (CCB)", ["NO", "Yes"], key="CCB_AKD")
            Omeprazole = st.selectbox("Omeprazole", ["NO", "Yes"], key="Omeprazole_AKD")
            RBC = st.number_input("Red Blood Cells (RBC, 10¹²/L)", value=0.0, format="%.2f", key="RBC_AKD")
            Cardiac_glycosides = st.selectbox("Cardiac Glycosides", ["NO", "Yes"], key="Cardiac_glycosides_AKD")

            # Encode
            AKI_stage_encoded = AKI_stage_mapping[AKI_stage]
            Aspirin_encoded = Aspirin_mapping[Aspirin]
            CHD_encoded = Coronary_heart_disease_mapping[CHD]
            beta_lactam_encoded = beta_lactam_antibiotics_mapping[beta_lactam_antibiotics]
            CCB_encoded = CCB_mapping[CCB]
            Omeprazole_encoded = Omeprazole_mapping[Omeprazole]
            Cardiac_glycosides_encoded = Cardiac_glycosides_mapping[Cardiac_glycosides]

            # Features
            features.extend([
                AKI_stage_encoded, ALB, LDH, Aspirin_encoded, CHD_encoded, Na, CK, Cys,
                GGT, Scr, beta_lactam_encoded, CCB_encoded, Omeprazole_encoded, RBC, Cardiac_glycosides_encoded
            ])

            if st.button("Predict AKD Probability"):
                akd_prob = predict_akd_probability(np.array(features).reshape(1, -1))
                st.write(f"AKD Probability: {akd_prob:.2f}")

        elif prediction_type == "AKI Prediction":
            st.subheader("AKI Features")

            Scr = st.number_input("Scr (μmol/L)", value=0.0, format="%.2f", key="Scr_AKI")
            Cardiac_glycosides = st.selectbox("Cardiac glycosides", ["NO", "Yes"], key="Cardiac_glycosides_AKI")
            Cys = st.number_input("Cystatin C (mg/L)", value=0.0, format="%.2f", key="Cys_AKI")
            Glucose = st.number_input("Glucose (mmol/L)", value=0.0, format="%.2f", key="Glucose_AKI")
            BUN = st.number_input("Blood Urea Nitrogen (mmol/L)", value=0.0, format="%.2f", key="BUN_AKI")
            Neut = st.number_input("Neutrophils (10⁹/L)", value=0.0, format="%.2f", key="Neut_AKI")
            Lactic_acid = st.number_input("Lactic acid (mmol/L)", value=0.0, format="%.2f", key="Lactic_acid_AKI")
            UA = st.number_input("Uric Acid (μmol/L)", value=0.0, format="%.2f", key="UA_AKI")
            Aspirin = st.selectbox("Aspirin", ["NO", "Yes"], key="Aspirin_AKI")
            Na = st.number_input("Sodium (Na, mmol/L)", value=0.0, format="%.2f", key="Na_AKI")
            eGFR = st.number_input("eGFR (ml/min/1.73m²)", value=0.0, format="%.2f", key="eGFR_AKI")
            Mg = st.number_input("Magnesium (Mg, mmol/L)", value=0.0, format="%.2f", key="Mg_AKI")
            INR_PT = st.number_input("INR/PT", value=0.0, format="%.2f", key="INR_PT_AKI")
            FIB = st.number_input("Fibrinogen (g/L)", value=0.0, format="%.2f", key="FIB_AKI")
            TBIL = st.number_input("Total Bilirubin (TBIL, μmol/L)", value=0.0, format="%.2f", key="TBIL_AKI")

            Cardiac_glycosides_encoded = Cardiac_glycosides_mapping[Cardiac_glycosides]
            Aspirin_encoded = Aspirin_mapping[Aspirin]

            features.extend([
                Scr, Cardiac_glycosides_encoded, Cys, Glucose, BUN, Neut, Lactic_acid, UA,
                Aspirin_encoded, Na, eGFR, Mg, INR_PT, FIB, TBIL
            ])

            if st.button("Predict AKI Probability"):
                aki_prob = predict_aki_probability(np.array(features).reshape(1, -1))
                st.write(f"AKI Probability: {aki_prob:.2f}")

        elif prediction_type == "mortality Prediction":
            st.subheader("Death Risk Prediction Features")

            Cardiac_glycosides = st.selectbox("Cardiac glycosides", ["NO", "Yes"], key="Cardiac_glycosides_death")
            dynamic = st.selectbox("Renal dynamic state", list(dynamic_mapping.keys()), key="dynamic_death")
            LDH = st.number_input("LDH (U/L)", value=0.0, format="%.2f", key="LDH_death")
            Lactic_acid = st.number_input("Lactic acid (mmol/L)", value=0.0, format="%.2f", key="Lactic_acid_death")
            Enzymes_antithrombotics = st.selectbox("Enzymes antithrombotics", ["NO", "Yes"], key="Enzymes_antithrombotics_death")
            Neut = st.number_input("Neutrophil count (10^9/L)", value=0.0, format="%.2f", key="Neut_death")
            A_G = st.number_input("A/G ratio", value=0.0, format="%.2f", key="AG_death")
            RF = st.number_input("Rheumatoid factor (IU/mL)", value=0.0, format="%.2f", key="RF_death")
            ALB = st.number_input("Albumin (g/L)", value=0.0, format="%.2f", key="ALB_death")
            Cys = st.number_input("Cystatin C (mg/L)", value=0.0, format="%.2f", key="Cys_death")
            Shock = st.selectbox("Shock", ["NO", "Yes"], key="Shock_death")
            GGT = st.number_input("GGT (U/L)", value=0.0, format="%.2f", key="GGT_death")
            MODS = st.selectbox("MODS", ["NO", "Yes"], key="MODS_death")
            PDE_inhibitor = st.selectbox("Phosphodiesterase inhibitor", ["NO", "Yes"], key="PDE_inhibitor_death")
            PT = st.number_input("Prothrombin time (sec)", value=0.0, format="%.2f", key="PT_death")

            features.extend([
                Cardiac_glycosides_mapping[Cardiac_glycosides],
                dynamic_mapping[dynamic],
                LDH, Lactic_acid,
                Enzymes_antithrombotics_mapping[Enzymes_antithrombotics],
                Neut, A_G, RF, ALB, Cys,
                Shock_mapping[Shock],
                GGT,
                MODS_mapping[MODS],
                PDE_inhibitor_mapping[PDE_inhibitor],
                PT
            ])

            if st.button("Predict Mortality Probability"):
                mortality_prob = predict_mortality_probability(np.array(features).reshape(1, -1))
                st.write(f"Mortality Probability: {mortality_prob:.2f}")

if __name__ == '__main__':
    main()

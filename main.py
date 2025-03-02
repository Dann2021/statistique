import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

import traitements.utilitaire as ut

st.write("# Statistiques")


donnees = st.text_input(label="Saisir les donnees")
effectif = st.text_input(label="Saisir les effectifs")


if donnees and effectif:

    # Traitement des donnees

    data, message = ut.transformeur(donnees)
    ni, entiers, message2 = ut.transformeur_liste(effectif)
    a, b, message3 = ut.parcours_tableau(data=data)

    # Analyse si il y a les erreurs
    if message:
        st.error(message)
    if message3:
        st.error(message3)
    if message2:
        st.error(message2)
    else:

        if len(b) != len(ni):
            st.warning("Le nombre total de classe doit être égale au nombre d'effectif")
        else:
            st.write("# Le tableau est le suivant : ")
            amplitude = ut.amplitude(a, b)

            check, valeur_retour = ut.verification_amplitudes(amplitude)
            if valeur_retour == 0:
                st.success(check)
            else:
                st.warning(check)

            ai = ut.correction_hauteur(check, amplitude)
            ec = ut.effectif_corrige(ni, ai)
            # print(f"ec : {ec} ")

            centre = ut.centre_classe(a, b)

            dico = ut.dataframe_dynamique(
                valeur_retour, a, b, ni, amplitude, ai, ec, centre
            )

            dataf = pd.DataFrame(data=dico)

            # Traitements des modes

            # Ici on sait que le mode correspond à l'effectif le plus élevé

            maximum = max(entiers)

            repetition = entiers.count(
                maximum
            )  # ici on va vérifié si ce maximum se repete

            # 1 - si la serie admet un seul mode
            if repetition == 1:
                mode, index, message = ut.mode(entiers)
                c1, c2 = a[index], b[index]
                st.success(message)
                st.write(
                    f"Le mode est ${mode}$ et correspond à la classe $[{c1};{c2}]$"
                )
            else:
                message, dico = ut.mode_multiple(a, b, entiers)
                st.success(message)
                st.dataframe(dico)

            # _, _, dico = ut.mode2(a, b, liste)

            st.dataframe(data=dataf)


else:
    st.warning("Veuillez saisir les données")

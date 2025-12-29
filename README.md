# Ensae-Prog2A
# Projet Python pour la Data Science (2025-2026)
Auteurs : Assoun Raphaël, 
# Présentation du Sujet
Les cryptomonnaies, et en particulier le Bitcoin, sont souvent présentées comme des actifs faiblement corrélés aux marchés financiers traditionnels, ce qui en ferait des outils potentiels de diversification. Toutefois, cette propriété semble se fragiliser lors de périodes de tensions économiques ou financières, où les comportements de marché tendent à se rapprocher. Ces épisodes soulèvent des questions importantes quant au rôle réel du Bitcoin face aux chocs macroéconomiques et aux crises de marché.
L’objectif de ce projet est d’analyser l’évolution de la corrélation entre le Bitcoin et différents actifs financiers, et de mieux comprendre les mécanismes susceptibles d’expliquer ses variations dans le temps. En étudiant ces relations dans un cadre empirique, ce travail vise à évaluer dans quelle mesure le Bitcoin conserve ses caractéristiques d’actif alternatif, notamment dans les phases de stress, et à en tirer des enseignements en matière de gestion du risque et de diversification de portefeuille.
# Problématique
Dans quelle mesure les cryptomonnaies peuvent-elles jouer un rôle de diversification au regard de l’évolution de leur corrélation avec les actifs financiers traditionnels ?
# Méthodologie :

***1. Collecte de données*** <br>
Nous collectons des données historiques de prix et de volumes pour les principales cryptomonnaies, indices boursiers et matières premières via Yahoo Finance, puis nous enrichissons le jeu de données avec des indicateurs macro-financiers (VIX, taux réels, énergie) issus de la base FRED. L’ensemble des séries est harmonisé sur une base temporelle commune, nettoyé et transformé en rendements journaliers logarithmiques afin de permettre une analyse cohérente des corrélations et des dynamiques temporelles.

***2. Analyse descriptive*** <br>
Ensuite nous analysons des rendements journaliers de Bitcoin et Ethereum par rapport aux indices boursiers (S&P 500, NASDAQ, FTSE 100, Euro Stoxx 50, Nikkei 225), aux matières premières (or, argent, énergie, métaux) et aux taux d’intérêt américains. Nous étudions des corrélations classiques, glissantes et conditionnelles selon le régime de volatilité (VIX), ainsi que des variations autour de chocs macroéconomiques (COVID‑19, annonces commerciales). Les analyses incluent également les corrélations avec décalage temporel, les volumes des actifs et l’impact sur différentes configurations de portefeuilles.

***3. Modélisation*** <br>







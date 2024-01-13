from pathlib import Path
from pydantic_settings import BaseSettings


class _Settings(BaseSettings):
    # Districts dict with coordinates to focus in district view
    DISTRICTS: dict = {
        'Arganzuela': [-3.6977073720303224, 40.39696549068384],
        'Barajas': [-3.5798445416938307, 40.47426260285562],
        'Carabanchel': [-3.7450019525130926, 40.37421297195493],
        'Centro': [-3.7450019525130926, 40.37421297195493],
        'Chamartin': [-3.6761647124896797, 40.45884516797494],
        'Chamberi': [-3.705624553016122, 40.4389269183163],
        'Ciudad Lineal': [-3.6511046331729915, 40.448498837010845],
        'Fuencarral-El Pardo': [-3.6924088198917957, 40.497230174061485],
        'Hortaleza': [-3.6436170484341517, 40.47253959492912],
        'Latina': [-3.7366958787908118, 40.40379531504183],
        'Moncloa-Aravaca': [-3.749754866885297, 40.4312012601919],
        'Moratalaz': [-3.6450034600497077, 40.405914222890345],
        'Puente de Vallecas': [-3.6584853901355245, 40.386515584691296],
        'Retiro': [-3.6760182341180325, 40.41108711730982],
        'Salamanca': [-3.681145256622216, 40.42714647084156],
        'San Blas': [-3.6205617333341706, 40.4353935944126],
        'Tetuan': [-3.698580766994951, 40.46077102857467],
        'Usera': [-3.707024057787578, 40.38390299292067],
        'Vicalvaro': [-3.5964440033652636, 40.4020033833267],
        'Villa de Vallecas': [-3.6220842669656577, 40.37674567380975],
        'Villaverde': [-3.6977774986072234, 40.34567971812692]
    }

    # Mongo related settings
    MONGO_URI: str = "mongodb://mongo"
    PORT: int = 27017
    MONGO_DB: str = "myapp"
    TTL: int = 3600 * 24 * 30

    # Settings for app
    GEOJSON_FILE: str = "data/madrid-districts.geojson"
    TEMP_SERIES_PROJECTION: dict = {'idelem': 1, 'carga': 1, 'fecha_hora': 1, 'distrito': 1}
    N_SENSORS: int = 4607
    SUBAREA_COLORS: dict = {
        'Arganzuela': {'110068': 'hsl(0.0,50%,50%)', '110018': 'hsl(17.142857142857142,50%,50%)',
                       '0': 'hsl(34.285714285714285,50%,50%)', None: 'hsl(51.42857142857143,50%,50%)',
                       '110011': 'hsl(68.57142857142857,50%,50%)', '0101': 'hsl(85.71428571428571,50%,50%)',
                       '110069': 'hsl(102.85714285714286,50%,50%)', '0129': 'hsl(120.0,50%,50%)',
                       '110092': 'hsl(137.14285714285714,50%,50%)', '110033': 'hsl(154.28571428571428,50%,50%)',
                       '110078': 'hsl(171.42857142857142,50%,50%)', '110093': 'hsl(188.57142857142856,50%,50%)',
                       '110016': 'hsl(205.71428571428572,50%,50%)', '110031': 'hsl(222.85714285714286,50%,50%)',
                       '110025': 'hsl(240.0,50%,50%)', '110070': 'hsl(257.1428571428571,50%,50%)',
                       '110023': 'hsl(274.2857142857143,50%,50%)', '110049': 'hsl(291.42857142857144,50%,50%)',
                       '110035': 'hsl(308.57142857142856,50%,50%)', '0114': 'hsl(325.7142857142857,50%,50%)',
                       '0112': 'hsl(342.85714285714283,50%,50%)', 'unknown': '#39b0b3'},
        'Barajas': {'3902': 'hsl(0.0,50%,50%)', '3904': 'hsl(51.42857142857143,50%,50%)',
                    '4013': 'hsl(102.85714285714286,50%,50%)', '3901': 'hsl(154.28571428571428,50%,50%)',
                    '3818': 'hsl(205.71428571428572,50%,50%)', '3906': 'hsl(257.14285714285717,50%,50%)',
                    '3805': 'hsl(308.57142857142856,50%,50%)', 'unknown': '#39b0b3'},
        'Carabanchel': {'110068': 'hsl(0.0,50%,50%)', '1774': 'hsl(51.42857142857143,50%,50%)',
                        '1758': 'hsl(102.85714285714286,50%,50%)', '1773': 'hsl(12.413793103448276,50%,50%)',
                        '1764': 'hsl(24.82758620689655,50%,50%)', '1765': 'hsl(13.333333333333334,50%,50%)',
                        '1722': 'hsl(37.241379310344826,50%,50%)', '0': 'hsl(49.6551724137931,50%,50%)',
                        '1721': 'hsl(62.06896551724138,50%,50%)', None: 'hsl(74.48275862068965,50%,50%)',
                        '1733': 'hsl(86.89655172413794,50%,50%)', '0129': 'hsl(99.3103448275862,50%,50%)',
                        '1759': 'hsl(111.72413793103448,50%,50%)', '1740': 'hsl(124.13793103448276,50%,50%)',
                        '1739': 'hsl(136.55172413793105,50%,50%)', '1742': 'hsl(148.9655172413793,50%,50%)',
                        '1710': 'hsl(161.3793103448276,50%,50%)', '1741': 'hsl(173.79310344827587,50%,50%)',
                        '1702': 'hsl(186.20689655172413,50%,50%)', '1763': 'hsl(198.6206896551724,50%,50%)',
                        '1744': 'hsl(211.0344827586207,50%,50%)', '1724': 'hsl(223.44827586206895,50%,50%)',
                        '1715': 'hsl(235.86206896551724,50%,50%)', '1727': 'hsl(248.27586206896552,50%,50%)',
                        '1726': 'hsl(260.6896551724138,50%,50%)', '1756': 'hsl(273.1034482758621,50%,50%)',
                        '1751': 'hsl(285.51724137931035,50%,50%)', '1720': 'hsl(297.9310344827586,50%,50%)',
                        '1719': 'hsl(310.3448275862069,50%,50%)', '1761': 'hsl(322.7586206896552,50%,50%)',
                        '1712': 'hsl(335.17241379310343,50%,50%)', '1757': 'hsl(347.58620689655174,50%,50%)',
                        'unknown': '#39b0b3'},
        'Centro': {'110007': 'hsl(0.0,50%,50%)', '110003': 'hsl(21.176470588235293,50%,50%)',
                   '110039': 'hsl(42.35294117647059,50%,50%)', '0': 'hsl(63.529411764705884,50%,50%)',
                   '0101': 'hsl(84.70588235294117,50%,50%)', '110092': 'hsl(105.88235294117646,50%,50%)',
                   '110013': 'hsl(127.05882352941177,50%,50%)', '110037': 'hsl(148.23529411764704,50%,50%)',
                   '110021': 'hsl(169.41176470588235,50%,50%)', '110017': 'hsl(190.58823529411765,50%,50%)',
                   '110025': 'hsl(211.76470588235293,50%,50%)', '110027': 'hsl(232.94117647058823,50%,50%)',
                   '0105': 'hsl(254.11764705882354,50%,50%)', '110023': 'hsl(275.29411764705884,50%,50%)',
                   '110019': 'hsl(296.4705882352941,50%,50%)', '110046': 'hsl(317.6470588235294,50%,50%)',
                   '0152': 'hsl(338.8235294117647,50%,50%)', 'unknown': '#39b0b3'},
        'Chamartin': {'130009': 'hsl(0.0,50%,50%)', '0': 'hsl(13.333333333333334,50%,50%)',
                      '0124': 'hsl(26.666666666666668,50%,50%)', '0329': 'hsl(40.0,50%,50%)',
                      None: 'hsl(53.333333333333336,50%,50%)', '0101': 'hsl(66.66666666666667,50%,50%)',
                      '130030': 'hsl(80.0,50%,50%)', '0304': 'hsl(93.33333333333334,50%,50%)',
                      '0334': 'hsl(106.66666666666667,50%,50%)', '0308': 'hsl(120.0,50%,50%)',
                      '130017': 'hsl(133.33333333333334,50%,50%)', '0311': 'hsl(146.66666666666669,50%,50%)',
                      '130007': 'hsl(160.0,50%,50%)', '110036': 'hsl(173.33333333333334,50%,50%)',
                      '130033': 'hsl(186.66666666666669,50%,50%)', '3204': 'hsl(200.0,50%,50%)',
                      '130031': 'hsl(213.33333333333334,50%,50%)', '130010': 'hsl(226.66666666666669,50%,50%)',
                      '0301': 'hsl(240.0,50%,50%)', '130018': 'hsl(253.33333333333334,50%,50%)',
                      '110030': 'hsl(266.6666666666667,50%,50%)', '110034': 'hsl(280.0,50%,50%)',
                      '0302': 'hsl(293.33333333333337,50%,50%)', '3203': 'hsl(306.6666666666667,50%,50%)',
                      '0306': 'hsl(320.0,50%,50%)', '3215': 'hsl(333.33333333333337,50%,50%)',
                      '130032': 'hsl(346.6666666666667,50%,50%)', 'unknown': '#39b0b3'},
        'Chamberi': {'0313': 'hsl(0.0,50%,50%)', '0305': 'hsl(27.692307692307693,50%,50%)',
                     '0': 'hsl(55.38461538461539,50%,50%)', '0101': 'hsl(83.07692307692308,50%,50%)',
                     '110009': 'hsl(110.76923076923077,50%,50%)', '0304': 'hsl(138.46153846153845,50%,50%)',
                     '110026': 'hsl(166.15384615384616,50%,50%)', '0301': 'hsl(193.84615384615387,50%,50%)',
                     '0108': 'hsl(221.53846153846155,50%,50%)', '0105': 'hsl(249.23076923076923,50%,50%)',
                     '110006': 'hsl(276.9230769230769,50%,50%)', '0152': 'hsl(304.61538461538464,50%,50%)',
                     '0303': 'hsl(332.3076923076923,50%,50%)', 'unknown': '#39b0b3'},
        'Ciudad Lineal': {'3210': 'hsl(0.0,50%,50%)', '3802': 'hsl(14.4,50%,50%)', '3605': 'hsl(28.8,50%,50%)',
                          '3248': 'hsl(43.2,50%,50%)', None: 'hsl(57.6,50%,50%)', '3228': 'hsl(72.0,50%,50%)',
                          '3202': 'hsl(86.4,50%,50%)', '3603': 'hsl(100.8,50%,50%)', '3246': 'hsl(115.2,50%,50%)',
                          '3240': 'hsl(129.6,50%,50%)', '3204': 'hsl(144.0,50%,50%)', '3201': 'hsl(158.4,50%,50%)',
                          '3206': 'hsl(172.8,50%,50%)', '3219': 'hsl(187.20000000000002,50%,50%)',
                          '3602': 'hsl(201.6,50%,50%)', '3214': 'hsl(216.0,50%,50%)', '3212': 'hsl(230.4,50%,50%)',
                          '3218': 'hsl(244.8,50%,50%)', '3211': 'hsl(259.2,50%,50%)', '3203': 'hsl(273.6,50%,50%)',
                          '3216': 'hsl(288.0,50%,50%)', '3604': 'hsl(302.40000000000003,50%,50%)',
                          '3227': 'hsl(316.8,50%,50%)', '3601': 'hsl(331.2,50%,50%)', '3215': 'hsl(345.6,50%,50%)',
                          'unknown': '#39b0b3'},
        'Fuencarral-El Pardo': {'0314': 'hsl(0.0,50%,50%)', '3140': 'hsl(8.372093023255815,50%,50%)',
                                '3107': 'hsl(16.74418604651163,50%,50%)', '3137': 'hsl(25.116279069767444,50%,50%)',
                                '3105': 'hsl(33.48837209302326,50%,50%)', '0': 'hsl(41.86046511627907,50%,50%)',
                                '3106': 'hsl(50.23255813953489,50%,50%)', '3118': 'hsl(58.6046511627907,50%,50%)',
                                None: 'hsl(66.97674418604652,50%,50%)', '3110': 'hsl(75.34883720930233,50%,50%)',
                                '3128': 'hsl(83.72093023255815,50%,50%)', '3117': 'hsl(92.09302325581396,50%,50%)',
                                '130019': 'hsl(100.46511627906978,50%,50%)', '3139': 'hsl(108.83720930232559,50%,50%)',
                                '3112': 'hsl(117.2093023255814,50%,50%)', '3115': 'hsl(125.58139534883722,50%,50%)',
                                '130025': 'hsl(133.95348837209303,50%,50%)',
                                '130035': 'hsl(142.32558139534885,50%,50%)', '3138': 'hsl(150.69767441860466,50%,50%)',
                                '130015': 'hsl(159.06976744186048,50%,50%)', '130033': 'hsl(167.4418604651163,50%,50%)',
                                '3103': 'hsl(175.8139534883721,50%,50%)', '3109': 'hsl(184.18604651162792,50%,50%)',
                                '3122': 'hsl(192.55813953488374,50%,50%)', '4002': 'hsl(200.93023255813955,50%,50%)',
                                '3119': 'hsl(209.30232558139537,50%,50%)', '3101': 'hsl(217.67441860465118,50%,50%)',
                                '3127': 'hsl(226.046511627907,50%,50%)', '3124': 'hsl(234.4186046511628,50%,50%)',
                                '130020': 'hsl(242.79069767441862,50%,50%)',
                                '130023': 'hsl(251.16279069767444,50%,50%)', '130024': 'hsl(259.5348837209302,50%,50%)',
                                '3130': 'hsl(267.90697674418607,50%,50%)', '3129': 'hsl(276.2790697674419,50%,50%)',
                                '3108': 'hsl(284.6511627906977,50%,50%)', '3111': 'hsl(293.0232558139535,50%,50%)',
                                '4001': 'hsl(301.3953488372093,50%,50%)', '3102': 'hsl(309.76744186046517,50%,50%)',
                                '3104': 'hsl(318.13953488372096,50%,50%)', '3136': 'hsl(326.51162790697674,50%,50%)',
                                '3133': 'hsl(334.8837209302326,50%,50%)', '130032': 'hsl(343.2558139534884,50%,50%)',
                                '3120': 'hsl(351.6279069767442,50%,50%)', 'unknown': '#39b0b3'},
        'Hortaleza': {'3808': 'hsl(0.0,50%,50%)', '3802': 'hsl(14.4,50%,50%)', '3807': 'hsl(28.8,50%,50%)',
                      '3801': 'hsl(43.2,50%,50%)', '3809': 'hsl(57.6,50%,50%)', '4013': 'hsl(72.0,50%,50%)',
                      '3905': 'hsl(86.4,50%,50%)', '4009': 'hsl(100.8,50%,50%)', '4006': 'hsl(115.2,50%,50%)',
                      '4003': 'hsl(129.6,50%,50%)', '3806': 'hsl(144.0,50%,50%)', '3817': 'hsl(158.4,50%,50%)',
                      '4002': 'hsl(172.8,50%,50%)', '3813': 'hsl(187.20000000000002,50%,50%)',
                      '3815': 'hsl(201.6,50%,50%)', '4011': 'hsl(216.0,50%,50%)', '3812': 'hsl(230.4,50%,50%)',
                      '3803': 'hsl(244.8,50%,50%)', '4004': 'hsl(259.2,50%,50%)', '3804': 'hsl(273.6,50%,50%)',
                      '3805': 'hsl(288.0,50%,50%)', '4012': 'hsl(302.40000000000003,50%,50%)',
                      '4001': 'hsl(316.8,50%,50%)', '3218': 'hsl(331.2,50%,50%)', '3203': 'hsl(345.6,50%,50%)',
                      'unknown': '#39b0b3'},
        'Latina': {'1773': 'hsl(0.0,50%,50%)', '1765': 'hsl(14.4,50%,50%)', '1735': 'hsl(28.8,50%,50%)',
                   '1721': 'hsl(43.2,50%,50%)', None: 'hsl(57.6,50%,50%)', '1753': 'hsl(72.0,50%,50%)',
                   '1749': 'hsl(86.4,50%,50%)', '1772': 'hsl(100.8,50%,50%)', '1769': 'hsl(115.2,50%,50%)',
                   '1734': 'hsl(129.6,50%,50%)', '1762': 'hsl(144.0,50%,50%)', '1755': 'hsl(158.4,50%,50%)',
                   '110025': 'hsl(172.8,50%,50%)', '1702': 'hsl(187.20000000000002,50%,50%)',
                   '1724': 'hsl(201.6,50%,50%)', '1715': 'hsl(216.0,50%,50%)', '1718': 'hsl(230.4,50%,50%)',
                   '1752': 'hsl(244.8,50%,50%)', '1701': 'hsl(259.2,50%,50%)', '1736': 'hsl(273.6,50%,50%)',
                   '1743': 'hsl(288.0,50%,50%)', '1719': 'hsl(302.40000000000003,50%,50%)',
                   '1712': 'hsl(316.8,50%,50%)', '1717': 'hsl(331.2,50%,50%)', '1767': 'hsl(345.6,50%,50%)',
                   'unknown': '#39b0b3'},
        'Moncloa-Aravaca': {'130038': 'hsl(0.0,50%,50%)', '110045': 'hsl(10.909090909090908,50%,50%)',
                            '110003': 'hsl(21.818181818181817,50%,50%)', '0166': 'hsl(32.72727272727273,50%,50%)',
                            '0313': 'hsl(43.63636363636363,50%,50%)', '130016': 'hsl(54.54545454545454,50%,50%)',
                            '0143': 'hsl(65.45454545454545,50%,50%)', '2005': 'hsl(76.36363636363636,50%,50%)',
                            '0': 'hsl(87.27272727272727,50%,50%)', None: 'hsl(98.18181818181817,50%,50%)',
                            '110009': 'hsl(109.09090909090908,50%,50%)', '130019': 'hsl(119.99999999999999,50%,50%)',
                            '2002': 'hsl(130.9090909090909,50%,50%)', '2009': 'hsl(141.8181818181818,50%,50%)',
                            '3139': 'hsl(152.72727272727272,50%,50%)', '0328': 'hsl(163.63636363636363,50%,50%)',
                            '3115': 'hsl(174.54545454545453,50%,50%)', '2006': 'hsl(185.45454545454544,50%,50%)',
                            '130025': 'hsl(196.36363636363635,50%,50%)', '2004': 'hsl(207.27272727272725,50%,50%)',
                            '2008': 'hsl(218.18181818181816,50%,50%)', '130036': 'hsl(229.09090909090907,50%,50%)',
                            '110064': 'hsl(239.99999999999997,50%,50%)', '110027': 'hsl(250.90909090909088,50%,50%)',
                            '0105': 'hsl(261.8181818181818,50%,50%)', '110063': 'hsl(272.7272727272727,50%,50%)',
                            '130041': 'hsl(283.6363636363636,50%,50%)', '130012': 'hsl(294.5454545454545,50%,50%)',
                            '1736': 'hsl(305.45454545454544,50%,50%)', '2001': 'hsl(316.3636363636363,50%,50%)',
                            '110006': 'hsl(327.27272727272725,50%,50%)', '2003': 'hsl(338.18181818181813,50%,50%)',
                            '110062': 'hsl(349.09090909090907,50%,50%)', 'unknown': '#39b0b3'},
        'Moratalaz': {'3210': 'hsl(0.0,50%,50%)', '3517': 'hsl(36.0,50%,50%)', '3507': 'hsl(72.0,50%,50%)',
                      '3506': 'hsl(108.0,50%,50%)', '3504': 'hsl(144.0,50%,50%)', None: 'hsl(180.0,50%,50%)',
                      '3503': 'hsl(216.0,50%,50%)', '3505': 'hsl(252.0,50%,50%)', '3501': 'hsl(288.0,50%,50%)',
                      '3522': 'hsl(324.0,50%,50%)', 'unknown': '#39b0b3'},
        'Puente de Vallecas': {'3526': 'hsl(0.0,50%,50%)', '3019': 'hsl(18.94736842105263,50%,50%)',
                               '3507': 'hsl(37.89473684210526,50%,50%)', '3512': 'hsl(56.84210526315789,50%,50%)',
                               '3003': 'hsl(75.78947368421052,50%,50%)', None: 'hsl(94.73684210526315,50%,50%)',
                               '3036': 'hsl(113.68421052631578,50%,50%)', '3002': 'hsl(132.6315789473684,50%,50%)',
                               '3026': 'hsl(151.57894736842104,50%,50%)', '3008': 'hsl(170.52631578947367,50%,50%)',
                               '3004': 'hsl(189.4736842105263,50%,50%)', '3001': 'hsl(208.42105263157893,50%,50%)',
                               '3514': 'hsl(227.36842105263156,50%,50%)', '3005': 'hsl(246.3157894736842,50%,50%)',
                               '3510': 'hsl(265.2631578947368,50%,50%)', '3007': 'hsl(284.2105263157895,50%,50%)',
                               '3513': 'hsl(303.1578947368421,50%,50%)', '3006': 'hsl(322.1052631578947,50%,50%)',
                               '0112': 'hsl(341.05263157894734,50%,50%)', 'unknown': '#39b0b3'},
        'Retiro': {'110040': 'hsl(0.0,50%,50%)', '110003': 'hsl(36.0,50%,50%)', '110041': 'hsl(72.0,50%,50%)',
                   '0': 'hsl(108.0,50%,50%)', None: 'hsl(144.0,50%,50%)', '0101': 'hsl(180.0,50%,50%)',
                   '110050': 'hsl(216.0,50%,50%)', '0104': 'hsl(252.0,50%,50%)', '3001': 'hsl(288.0,50%,50%)',
                   '110010': 'hsl(324.0,50%,50%)', 'unknown': '#39b0b3'},
        'Salamanca': {'110041': 'hsl(0.0,50%,50%)', '0': 'hsl(27.692307692307693,50%,50%)',
                      '0124': 'hsl(55.38461538461539,50%,50%)', None: 'hsl(83.07692307692308,50%,50%)',
                      '0101': 'hsl(110.76923076923077,50%,50%)', '110088': 'hsl(138.46153846153845,50%,50%)',
                      '110032': 'hsl(166.15384615384616,50%,50%)', '0104': 'hsl(193.84615384615387,50%,50%)',
                      '110020': 'hsl(221.53846153846155,50%,50%)', '110022': 'hsl(249.23076923076923,50%,50%)',
                      '3212': 'hsl(276.9230769230769,50%,50%)', '110034': 'hsl(304.61538461538464,50%,50%)',
                      '3211': 'hsl(332.3076923076923,50%,50%)', 'unknown': '#39b0b3'},
        'San Blas': {'3226': 'hsl(0.0,50%,50%)', '3224': 'hsl(18.94736842105263,50%,50%)',
                     '3208': 'hsl(37.89473684210526,50%,50%)', '3233': 'hsl(56.84210526315789,50%,50%)',
                     '3202': 'hsl(75.78947368421052,50%,50%)', '3220': 'hsl(94.73684210526315,50%,50%)',
                     '4101': 'hsl(113.68421052631578,50%,50%)', '3222': 'hsl(132.6315789473684,50%,50%)',
                     '3217': 'hsl(151.57894736842104,50%,50%)', '3245': 'hsl(170.52631578947367,50%,50%)',
                     '4102': 'hsl(189.4736842105263,50%,50%)', '3225': 'hsl(208.42105263157893,50%,50%)',
                     '3206': 'hsl(227.36842105263156,50%,50%)', '3244': 'hsl(246.3157894736842,50%,50%)',
                     '3209': 'hsl(265.2631578947368,50%,50%)', '3205': 'hsl(284.2105263157895,50%,50%)',
                     '3805': 'hsl(303.1578947368421,50%,50%)', '4103': 'hsl(322.1052631578947,50%,50%)',
                     '3223': 'hsl(341.05263157894734,50%,50%)', 'unknown': '#39b0b3'},
        'Tetuan': {'130038': 'hsl(0.0,50%,50%)', '130037': 'hsl(20.0,50%,50%)', '0305': 'hsl(40.0,50%,50%)',
                   '0': 'hsl(60.0,50%,50%)', '130039': 'hsl(80.0,50%,50%)', '0304': 'hsl(100.0,50%,50%)',
                   '130025': 'hsl(120.0,50%,50%)', '130021': 'hsl(140.0,50%,50%)', '130022': 'hsl(160.0,50%,50%)',
                   '130026': 'hsl(180.0,50%,50%)', '130033': 'hsl(200.0,50%,50%)', '0301': 'hsl(220.0,50%,50%)',
                   '130023': 'hsl(240.0,50%,50%)', '130024': 'hsl(260.0,50%,50%)', '130012': 'hsl(280.0,50%,50%)',
                   '0303': 'hsl(300.0,50%,50%)', '130032': 'hsl(320.0,50%,50%)', '130043': 'hsl(340.0,50%,50%)',
                   'unknown': '#39b0b3'},
        'Usera': {'1713': 'hsl(0.0,50%,50%)', '1706': 'hsl(20.0,50%,50%)', '1703': 'hsl(40.0,50%,50%)',
                  '1702': 'hsl(60.0,50%,50%)', '1766': 'hsl(80.0,50%,50%)', '1731': 'hsl(100.0,50%,50%)',
                  '1745': 'hsl(120.0,50%,50%)', '1754': 'hsl(140.0,50%,50%)', '1759': 'hsl(160.0,50%,50%)',
                  '1720': 'hsl(180.0,50%,50%)', '1714': 'hsl(200.0,50%,50%)', '1729': 'hsl(220.0,50%,50%)',
                  '1730': 'hsl(240.0,50%,50%)', '1705': 'hsl(260.0,50%,50%)', '0': 'hsl(280.0,50%,50%)',
                  None: 'hsl(300.0,50%,50%)', '1765': 'hsl(320.0,50%,50%)', '1774': 'hsl(340.0,50%,50%)',
                  'unknown': '#39b0b3'},
        'Vicalvaro': {'3702': 'hsl(0.0,50%,50%)', '3524': 'hsl(60.0,50%,50%)', '3701': 'hsl(120.0,50%,50%)',
                      '3704': 'hsl(180.0,50%,50%)', '3703': 'hsl(240.0,50%,50%)', '3705': 'hsl(300.0,50%,50%)',
                      'unknown': '#39b0b3'},
        'Villa de Vallecas': {'3031': 'hsl(0.0,50%,50%)', '3027': 'hsl(27.692307692307693,50%,50%)',
                              '3021': 'hsl(55.38461538461539,50%,50%)', '3032': 'hsl(83.07692307692308,50%,50%)',
                              '3035': 'hsl(110.76923076923077,50%,50%)', '3022': 'hsl(138.46153846153845,50%,50%)',
                              '3004': 'hsl(166.15384615384616,50%,50%)', '3034': 'hsl(193.84615384615387,50%,50%)',
                              '3025': 'hsl(221.53846153846155,50%,50%)', '3023': 'hsl(249.23076923076923,50%,50%)',
                              '3005': 'hsl(276.9230769230769,50%,50%)', '3040': 'hsl(304.61538461538464,50%,50%)',
                              '3033': 'hsl(332.3076923076923,50%,50%)', 'unknown': '#39b0b3'},
        'Villaverde': {'1746': 'hsl(0.0,50%,50%)', '1706': 'hsl(30.0,50%,50%)', '1707': 'hsl(60.0,50%,50%)',
                       '1711': 'hsl(90.0,50%,50%)', '1738': 'hsl(120.0,50%,50%)', '1716': 'hsl(150.0,50%,50%)',
                       '1723': 'hsl(180.0,50%,50%)', '1766': 'hsl(210.0,50%,50%)', '1708': 'hsl(240.0,50%,50%)',
                       '1748': 'hsl(270.0,50%,50%)', '1709': 'hsl(300.0,50%,50%)', '1730': 'hsl(330.0,50%,50%)',
                       'unknown': '#39b0b3'},
        'unknown': {}
    }


class Config:
    env_file = ".env"
    file_path = Path(env_file)
    if not file_path.is_file():
        print("⚠ `.env` not found in current directory")
        print("⚙ Loading settings from environment")
    else:
        print(f"⚙ Loading settings from dotenv @ {file_path.absolute()}")


settings = _Settings()
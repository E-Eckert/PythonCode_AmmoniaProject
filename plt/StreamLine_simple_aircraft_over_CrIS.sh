#!/bin/bash
#
# Stream lines plotting aircraft data over CrIS (no projection)
#

# Plot Aircraft over CrIS:
# ========================
# Specifications:
#   - xretv pressure level 3 (~825hPa)
#   - aircraft 100 step average
#   - 0.25x0.25 pixel boxes for CrIS
python "../../../../Python/Routines/Ammonia/plt/plt_simple_aircraft_over_CrIS.py" << EOF
../../../../plt/Ammonia/Aircraft_over_CrIS_simple
jpg
xretv
3
1000
54
59
-113
-108
-1
15
100
0.25
0.25
EOF

# Plot Aircraft over CrIS:
# ========================
# Specifications:
#   - xretv pressure level 4 (~750hPa)
#   - aircraft 100 step average
#   - 0.25x0.25 pixel boxes for CrIS
python "../../../../Python/Routines/Ammonia/plt/plt_simple_aircraft_over_CrIS.py" << EOF
../../../../plt/Ammonia/Aircraft_over_CrIS_simple
jpg
xretv
4
1000
54
59
-113
-108
-1
15
100
0.25
0.25
EOF

# Plot Aircraft over CrIS:
# ========================
# Specifications:
#   - xretv pressure level 3 (~825hPa)
#   - aircraft 200 step average
#   - 0.25x0.25 pixel boxes for CrIS
python "../../../../Python/Routines/Ammonia/plt/plt_simple_aircraft_over_CrIS.py" << EOF
../../../../plt/Ammonia/Aircraft_over_CrIS_simple
jpg
xretv
3
1000
54
59
-113
-108
-1
15
200
0.25
0.25
EOF

# Plot Aircraft over CrIS:
# ========================
# Specifications:
#   - xretv pressure level 4 (~750hPa)
#   - aircraft 200 step average
#   - 0.25x0.25 pixel boxes for CrIS
python "../../../../Python/Routines/Ammonia/plt/plt_simple_aircraft_over_CrIS.py" << EOF
../../../../plt/Ammonia/Aircraft_over_CrIS_simple
jpg
xretv
4
1000
54
59
-113
-108
-1
15
200
0.25
0.25
EOF

# Plot Aircraft over CrIS:
# ========================
# Specifications:
#   - xretv pressure level 3 (~825hPa)
#   - aircraft 50 step average
#   - 0.25x0.25 pixel boxes for CrIS
python "../../../../Python/Routines/Ammonia/plt/plt_simple_aircraft_over_CrIS.py" << EOF
../../../../plt/Ammonia/Aircraft_over_CrIS_simple
jpg
xretv
3
1000
54
59
-113
-108
-1
15
50
0.25
0.25
EOF

# Plot Aircraft over CrIS:
# ========================
# Specifications:
#   - xretv pressure level 4 (~750hPa)
#   - aircraft 50 step average
#   - 0.25x0.25 pixel boxes for CrIS
python "../../../../Python/Routines/Ammonia/plt/plt_simple_aircraft_over_CrIS.py" << EOF
../../../../plt/Ammonia/Aircraft_over_CrIS_simple
jpg
xretv
4
1000
54
59
-113
-108
-1
15
50
0.25
0.25
EOF

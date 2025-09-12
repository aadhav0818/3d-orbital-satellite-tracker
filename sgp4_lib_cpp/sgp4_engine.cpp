#include "Tle.h"
#include "Sgp4.h"
#include "Eci.h"
#include "DateTime.h"
#include <vector>

using namespace libsgp4;

extern "C" {

__declspec(dllexport)
void propagate_satellite(const char* line1, const char* line2, double year, int month, int day,
                         int hour, int min, double sec, double* xyz_out) 

{
    Tle tle("SAT", line1, line2);
    SGP4 sgp4(tle);
    DateTime dt(year, month, day, hour, min, sec);
    Eci eci = sgp4.FindPosition(dt);

    xyz_out[0] = eci.Position().x;
    xyz_out[1] = eci.Position().y;
    xyz_out[2] = eci.Position().z;
}
}

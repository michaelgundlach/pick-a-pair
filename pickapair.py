import math

# single patient implementation patient prescription is in [sph, cyl, axis] notation as a list
patient_prescription = [-2.00, -1.00, 25]

# quick and simple list of glasses a list of prescription within a list, this could probably be
# implemented as a class for prescriptions since all prescriptions glasses of patient will have
# similar components
list_of_glasses = [[-1.00, -2.00, 55], [-2.00, -1.00, 125],
                   [-2.00, -1.00, 25], [-2.00, -0.50, 22],
                   [-1.00, -1.00, 15], [-1.00, -0.50, 50]]

# relative importance of cylinder and axis errors versus sphere errors
cyl_weight = 0.5
axis_weight = 0.5

def fitness_for_prescription(prescription, glasses):
    def scrip_data(scrip):
        # scrip is [sph, cyl, axis]
        data = {}
        # prescription parameters
        data['sph'] = scrip[0]
        data['cyl'] = scrip[1]
        data['axis'] = math.radians(scrip[2])
        # MRE, Cyl@045, Cyl@180
        data['MRE'] = data['sph'] + data['cyl']/2
        data['C045'] = data['cyl'] * math.cos(2 * data['axis'])
        data['C180'] = data['cyl'] * math.sin(2 * data['axis'])
        return data

    pat = scrip_data(prescription)

    def error_for(pair):
        rx = scrip_data(pair)

        combined_error = 0

        #residual error calculations
        MRE_err = pat['MRE'] - rx['MRE']
        C045_err = pat['C045'] - rx['C045']
        C180_err = pat['C180'] - rx['C180']

        #make sure we don't divide by 0 by adding a negligable amount
        if C180_err == 0:
            C180_err += 0.00001

        # convert errors back to spherocylindrical form
        combcyl = C180_err + C045_err

        cyl_err = math.sqrt(abs(combcyl))
        sph_err = MRE_err - cyl_err / 2
        axis_err = math.atan(C045_err / C180_err) / 2

        #combine the spherical and cylindrical errors into a dioptric values
        combined_error += sph_err + (cyl_err * cyl_weight) + (axis_err * axis_weight)
        combined_error = abs(combined_error)

        return combined_error

    best_pairs = sorted(list_of_glasses, key=lambda pair: error_for(pair))
    return best_pairs[0:5]

print fitness_for_prescription(patient_prescription, list_of_glasses)

import sys
import data
import rbc
import helpers



def parse_sponsor_data_line(line):
    """
    Assumes blank and commented lines have already been removed.
    returns a tuple: (key/value pair)
    key is "last, first" name
    value is a tuple of sponsors ('first last')
    Fails if encounters an invalid line!!!
    """
    parts = line.split(":")
    sponsored = parts[0].strip()
    names = sponsored.split()
    name = '{}, {}'.format(names[1], names[0])
    part2 = parts[1]
    sponsors = tuple([
        sponsor.strip() for sponsor in parts[1].split(", ")])
    ret = name, sponsors
#   print("Parse line returning {}".format(repr(ret)))
    return ret


def get_sponsor_data(spot):
    """
    Returns a dict: keys are '2nd, 1st' names,
                    values are tuples of sponsors.
    """
    ret = {}
    with open(spot, 'r') as src:
#       lines = [
#           line for line in helpers.useful_lines(src, comment='#')]
#       for line in lines:
        for line in helpers.useful_lines(src, comment='#'):
#           print("Line is '{}".format(line))
            tup = parse_sponsor_data_line(line)
#           print("tup is {}".format(repr(tup)))
            (name, sponsors) = (tup[0], tup[1])
            ret[name] = sponsors
    return ret

sponsor_data = get_sponsor_data(rbc.Club.SPONSORS_SPoT)

for key in sponsor_data.keys():
    print('{}: {}'
          .format(key, 
                  ', '.join(sponsor_data[key])))
# line = "Jason Crichfield: Joseph Ferraro, Ralph Camiccia"
# print("Parse => {}".format(parse_sponsor_data_line(line)))


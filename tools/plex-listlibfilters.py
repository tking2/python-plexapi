from pprint import pprint
from collections import defaultdict


def find_filters(plex):
    filters = []
    for section in plex.library.sections():
        secs = defaultdict(list)
        data = plex.query('/library/sections/%s?includeDetails=1' % section.key)
        general = []

        # Find all general
        for d in data:
            # Find toplevel filters /library/sections/sectionnumber/year
            if d.tag == 'Directory':
                if 'prompt' not in d.attrib:
                    general.append(d.attrib.get('key'))

            if d.tag == 'Type':
                T = d.attrib.get('type')
                secs[T] = {}
                for dd in d:
                    # EX /library/sections/2/year?type=4
                    if dd.tag == 'Filter':
                        if 'filter' not in secs[T]:
                            secs[T]['filter'] = []
                        secs[T]['filter'].append(dd.attrib.get('filter'))

                    if dd.tag == 'Sort':
                        if 'sort' not in secs[T]:
                            secs[T]['sort'] = []
                        secs[T]['sort'].append(dd.attrib.get('key'))
                        secs[T]['sort'].append(dd.attrib.get('descKey'))

                    if dd.tag == 'Field':
                        if 'field' not in secs[T]:
                            secs[T]['field'] = []
                        secs[T]['field'].append(dd.attrib.get('key'))

        secs['general'] = general
        filters.append(secs)

    return filters

print(pprint(filters))

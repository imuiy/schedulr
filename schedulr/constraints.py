def meetings_overlap(m1, m2):
    if m1.day != m2.day:
        return False
    return not (m1.end <= m2.start or m2.end <= m1.start)


def sections_overlap(sec1, sec2):
    for m1 in sec1.meetings:
        for m2 in sec2.meetings:
            if meetings_overlap(m1, m2):
                return True
    return False

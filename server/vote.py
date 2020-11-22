
imposter = 1
alive = []


def pause():
    temp = 0


def imposter_remain():
    if imposter not in alive:
        print("crew win.")
        pause()


def vote():
    # et vote_rslt from vote module
    imposter_candidate = {1: 0, 2: 0, 3: 0, 4: 0}
    imposter = []
    vote_max = max(imposter_candidate.get(1), imposter_candidate.get(2), imposter_candidate.get(3),
                   imposter_candidate.get(4))
    for i in imposter_candidate:
        if i.value == vote_max:
            imposter.append(i.key)

    if len(imposter) == 1:
        alive.remove(imposter[0])
        print("crew" + imposter[0] + "is removed.")
        imposter_remain()
    else:
        print("nothing happened.")



def vote(alive_list):
    return alive_list


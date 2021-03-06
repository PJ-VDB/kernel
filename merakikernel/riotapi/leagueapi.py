import merakikernel.rediscache
import merakikernel.requests


_leagues_typename = "Leagues"
_league_entries_typename = "LeagueEntries"


def leagues_summoner(region, summonerIds, params={}):
    region = region.lower()
    ids = summonerIds.split(",")

    # 10 summoners max
    if len(ids) > 10:
        raise ValueError("Can only get leagues for up to 10 summoners at once.")

    leagues = merakikernel.rediscache.get_values(_leagues_typename, ids, region)

    missing = []
    loc = []
    for i in range(len(ids)):
        if not leagues[i]:
            missing.append(ids[i])
            loc.append(i)

    if missing:
        url = "/api/lol/{}/v2.5/league/by-summoner/{}".format(region, ",".join(missing))
        new_leagues = merakikernel.requests.get(region, url, params)

        for i in range(len(missing)):
            leagues[loc[i]] = new_leagues.get(missing[i], None)

        unzipped = [list(t) for t in zip(*new_leagues.items())]
        merakikernel.rediscache.put_values(_leagues_typename, unzipped[0], unzipped[1], region)

    return {ids[i]: leagues[i] for i in range(len(ids)) if leagues[i]}


def league_entries_summoner(region, summonerIds, params={}):
    region = region.lower()
    ids = summonerIds.split(",")

    # 10 summoners max
    if len(ids) > 10:
        raise ValueError("Can only get leagues for up to 10 summoners at once.")

    leagues = merakikernel.rediscache.get_values(_league_entries_typename, ids, region)

    missing = []
    loc = []
    for i in range(len(ids)):
        if not leagues[i]:
            missing.append(ids[i])
            loc.append(i)

    if missing:
        url = "/api/lol/{}/v2.5/league/by-summoner/{}/entry".format(region, ",".join(missing))
        new_leagues = merakikernel.requests.get(region, url, params)

        for i in range(len(missing)):
            leagues[loc[i]] = new_leagues.get(missing[i], None)

        unzipped = [list(t) for t in zip(*new_leagues.items())]
        merakikernel.rediscache.put_values(_league_entries_typename, unzipped[0], unzipped[1], region)

    return {ids[i]: leagues[i] for i in range(len(ids)) if leagues[i]}


def leagues_team(region, teamIds, params={}):
    region = region.lower()
    ids = teamIds.split(",")

    # 10 teams max
    if len(ids) > 10:
        raise ValueError("Can only get leagues for up to 10 teams at once.")

    leagues = merakikernel.rediscache.get_values(_leagues_typename, ids, region)

    missing = []
    loc = []
    for i in range(len(ids)):
        if not leagues[i]:
            missing.append(ids[i])
            loc.append(i)

    if missing:
        url = "/api/lol/{}/v2.5/league/by-team/{}".format(region, ",".join(missing))
        new_leagues = merakikernel.requests.get(region, url, params)

        for i in range(len(missing)):
            leagues[loc[i]] = new_leagues.get(missing[i], None)

        unzipped = [list(t) for t in zip(*new_leagues.items())]
        merakikernel.rediscache.put_values(_leagues_typename, unzipped[0], unzipped[1], region)

    return {ids[i]: leagues[i] for i in range(len(ids)) if leagues[i]}


def league_entries_team(region, teamIds, params={}):
    region = region.lower()
    ids = teamIds.split(",")

    # 10 teams max
    if len(ids) > 10:
        raise ValueError("Can only get league entries for up to 10 teams at once.")

    leagues = merakikernel.rediscache.get_values(_league_entries_typename, ids, region)

    missing = []
    loc = []
    for i in range(len(ids)):
        if not leagues[i]:
            missing.append(ids[i])
            loc.append(i)

    if missing:
        url = "/api/lol/{}/v2.5/league/by-team/{}/entry".format(region, ",".join(missing))
        new_leagues = merakikernel.requests.get(region, url, params)

        for i in range(len(missing)):
            leagues[loc[i]] = new_leagues.get(missing[i], None)

        unzipped = [list(t) for t in zip(*new_leagues.items())]
        merakikernel.rediscache.put_values(_league_entries_typename, unzipped[0], unzipped[1], region)

    return {ids[i]: leagues[i] for i in range(len(ids)) if leagues[i]}


def challenger(region, params={}):
    meta = "{}|{}".format(region.lower(), params.get("type", ""))

    challenger = merakikernel.rediscache.get_value(_leagues_typename, "challenger", meta)

    if challenger:
        return challenger

    url = "/api/lol/{}/v2.5/league/challenger".format(region)
    challenger = merakikernel.requests.get(region, url, params)

    merakikernel.rediscache.put_value(_leagues_typename, "challenger", challenger, meta)

    return challenger


def master(region, params={}):
    meta = "{}|{}".format(region.lower(), params.get("type", ""))

    master = merakikernel.rediscache.get_value(_leagues_typename, "master", meta)

    if master:
        return master

    url = "/api/lol/{}/v2.5/league/master".format(region)
    master = merakikernel.requests.get(region, url, params)

    merakikernel.rediscache.put_value(_leagues_typename, "master", master, meta)

    return master

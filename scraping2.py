from bs4 import BeautifulSoup
import requests
import json
import time
import os




def get_league_html(session, league, season, window):
    """
    HTML page response
    """
    URL_LEAGUE = "https://www.transfermarkt.com/premier-league/transfers/wettbewerb/{league}/plus/?saison_id={season}&s_w={window}"
    print(URL_LEAGUE)

    scrape_url = URL_LEAGUE.format(
        league=league,
        season=season,
        window=window
    )
    resp = session.get(scrape_url)

    #print(BeautifulSoup(resp.text)[:2000])
    return BeautifulSoup(resp.text)


def parse_team_id_from_url(url):
    """
    Helper to prase team id from URL
    """
    if 'verein/' in url:
        return url.split('/')[4]

    return None


def scrape_transfer_table(transfer_table_soup):
    """
    Scrape data from team transfers HTML table
    """
    table_records = transfer_table_soup.find("tbody").findAll("tr")

    # No rows with player transfers info
    if len(table_records[0].findAll("td")) <= 1:
        return None

    records = []
    for rec in table_records:
        rec_data = {}
        try:
            rec_data['player_name'] = rec.find("td").find("div").text.strip()
            rec_data['player_id'] = rec.find("td").find("div").find("a")["href"].split("spieler/")[-1]
            rec_data['player_age'] = rec.find("td", class_="zentriert alter-transfer-cell").text.strip()

            # player nationalities
            nationalities = rec_data['player_nat'] = rec.find(
                "td",
                class_="zentriert nat-transfer-cell"
            ).findAll("img")
            rec_data['player_nat'] = [nat['title'].strip() for nat in nationalities]

            rec_data['player_pos'] = rec.find("td", class_="kurzpos-transfer-cell zentriert").text.strip()
            rec_data['market_val'] = rec.find("td", class_="rechts mw-transfer-cell").text.strip()

            # counter team data
            counter_team = rec.find("td", class_="verein-flagge-transfer-cell")
            rec_data['counter_team_country'] = counter_team.find("img")["title"].strip() if counter_team.find(
                "img") else counter_team.text.strip()
            rec_data['counter_team_name'] = counter_team.find("a")["title"].strip() if counter_team.find(
                "a") else counter_team.text.strip()
            rec_data['counter_team_id'] = parse_team_id_from_url(
                counter_team.find("a")["href"]
            ) if counter_team.find("a") else counter_team.text.strip()

            # transfer data
            transfer = rec.findAll("td", class_="rechts")[-1].find("a")
            rec_data['transfer_fee'] = transfer.text.strip()
            rec_data['transfer_id'] = transfer["href"].split("transfer_id/")[-1]

        except Exception as e:
            print(rec)
            raise e

        records.append(rec_data)

    return records


def scrape_league_season(session, league, season, window):
    """

    """
    league_soup = get_league_html(session, league, season, window)
    league_country = league_soup.find("div", class_="flagge").find("img")['title'].strip()

    boxes = league_soup.find_all(class_="box")
    team_boxes = []
    for box in boxes:
        if box.find("div", class_="transfer-zusatzinfo-box"):  # transfer-zusatzinfo-box
            team_boxes.append(box)

    data = []
    for box in team_boxes:
        # team name and ID
        team_info_tag = box.find("div", class_="table-header")
        team_name = team_info_tag.text.strip()
        team_id = team_info_tag['id'].split('-')[1]

        # Tables with transfers
        team_tables = box.find_all("table")

        # IN transfers
        in_transfers = scrape_transfer_table(team_tables[0])

        # OUT transfers
        out_transfers = scrape_transfer_table(team_tables[1])

        data.append(
            {
                'team': {
                    'team_name': team_name,
                    'team_id': team_id,
                    'team_country': league_country
                },
                'in': in_transfers,
                'left': out_transfers
            }
        )

    return data


def scrape_script():
    HEADERS = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'cache-control': 'max-age=0',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36 OPR/62.0.3331.116',
    }

    SCRAPE_LEAGUES = ['GB1', 'ES1', 'IT1', 'L1', 'FR1', 'PO1', 'NL1']
    SCRAPE_SEASONS = [2002, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021]
    SCRAPE_WINDOWS = ["s", "w"]

    session = requests.session()
    session.headers.update(HEADERS)

    for league in SCRAPE_LEAGUES:
        for season in SCRAPE_SEASONS:
            for window in SCRAPE_WINDOWS:
                time.sleep(15)
                print('SCRAPE:', league, season, window)

                data = scrape_league_season(session, league, season, window)

                filename = f'{league}_{season}_{window}.json'
                print(filename)
                #if not os.path.exists(filename): os.makedirs(filename)
                with open(filename, 'w', encoding='utf8') as output:
                    json.dump(data, output, ensure_ascii=False)

    return None

scrape_script()
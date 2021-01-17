from Arcapi import SyncApi
from PIL import Image, ImageFont, ImageDraw
from datetime import datetime
import random

async def genimg(code:int):
    api = SyncApi(str(code))
    raw = api.userbest30()

    songs = []
    for i in raw[2:]:
        if type(i) == dict:
            songs.append(i)
            continue
        for j in i:
                if type(j) == dict:
                    songs.append(j)
                    continue

    songs = sorted(songs, key=lambda k:k['rating'], reverse=True)
    refls = {0: '[PST]', 1: '[PRS]', 2: '[FTR]', 3: '[BYD]'}
    for i in songs:
        i['difficulty'] = refls[i['difficulty']]
    best30 = songs[:30]

    ft = ImageFont.truetype('/root/service/nonebot/assets/arcbot/Roboto-Bold.ttf', 18)
    ft_low = ImageFont.truetype('/root/service/nonebot/assets/arcbot/Roboto-Regular.ttf', 14)
    ft_title = ImageFont.truetype('/root/service/nonebot/assets/arcbot/Roboto-Bold.ttf', 25)

    img = Image.open('/root/service/nonebot/assets/arcbot/in.png')
    draw = ImageDraw.Draw(img)

    songs = [i['song_id'].title() for i in best30]
    difficulties = [i['difficulty'] for i in best30]
    scores = [str(i['score']) for i in best30]
    ratings = [str(f"{i['rating']:.2f}") for i in best30]

    title_color = (230, 230, 230)
    inner_gap = [20, 52, 52]

    for i in range(15):
        ylen = 60 * i
        draw.text((150, ylen + inner_gap[0]), songs[i] + ' ' + difficulties[i], title_color, font=ft_title)
        draw.text((150, ylen + inner_gap[1]), 'Score: ' + scores[i], (255, 255, 255), font=ft)
        draw.text((400, ylen + inner_gap[2]), 'PTT: ' + ratings[i], (255, 255, 255), font=ft)
        draw.text((600, ylen + inner_gap[0]), songs[i+15] + ' ' + difficulties[i+15], title_color, font=ft_title)
        draw.text((600, ylen + inner_gap[1]), 'Score: ' + scores[i+15], (255, 255, 255), font=ft)
        draw.text((850, ylen + inner_gap[2]), 'PTT: ' + ratings[i+15], (255, 255, 255), font=ft)
        draw.text((20, 930), datetime.now().strftime("%Y-%m-%d  %H:%M") + "   Powered by iyume", (200, 200, 200), font=ft_low)

    url = '/root/service/nonebot/assets/arcbot/'
    random.seed(datetime.now())
    name = f'{random.randint(pow(2,32), pow(2,33)):x}'
    save_to = url + name + '.jpg'
    img.save(save_to)

    return save_to


async def getrecent(code:int) -> str:
    api = SyncApi(str(code))
    raw = api.userbest30()
    recent = raw[1]['recent_score'][0]

    refls = {0: '[PST]', 1: '[PRS]', 2: '[FTR]', 3: '[BYD]'}
    recent['difficulty'] = refls[recent['difficulty']]

    return '\n'.join([recent['song_id'].title(), "Score: " + str(recent['score']), "PTT: " + f"{recent['rating']:.2f}"])

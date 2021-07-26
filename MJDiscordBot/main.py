import discord
import os
import math
from discord.ext import commands
import keep_alive

client = commands.Bot(command_prefix='$')
scores = [0,0,0,0,8000,8000,12000,12000,16000,16000,16000,24000,24000,32000]
sequence = '123456789'
honors = 'SDZ'

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    await client.process_commands(message)

@client.command()
async def hand(ctx, arg):
  if 'p' not in arg or 'b' not in arg:
    await ctx.send("Your input should have format XpYYbZ. e.g. 2p60b1")
    return

  points, bonus = arg.split("b")
  bonus = int(bonus)
  if bonus < 0:
    await ctx.send("You can't have a negative bonus round wtf.")
    return
  o_han, o_fu = points.split("p")
  han = int(o_han)
  fu = int(o_fu)

  if han<1 or (fu%10!=0 and fu!=25) or fu>110 or fu<20 or (han==1 and fu<30):
      await ctx.send("Invalid Hand")
      return
  if (han==3 and fu>60) or (han==4 and fu>30):
      han = int(5)
  if han > 13:
    han = int(13)
  if han >= 5:
    base = scores[han]
    nond_ron = base + bonus*300
    d_ron = int(base*1.5) + bonus*300
    nond_tsumo = (int(base/2)+bonus*100, int(base/4)+bonus*100)
    d_tsumo = int(base*1.5/3)+bonus*100
  else:
    base = fu*(2**(han+2))
    nond_ron = int(math.ceil(base*4/100))*100 + bonus*300
    d_ron = int(math.ceil(base*6/100))*100 + bonus*300
    nond_tsumo = (int(math.ceil(base*2/100))*100 + bonus*100,int(math.ceil(base*1/100))*100 + bonus*100)
    d_tsumo = int(math.ceil(base*2/100))*100 + bonus*100

  reminder = 'Multiply the following by the number of yakumans your hand is worth.\n' if han == 13 else ''
  msg = reminder + 'Hand: {0} Point {1} Fu Bonus {2} \nNon-Dealer Ron: {3} \nNon-Dealer Tsumo: {4}(Dealer) {5}(Non-Dealer) \nDealer Ron: {6} \nDealer Tsumo: {7} All'

  await ctx.send(msg.format(int(o_han),int(o_fu),bonus,nond_ron,nond_tsumo[0],nond_tsumo[1],d_ron,d_tsumo))
  return


@client.command()
async def fu(ctx, hand):
    hand = hand.replace(" ","").split(',')
    if type(hand) != list or not all(type(meld)==str for meld in hand):
        await ctx.send('bitch this format ain\'t it')
        return
    
    if len(hand) != 5:
        if len(hand) == 7:
            if all(len(meld)==2 for meld in hand):
                await ctx.send('Fu: 25 (7 Pairs is always 25)')
                return
            else:
                await ctx.send('there\'s something wrong with your pairs')
        else:
            await ctx.send('wrong number of melds bro')
            return
        
    is_open = False
    acc_fu = 0
    ryanmen = False
    
    pair_count = 0
    tripquad_count = 0
    
    for meld in hand:
        if meld.startswith('C') or meld.startswith('O'):
            tiles = meld[1:]

            if len(tiles) == 2 and ((tile in sequence or tile in honors) for tile in tiles[1:]):
                pair_count += 1
                if meld.startswith('O'):
                    await ctx.send('your pair cannot be open')
                    return
                if tiles[0] != tiles[1]:
                    await ctx.send('your pair has two different tiles lmao')
                    return
                if tiles[0] in honors:
                    if tiles[0] == 'D':
                        acc_fu += 4
                    else:
                        acc_fu += 2
                
            if len(tiles) == 3:
                tripquad_count += 1
                if meld.startswith('O'):
                    is_open = True
                if tiles in sequence:
                    continue
                if all(tile == tiles[0] and (tile in sequence or tile in honors) for tile in tiles[1:]):
                    if meld.startswith('O'):
                        if tiles[0] in sequence[1:-1]:
                            acc_fu += 2
                        else:
                            acc_fu += 4
                    else:
                        if tiles[0] in sequence[1:-1]:
                            acc_fu += 4
                        else:
                            acc_fu += 8
                else:
                    await ctx.send('something is wrong with one of your triplets bro')
                    return
                
            if len(tiles) == 4:
                tripquad_count += 1
                if tiles in sequence:
                    await ctx.send('sequences are limited to 3 tiles')
                    return
                if all(tile == tiles[0] and (tile in sequence or tile in honors) for tile in tiles[1:]):
                    if meld.startswith('O'):
                        is_open = True
                        if tiles[0] in sequence[1:-1]:
                            acc_fu += 8
                        else:
                            acc_fu += 16
                    else:
                        if tiles[0] in sequence[1:-1]:
                            acc_fu += 16
                        else:
                            acc_fu += 32
                else:
                    await ctx.send('you need to check your kans')
                    return
                
        if '*' in meld:
            if all(tile in sequence or tile in honors for tile in meld if tile != '*'):
                juliets, romeo = meld.split('*')
                
                if len(juliets) == 1 and juliets == romeo:
                    pair_count += 1
                    acc_fu += 2
                    
                    if juliets in honors:
                        if juliets == 'D':
                            acc_fu += 4
                        else:
                            acc_fu += 2

                elif juliets[0] + romeo + juliets[1] in sequence:
                    tripquad_count += 1
                    acc_fu += 2 

                elif juliets + romeo == sequence[:3] or romeo + juliets == sequence[6:]:
                    tripquad_count += 1
                    acc_fu += 2

                elif juliets[0] == juliets[1] == romeo:
                    tripquad_count += 1
                    if juliets[0] in sequence[1:-1]:
                        acc_fu += 4
                    else:
                        acc_fu += 8
                    
                elif juliets + romeo in sequence or romeo + juliets in sequence:
                    tripquad_count += 1
                    ryanmen = True
                    
                else:
                    await ctx.send('winning meld is problematic')
                    return
            
            else:
                await ctx.send('winning meld is problematic')
                return
            
    if pair_count != 1 or tripquad_count != 4:
        msg = 'Invalid Hand'
        await ctx.send(msg)
        return
            
    if not is_open and acc_fu == 0 and ryanmen:
        msg = 'Pinfu Tsumo: 20 Fu\nPinfu Deal In: 30 Fu'
        await ctx.send(msg)
        return
        
    base = 30 if not is_open else 20
    deal_fu = 30 if base + acc_fu == 20 else int(math.ceil((base + acc_fu)/10))*10
    tsumo_fu = int(math.ceil((base + acc_fu + 2)/10))*10
    
    msg = 'Tsumo: {0} Fu\nDeal In: {1} Fu'
    await ctx.send(msg.format(tsumo_fu, deal_fu))
            
            
    return


keep_alive.keep_alive()

client.run(os.getenv('TOKEN'))
